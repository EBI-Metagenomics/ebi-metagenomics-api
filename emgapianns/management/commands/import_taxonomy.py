#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import logging
import os
import re

from emgapianns import models as m_models

from ..lib import EMGBaseCommand

logger = logging.getLogger(__name__)


ORGANISM_RANK = {
    '1.0': ['kingdom', 'phylum', 'class', 'order', 'family', 'genus',
            'species'],
    '2.0': ['kingdom', 'phylum', 'class', 'order', 'family', 'genus',
            'species'],
    '3.0': ['kingdom', 'phylum', 'class', 'order', 'family', 'genus',
            'species'],
    '4.0': ['super kingdom', 'kingdom', 'phylum', 'class', 'order', 'family',
            'genus', 'species'],
    '4.1': ['super kingdom', 'kingdom', 'phylum', 'class', 'order', 'family',
            'genus', 'species'],
    '5.0': ['super kingdom', 'kingdom', 'phylum', 'class', 'order', 'family',
            'genus', 'species'],
}


class Command(EMGBaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def populate_from_accession(self, options):
        logger.info("Found %d" % len(self.obj_list))
        for o in self.obj_list:
            self.find_path(o, options)

    def load_data_from_file(self, f, obj):
        if f is not None and os.path.exists(f) and os.path.isfile(f):
            logger.info("Found: %s" % f)
            with open(f) as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                self.load_organism_from_summary_file(reader, obj)
        else:
            logger.error("Path %r exist. No Taxonomy SKIPPING!" % f)

    def find_path(self, obj, options):
        rootpath = options.get('rootpath', None)

        res = os.path.join(rootpath, obj.result_directory, 'taxonomy-summary')
        if os.path.exists(res):
            logger.info("Pipeline version: %s" %
                        obj.pipeline.release_version)
            if obj.pipeline.release_version in ('1.0', '2.0', '3.0',):
                _f = os.path.join(res, 'krona-input.txt')
                if os.path.exists(_f):
                    logger.info("Taxonomy loading: %s" % _f)
                    with open(_f) as csvfile:
                        reader = csv.reader(csvfile, delimiter='\t')
                        self.load_organism_from_summary_file(
                            reader, obj, 'taxonomy')
            elif obj.pipeline.release_version in ('4.0', '4.1', '5.0',):
                name = "%s_SSU.fasta.mseq.txt" % (obj.input_file_name)
                _f = os.path.join(res, 'SSU', name)
                if os.path.exists(_f):
                    logger.info("SSU loading: %s" % _f)
                    with open(_f) as csvfile:
                        reader = csv.reader(csvfile, delimiter='\t')
                        self.load_organism_from_summary_file(
                            reader, obj, 'taxonomy_ssu')
                name = "%s_LSU.fasta.mseq.txt" % (obj.input_file_name)
                _f = os.path.join(res, 'LSU', name)
                if os.path.exists(_f):
                    logger.info("LSU loading: %s" % _f)
                    with open(_f) as csvfile:
                        reader = csv.reader(csvfile, delimiter='\t')
                        self.load_organism_from_summary_file(
                            reader, obj, 'taxonomy_lsu')
                if obj.pipeline.release_version == '5.0':
                    # This version of the pipeline introduced ITS
                    self.load_its(res, obj, 'itsonedb')
                    self.load_its(res, obj, 'unite')
            else:
                logger.error("Pipeline not supported SKIPPING!")
        else:
            logger.error("Path %r doesn't exist. SKIPPING!" % res)

    def load_its(self, res, ajob, db):
        """Load ITS results into Mongo.
        Arguments:
        res  -- root path of the results
        ajob -- AnalysisJob
        db  --  ITS DB (unite or itsonedb)

        If the file is not found then the method will fail silently.
        """
        if db not in ('itsonedb', 'unite',):
            logger.error('ITS not supported {}'.format(db))
            return

        _f = os.path.join(res, 'its', db, '{}_{}.fasta.mseq.txt'.format(ajob.input_file_name, db))
        if not os.path.exists(_f):
            # OK, let's try in lowercase
            _f = os.path.join(res, 'its', db.lower(),
                              '{}_{}.fasta.mseq.txt'.format(ajob.input_file_name, db.lower()))
            if not os.path.exists(_f):
                logger.warn('ITS file {} not found (not even with lowercase).'.format(_f))
                return

        logger.info('ITS {} loading: {}'.format(db, _f))

        with open(_f) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            field = db.replace('its', '').lower()
            self.load_organism_from_summary_file(
                reader, ajob, 'taxonomy_its{}'.format(field))

    def load_organism_from_summary_file(self, reader, obj, tax):  # noqa
        try:
            run = m_models.AnalysisJobTaxonomy.objects \
                .get(pk=str(obj.job_id))
        except m_models.AnalysisJobTaxonomy.DoesNotExist:
            run = m_models.AnalysisJobTaxonomy()
        run.analysis_id = str(obj.job_id)
        run.accession = obj.accession
        version = obj.pipeline.release_version
        run.pipeline_version = version
        run.job_id = obj.job_id
        new_orgs = list()
        orgs = []
        setattr(run, tax, list())
        for row in reader:
            if len(row) < 1:
                continue
            count = row[0]

            def clean_prefix(s):
                return re.sub(r"[a-zA-Z]+__", "", s.rstrip())
            lineage = list(map(clean_prefix, row[1:]))

            if len(lineage) > 1:
                hierarchy = {
                    r: a for r, a in zip(ORGANISM_RANK[version], lineage)
                }
                domain = lineage[0]
                name = lineage[-1]
                ancestors = lineage[0:-1]
                parent = ancestors[-1]
                rank = ORGANISM_RANK[version][len(ancestors)]
            else:
                ancestors = []
                parent = None
                try:
                    if len(lineage[0]) > 0:
                        hierarchy = {
                            r: a for r, a in zip(ORGANISM_RANK[version],
                                                 lineage)
                        }
                        domain = lineage[0]
                        name = lineage[0]
                        rank = ORGANISM_RANK[version][len(ancestors)]
                    else:
                        name = 'Unusigned'
                        rank = None
                        lineage = ['Unusigned']
                        hierarchy = {}
                        domain = None
                except KeyError:
                    name = 'Unusigned'
                    rank = None
                    lineage = ['Unusigned']
                    hierarchy = {}
                    domain = None
            organism = None
            try:
                organism = m_models.Organism.objects.get(
                    lineage=":".join(lineage), rank=rank,
                    pipeline_version=version
                )
            except m_models.Organism.DoesNotExist:
                #  TODO https://github.com/MongoEngine/mongoengine/issues/1685
                pk = "%s|%s" % (":".join(lineage), version)
                organism = m_models.Organism(
                    id=pk,
                    lineage=":".join(lineage), name=name, parent=parent,
                    ancestors=ancestors, hierarchy=hierarchy,
                    rank=rank, pipeline_version=version, domain=domain
                )
                new_orgs.append(organism)

            if organism is not None:
                orgs.append(organism)
                rorg = m_models.AnalysisJobOrganism(
                    count=count,
                    organism=organism
                )
                t = getattr(run, tax, list())
                t.append(rorg)
                setattr(run, tax, t)

        if len(orgs) > 0:
            logger.info(
                'Total {} Organisms for Run: {} {} {}'.format(len(orgs), obj.accession, version, tax))
            if len(new_orgs) > 0:
                m_models.Organism.objects.insert(new_orgs)
                logger.info(
                    'Created {} new Organisms'.format(len(new_orgs)))
            run.save()
            logger.info('Saved Run {}'.format(run))

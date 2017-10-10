#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import logging

from emgapianns import models as m_models

from ..lib import EMGBaseCommand

logger = logging.getLogger(__name__)


class Command(EMGBaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('suffix', nargs='?', type=str, default='.go_slim')

    def populate_from_accession(self, options):
        logger.info("Found %d" % len(self.obj_list))
        for o in self.obj_list:
            self.find_path(o, options)

    def find_path(self, obj, options):
        rootpath = options.get('rootpath', None)
        self.suffix = options.get('suffix', None)

        res = os.path.join(rootpath, obj.result_directory)
        logger.info("Scanning path: %s" % res)
        if os.path.exists(res):
            if os.path.isdir(res):
                for root, dirs, files in os.walk(res, topdown=False):
                    for name in files:
                        if name.endswith(self.suffix):
                            _f = os.path.join(root, name)
                            logger.info("Found: %s" % _f)
                            with open(_f) as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                if self.suffix == '.ipr':
                                    self.load_ipr_from_summary_file(
                                        reader, obj
                                    )
                                elif self.suffix in ('.go_slim', '.go'):
                                    self.load_go_from_summary_file(
                                        reader, obj
                                    )
                            continue
            elif os.path.isfile(res):
                raise NotImplementedError("Give path to directory.")
        else:
            logger.error("Path %r doesn't exist. SKIPPING!" % res)

    def load_go_from_summary_file(self, reader, obj):  # noqa
        try:
            run = m_models.AnalysisJobGoTerm.objects \
                .get(analysis_id=obj.job_id)
        except m_models.AnalysisJobGoTerm.DoesNotExist:
            run = m_models.AnalysisJobGoTerm()
        run.analysis_id = str(obj.job_id)
        run.accession = obj.accession
        run.pipeline_version = obj.pipeline.release_version
        run.job_id = obj.job_id
        new_anns = []
        anns = []
        for row in reader:
            try:
                row[0].lower().startswith('go:')
            except KeyError:
                pass
            else:
                ann = None
                try:
                    ann = m_models.GoTerm.objects.get(accession=row[0])
                except m_models.GoTerm.DoesNotExist:
                    ann = m_models.GoTerm(
                        accession=row[0],
                        description=row[1],
                        lineage=row[2],
                    )
                    new_anns.append(ann)
                if ann is not None:
                    anns.append(ann)
                    if self.suffix == '.go_slim':
                        rann = m_models.AnalysisJobGoTermAnnotation(
                            count=row[3],
                            go_term=ann
                        )
                        run.go_slim.append(rann)
                    elif self.suffix == '.go':
                        rann = m_models.AnalysisJobGoTermAnnotation(
                            count=row[3],
                            go_term=ann
                        )
                        run.go_terms.append(rann)
        if len(anns) > 0:
            logger.info(
                "Total %d Annotations for Run: %s" % (
                    len(anns), obj.accession))
            if len(new_anns) > 0:
                m_models.GoTerm.objects.insert(new_anns)
                logger.info(
                    "Created %d new GoTerm Annotations" % len(new_anns))
            run.save()
            logger.info("Saved Run %r" % run)

    def load_ipr_from_summary_file(self, reader, obj):  # noqa
        try:
            run = m_models.AnalysisJobInterproIdentifier.objects.get(
                analysis_id=obj.job_id)
        except m_models.AnalysisJobInterproIdentifier.DoesNotExist:
            run = m_models.AnalysisJobInterproIdentifier()
        run.analysis_id = str(obj.job_id)
        run.accession = obj.accession
        run.pipeline_version = obj.pipeline.release_version
        run.job_id = obj.job_id
        new_anns = []
        anns = []
        for row in reader:
            try:
                row[0].lower().startswith('ipr')
            except KeyError:
                pass
            else:
                ann = None
                try:
                    ann = m_models.InterproIdentifier.objects \
                        .get(accession=row[0])
                except m_models.InterproIdentifier.DoesNotExist:
                    ann = m_models.InterproIdentifier(
                        accession=row[0],
                        description=row[1],
                    )
                    new_anns.append(ann)
                if ann is not None:
                    anns.append(ann)
                    if self.suffix == '.ipr':
                        rann = m_models.AnalysisJobInterproIdentifierAnnotation(  # NOQA
                            count=row[2],
                            interpro_identifier=ann
                        )
                        run.interpro_identifiers.append(rann)
        if len(anns) > 0:
            logger.info(
                "Total %d Annotations for Run: %s" % (
                    len(anns), obj.accession))
            if len(new_anns) > 0:
                m_models.InterproIdentifier.objects.insert(new_anns)
                logger.info(
                    "Created %d new IPR Annotations" % len(new_anns))
            run.save()
            logger.info("Saved Run %r" % run)

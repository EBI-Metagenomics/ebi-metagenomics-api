import logging
import os

from django.core.management import BaseCommand
from ena_portal_api import ena_handler

from emgapianns.management.lib import utils

logger = logging.getLogger(__name__)

cog_cache = {}
ipr_cache = {}
kegg_cache = {}

ena = ena_handler.EnaApiHandler()

"""
    Cl call:
        emgcli import_analysis <primary_accession> /home/maxim/
    Draft
    Inputs:
        - Accessions: Study, Sample and (run or assembly)
        - Path to the result directory
"""


class Importer:

    def __init__(self, rootpath, accession):
        """

        :param rootpath: NFS root path of the results archive
        :param accession: ENA accession for run or assembly/analysis
        """
        self._rootpath = os.path.realpath(rootpath).strip()
        self._accession = accession
        self.existence_check()

    def get_rootpath(self):
        return self._rootpath

    def get_accession(self):
        return self._accession

    def existence_check(self):
        """
            Check if result folder does exit on the production file system.
        :return:
        """
        if not os.path.exists(self._rootpath):
            raise FileNotFoundError('Results dir {} does not exist'.format(self._rootpath))

    def sanity_check_dir(self, experiment_type):
        """
            Step 1: Search run/assembly result folder
            Step 2: Perform sanity check on result folder
        :type experiment_type: Possible values are AMPLICON, WGS, RNA-Seq, ASSEMBLY
        :return:
        """
        # Step 1
        utils.retrieve_existing_result_dir(self._rootpath, self.get_accession())

        pass

    def get_raw_metadata(self):
        """
            Retrieves metadata from the ENA for the given run or assembly accession.
        :return:
        """
        return ena.get_run(run_accession=self.get_accession())

    def get_or_create_study(self, study_accession):
        pass

    def get_or_create_publication(self):
        pass

    def link_study_publication(self, study, publication):
        pass

    def get_or_create_sample(self):
        pass

    def get_or_create_run(self, raw_metadata):
        pass

    def link_study_sample(self, study, sample):
        pass

    def link_run_sample(self, run, sample):
        pass

    def link_analysis_run(self, analysis, run):
        pass

    def link_analysis_assembly(self, analysis, assembly):
        pass

    def link_assembly_sample(self, assembly, sample):
        pass

    def get_or_create_analysis(self, raw_metadata):
        pass


class Command(BaseCommand):
    help = 'Imports new objects into EMG.'

    obj_list = list()
    rootpath = None
    genome_folders = None

    database = None

    def add_arguments(self, parser):
        parser.add_argument('accession',
                            help='ENA primary accession for run or assembly',
                            type=str,
                            action='store')
        parser.add_argument('--prod_dir',
                            help="NFS root path of the results archive",
                            default='/nfs/production/interpro/metagenomics/results/')

        # parser.add_argument('--update', action='store_true')
        #  parser.add_argument('--database', type=str, default='default')

    def handle(self, *args, **options):
        importer = Importer(
            options.get('prod_dir'),
            options['accession']
        )

        logger.info("CLI %r" % options)

        is_assembly = utils.is_assembly(importer.get_accession())
        logger.info("Identified assembly accession: {0}".format(is_assembly))

        if is_assembly:
            assembly, experiment_type = utils.parse_assembly_metadata(
                ena.get_assembly(assembly_name=importer.get_accession()))
            pass
        else:  # Run accession detected
            run, experiment_type = utils.parse_run_metadata(ena.get_run(run_accession=importer.get_accession()))

        importer.sanity_check_dir(experiment_type)

        study = importer.get_or_create_study(study_accession)
        #
        # publication = self.get_or_create_publication()
        # self.link_study_publication(study, publication)
        #
        # sample = self.get_or_create_sample(raw_metadata['sample_accession'])
        # self.link_study_sample(study, sample)
        #
        # analysis = self.get_or_create_analysis(raw_metadata)
        #
        # if self.is_run(raw_metadata):
        #     run = self.get_or_create_run(raw_metadata)
        #     self.link_run_sample(run, sample)
        #     self.link_analysis_run(analysis, run)
        # elif self.is_assembly(raw_metadata):
        #     assembly = self.get_or_create_assembly(raw_metadata)
        #     self.link_assembly_sample(assembly, sample)
        #     self.link_analysis_assembly(analysis, assembly)
        # else:
        #     raise ValueError(
        #         'Could not determine if object is run or assembly from accession.')
        #
        # # TODO: If assembly is linked to run create RunAssembly object
        #
        # self.load_api_files(raw_accession, self.rootpath)

        logger.info("Program finished successfully.")

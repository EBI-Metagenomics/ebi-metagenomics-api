# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 18:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisStatus',
            fields=[
                ('analysis_status_id', models.AutoField(db_column='ANALYSIS_STATUS_ID', primary_key=True, serialize=False)),
                ('analysis_status', models.CharField(db_column='ANALYSIS_STATUS', max_length=25)),
            ],
            options={
                'db_table': 'ANALYSIS_STATUS',
                'ordering': ('analysis_status_id',),
            },
        ),
        migrations.CreateModel(
            name='Biome',
            fields=[
                ('biome_id', models.SmallIntegerField(db_column='BIOME_ID', primary_key=True, serialize=False)),
                ('biome_name', models.CharField(db_column='BIOME_NAME', max_length=60)),
                ('lft', models.SmallIntegerField(db_column='LFT')),
                ('rgt', models.SmallIntegerField(db_column='RGT')),
                ('depth', models.IntegerField(db_column='DEPTH')),
                ('lineage', models.CharField(db_column='LINEAGE', max_length=500)),
            ],
            options={
                'db_table': 'BIOME_HIERARCHY_TREE',
                'ordering': ('biome_id',),
            },
        ),
        migrations.CreateModel(
            name='ExperimentType',
            fields=[
                ('experiment_type_id', models.AutoField(db_column='EXPERIMENT_TYPE_ID', primary_key=True, serialize=False)),
                ('experiment_type', models.CharField(db_column='EXPERIMENT_TYPE', max_length=30)),
            ],
            options={
                'db_table': 'EXPERIMENT_TYPE',
            },
        ),
        migrations.CreateModel(
            name='PipelineRelease',
            fields=[
                ('pipeline_id', models.AutoField(db_column='PIPELINE_ID', primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, db_column='DESCRIPTION', null=True)),
                ('changes', models.TextField(blank=True, db_column='CHANGES', null=True)),
                ('release_version', models.CharField(db_column='RELEASE_VERSION', max_length=20)),
                ('release_date', models.DateField(db_column='RELEASE_DATE')),
            ],
            options={
                'db_table': 'PIPELINE_RELEASE',
                'ordering': ('release_version',),
            },
        ),
        migrations.CreateModel(
            name='PipelineTool',
            fields=[
                ('tool_id', models.SmallIntegerField(db_column='TOOL_ID', primary_key=True, serialize=False)),
                ('tool_name', models.CharField(db_column='TOOL_NAME', max_length=30)),
                ('description', models.TextField(db_column='DESCRIPTION')),
                ('web_link', models.CharField(blank=True, db_column='WEB_LINK', max_length=500, null=True)),
                ('version', models.CharField(db_column='VERSION', max_length=30)),
                ('exe_command', models.CharField(db_column='EXE_COMMAND', max_length=500)),
                ('installation_dir', models.CharField(blank=True, db_column='INSTALLATION_DIR', max_length=200, null=True)),
                ('configuration_file', models.TextField(blank=True, db_column='CONFIGURATION_FILE', null=True)),
                ('notes', models.TextField(blank=True, db_column='NOTES', null=True)),
            ],
            options={
                'db_table': 'PIPELINE_TOOL',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('pub_id', models.AutoField(db_column='PUB_ID', primary_key=True, serialize=False)),
                ('authors', models.CharField(blank=True, db_column='AUTHORS', max_length=4000, null=True)),
                ('doi', models.CharField(blank=True, db_column='DOI', max_length=1500, null=True)),
                ('isbn', models.CharField(blank=True, db_column='ISBN', max_length=100, null=True)),
                ('iso_journal', models.CharField(blank=True, db_column='ISO_JOURNAL', max_length=255, null=True)),
                ('issue', models.CharField(blank=True, db_column='ISSUE', max_length=55, null=True)),
                ('medline_journal', models.CharField(blank=True, db_column='MEDLINE_JOURNAL', max_length=255, null=True)),
                ('pub_abstract', models.TextField(blank=True, db_column='PUB_ABSTRACT', null=True)),
                ('pubmed_central_id', models.IntegerField(blank=True, db_column='PUBMED_CENTRAL_ID', null=True)),
                ('pubmed_id', models.IntegerField(blank=True, db_column='PUBMED_ID', null=True)),
                ('pub_title', models.CharField(db_column='PUB_TITLE', max_length=740)),
                ('raw_pages', models.CharField(blank=True, db_column='RAW_PAGES', max_length=30, null=True)),
                ('url', models.CharField(blank=True, db_column='URL', max_length=740, null=True)),
                ('volume', models.CharField(blank=True, db_column='VOLUME', max_length=55, null=True)),
                ('published_year', models.SmallIntegerField(blank=True, db_column='PUBLISHED_YEAR', null=True)),
                ('pub_type', models.CharField(blank=True, db_column='PUB_TYPE', max_length=150, null=True)),
            ],
            options={
                'db_table': 'PUBLICATION',
                'ordering': ('pub_id',),
            },
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('run_id', models.BigAutoField(db_column='JOB_ID', primary_key=True, serialize=False)),
                ('accession', models.CharField(db_column='EXTERNAL_RUN_IDS', max_length=100)),
                ('job_operator', models.CharField(db_column='JOB_OPERATOR', max_length=15)),
                ('submit_time', models.DateTimeField(db_column='SUBMIT_TIME')),
                ('complete_time', models.DateTimeField(blank=True, db_column='COMPLETE_TIME', null=True)),
                ('input_file_name', models.CharField(db_column='INPUT_FILE_NAME', max_length=50)),
                ('result_directory', models.CharField(db_column='RESULT_DIRECTORY', max_length=100)),
                ('is_production_run', models.TextField(blank=True, db_column='IS_PRODUCTION_RUN', null=True)),
                ('run_status_id', models.IntegerField(blank=True, db_column='RUN_STATUS_ID', null=True)),
                ('instrument_platform', models.CharField(blank=True, db_column='INSTRUMENT_PLATFORM', max_length=50, null=True)),
                ('instrument_model', models.CharField(blank=True, db_column='INSTRUMENT_MODEL', max_length=50, null=True)),
                ('analysis_status', models.ForeignKey(db_column='ANALYSIS_STATUS_ID', on_delete=django.db.models.deletion.CASCADE, to='emg_api.AnalysisStatus')),
                ('experiment_type', models.ForeignKey(blank=True, db_column='EXPERIMENT_TYPE_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to='emg_api.ExperimentType')),
            ],
            options={
                'db_table': 'ANALYSIS_JOB',
                'ordering': ('accession',),
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('sample_id', models.AutoField(db_column='SAMPLE_ID', primary_key=True, serialize=False)),
                ('accession', models.CharField(db_column='EXT_SAMPLE_ID', max_length=15)),
                ('analysis_completed', models.DateField(blank=True, db_column='ANALYSIS_COMPLETED', null=True)),
                ('collection_date', models.DateField(blank=True, db_column='COLLECTION_DATE', null=True)),
                ('geo_loc_name', models.CharField(blank=True, db_column='GEO_LOC_NAME', max_length=255, null=True)),
                ('is_public', models.IntegerField(blank=True, db_column='IS_PUBLIC', null=True)),
                ('metadata_received', models.DateTimeField(blank=True, db_column='METADATA_RECEIVED', null=True)),
                ('sample_desc', models.TextField(blank=True, db_column='SAMPLE_DESC', null=True)),
                ('sequencedata_archived', models.DateTimeField(blank=True, db_column='SEQUENCEDATA_ARCHIVED', null=True)),
                ('sequencedata_received', models.DateTimeField(blank=True, db_column='SEQUENCEDATA_RECEIVED', null=True)),
                ('environment_biome', models.CharField(blank=True, db_column='ENVIRONMENT_BIOME', max_length=255, null=True)),
                ('environment_feature', models.CharField(blank=True, db_column='ENVIRONMENT_FEATURE', max_length=255, null=True)),
                ('environment_material', models.CharField(blank=True, db_column='ENVIRONMENT_MATERIAL', max_length=255, null=True)),
                ('sample_name', models.CharField(blank=True, db_column='SAMPLE_NAME', max_length=255, null=True)),
                ('sample_alias', models.CharField(blank=True, db_column='SAMPLE_ALIAS', max_length=255, null=True)),
                ('host_tax_id', models.IntegerField(blank=True, db_column='HOST_TAX_ID', null=True)),
                ('species', models.CharField(blank=True, db_column='SPECIES', max_length=255, null=True)),
                ('latitude', models.DecimalField(blank=True, db_column='LATITUDE', decimal_places=4, max_digits=7, null=True)),
                ('longitude', models.DecimalField(blank=True, db_column='LONGITUDE', decimal_places=4, max_digits=7, null=True)),
                ('last_update', models.DateTimeField(db_column='LAST_UPDATE')),
                ('submission_account_id', models.CharField(blank=True, db_column='SUBMISSION_ACCOUNT_ID', max_length=15, null=True)),
            ],
            options={
                'db_table': 'SAMPLE',
                'ordering': ('accession',),
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('study_id', models.AutoField(db_column='STUDY_ID', primary_key=True, serialize=False)),
                ('accession', models.CharField(db_column='EXT_STUDY_ID', max_length=18)),
                ('centre_name', models.CharField(blank=True, db_column='CENTRE_NAME', max_length=255, null=True)),
                ('is_public', models.IntegerField(blank=True, db_column='IS_PUBLIC', null=True)),
                ('public_release_date', models.DateField(blank=True, db_column='PUBLIC_RELEASE_DATE', null=True)),
                ('study_abstract', models.TextField(blank=True, db_column='STUDY_ABSTRACT', null=True)),
                ('study_name', models.CharField(blank=True, db_column='STUDY_NAME', max_length=255, null=True)),
                ('study_status', models.CharField(blank=True, db_column='STUDY_STATUS', max_length=30, null=True)),
                ('data_origination', models.CharField(blank=True, db_column='DATA_ORIGINATION', max_length=20, null=True)),
                ('author_email', models.CharField(blank=True, db_column='AUTHOR_EMAIL', max_length=100, null=True)),
                ('author_name', models.CharField(blank=True, db_column='AUTHOR_NAME', max_length=100, null=True)),
                ('last_update', models.DateTimeField(db_column='LAST_UPDATE')),
                ('submission_account_id', models.CharField(blank=True, db_column='SUBMISSION_ACCOUNT_ID', max_length=15, null=True)),
                ('result_directory', models.CharField(blank=True, db_column='RESULT_DIRECTORY', max_length=100, null=True)),
                ('first_created', models.DateTimeField(db_column='FIRST_CREATED')),
                ('project_id', models.CharField(blank=True, db_column='PROJECT_ID', max_length=18, null=True)),
            ],
            options={
                'db_table': 'STUDY',
                'ordering': ('accession',),
            },
        ),
        migrations.CreateModel(
            name='PipelineReleaseTool',
            fields=[
                ('pipeline', models.ForeignKey(db_column='PIPELINE_ID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='emg_api.PipelineRelease')),
                ('tool_group_id', models.DecimalField(db_column='TOOL_GROUP_ID', decimal_places=3, max_digits=6)),
                ('how_tool_used_desc', models.TextField(db_column='HOW_TOOL_USED_DESC')),
                ('tool', models.ForeignKey(db_column='TOOL_ID', on_delete=django.db.models.deletion.CASCADE, to='emg_api.PipelineTool')),
            ],
            options={
                'db_table': 'PIPELINE_RELEASE_TOOL',
            },
        ),
        migrations.CreateModel(
            name='SamplePublication',
            fields=[
                ('sample', models.ForeignKey(db_column='SAMPLE_ID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='emg_api.Sample')),
                ('pub', models.ForeignKey(db_column='PUB_ID', on_delete=django.db.models.deletion.CASCADE, to='emg_api.Publication')),
            ],
            options={
                'db_table': 'SAMPLE_PUBLICATION',
            },
        ),
        migrations.CreateModel(
            name='StudyPublication',
            fields=[
                ('study', models.ForeignKey(db_column='STUDY_ID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='emg_api.Study')),
                ('pub', models.ForeignKey(db_column='PUB_ID', on_delete=django.db.models.deletion.CASCADE, to='emg_api.Publication')),
            ],
            options={
                'db_table': 'STUDY_PUBLICATION',
            },
        ),
        migrations.AddField(
            model_name='study',
            name='biome',
            field=models.ForeignKey(blank=True, db_column='BIOME_ID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studies', to='emg_api.Biome'),
        ),
        migrations.AddField(
            model_name='sample',
            name='biome',
            field=models.ForeignKey(blank=True, db_column='BIOME_ID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='emg_api.Biome'),
        ),
        migrations.AddField(
            model_name='sample',
            name='study',
            field=models.ForeignKey(blank=True, db_column='STUDY_ID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='emg_api.Study'),
        ),
        migrations.AddField(
            model_name='run',
            name='pipeline',
            field=models.ForeignKey(db_column='PIPELINE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='emg_api.PipelineRelease'),
        ),
        migrations.AddField(
            model_name='run',
            name='sample',
            field=models.ForeignKey(blank=True, db_column='SAMPLE_ID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='emg_api.Sample'),
        ),
        migrations.AlterUniqueTogether(
            name='pipelinerelease',
            unique_together=set([('pipeline_id', 'release_version')]),
        ),
        migrations.AddField(
            model_name='study',
            name='publications',
            field=models.ManyToManyField(related_name='studies', through='emg_api.StudyPublication', to='emg_api.Publication'),
        ),
        migrations.AlterUniqueTogether(
            name='sample',
            unique_together=set([('sample_id', 'accession')]),
        ),
        migrations.AlterUniqueTogether(
            name='study',
            unique_together=set([('study_id', 'accession')]),
        ),
        migrations.AlterUniqueTogether(
            name='pipelinereleasetool',
            unique_together=set([('pipeline', 'tool'), ('pipeline', 'tool_group_id')]),
        ),
    ]
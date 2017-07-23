#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2017 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging

# from django.utils.text import Truncator
from rest_framework.reverse import reverse

# from rest_framework import serializers
from rest_framework_json_api import serializers
from rest_framework_json_api import relations

from . import models as emg_models

logger = logging.getLogger(__name__)


class ExplicitFieldsModelSerializer(serializers.ModelSerializer):
    """
    Retrieve object with explicit fields. This is compatible with `include`
    although relationship has to be present in `fields`.
    """

    def __init__(self, *args, **kwargs):
        super(ExplicitFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class BiomeSerializer(ExplicitFieldsModelSerializer,
                      serializers.HyperlinkedModelSerializer):

    included_serializers = {}

    url = serializers.HyperlinkedIdentityField(
        view_name='emgapi:biomes-detail',
        lookup_field='lineage',
    )

    # studies = serializers.HyperlinkedIdentityField(
    #     view_name='emgapi:biomes-studies-list',
    #     lookup_field='lineage',
    # )
    # studies = relations.ResourceRelatedField(
    #     queryset=emg_models.Biome.objects,
    #     many=True,
    #     related_link_view_name='emgapi:biomes-studies-list',
    #     related_link_url_kwarg='lineage',
    # )
    studies = relations.SerializerMethodResourceRelatedField(
        source='get_studies',
        model=emg_models.Biome,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:biomes-studies-list',
        related_link_url_kwarg='lineage',
        related_link_lookup_field='lineage',
    )

    def get_studies(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    # samples = serializers.HyperlinkedIdentityField(
    #     view_name='emgapi:biomes-samples-list',
    #     lookup_field='lineage',
    # )
    # samples = relations.ResourceRelatedField(
    #     queryset=emg_models.Biome.objects,
    #     many=True,
    #     related_link_view_name='emgapi:biomes-samples-list',
    #     related_link_url_kwarg='lineage',
    # )
    samples = relations.SerializerMethodResourceRelatedField(
        source='get_samples',
        model=emg_models.Biome,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:biomes-samples-list',
        related_link_url_kwarg='lineage',
        related_link_lookup_field='lineage',
    )

    def get_samples(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    class Meta:
        model = emg_models.Biome
        fields = '__all__'


# Publication serializer

class PublicationSerializer(ExplicitFieldsModelSerializer,
                            serializers.HyperlinkedModelSerializer):

    included_serializers = {
        'studies': 'emgapi.serializers.StudySerializer',
    }

    url = serializers.HyperlinkedIdentityField(
        view_name='emgapi:publications-detail',
        lookup_field='pub_id',
    )

    # relationships
    # studies = serializers.HyperlinkedIdentityField(
    #     view_name='emgapi:publications-studies-list',
    #     lookup_field='pub_id',
    # )
    # studies = relations.ResourceRelatedField(
    #     queryset=emg_models.Publication.objects,
    #     many=True,
    #     related_link_view_name='emgapi:publications-studies-list',
    #     related_link_url_kwarg='pub_id',
    # )
    studies = relations.SerializerMethodResourceRelatedField(
        source='get_studies',
        model=emg_models.Publication,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:publications-studies-list',
        related_link_url_kwarg='pub_id',
        related_link_lookup_field='pub_id',
    )

    def get_studies(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    class Meta:
        model = emg_models.Publication
        fields = '__all__'


# Pipeline serializer

class PipelineToolSerializer(ExplicitFieldsModelSerializer,
                             serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='emgapi:tools-detail',
        lookup_field='tool_name',
    )

    pipelines = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='emgapi:pipelines-detail',
        lookup_field='release_version',
    )

    class Meta:
        model = emg_models.PipelineTool
        fields = '__all__'


class PipelineSerializer(ExplicitFieldsModelSerializer,
                         serializers.HyperlinkedModelSerializer):

    included_serializers = {
        'tools': 'emgapi.serializers.PipelineToolSerializer',
    }

    url = serializers.HyperlinkedIdentityField(
        view_name='emgapi:pipelines-detail',
        lookup_field='release_version',
    )

    # runs = relations.ResourceRelatedField(
    #     read_only=True,
    #     many=True,
    #     related_link_view_name='pipelines-runs-list',
    #     related_link_url_kwarg='release_version',
    # )
    runs = relations.SerializerMethodResourceRelatedField(
        source='get_runs',
        model=emg_models.Run,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:pipelines-runs-list',
        related_link_url_kwarg='release_version',
        related_link_lookup_field='release_version',
    )

    def get_runs(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    tools = relations.SerializerMethodResourceRelatedField(
        source='get_tools',
        model=emg_models.PipelineTool,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:pipelines-tools-list',
        related_link_url_kwarg='release_version',
        related_link_lookup_field='release_version',
    )

    def get_tools(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    class Meta:
        model = emg_models.Pipeline
        fields = '__all__'


# ExperimentType serializer

class ExperimentTypeSerializer(ExplicitFieldsModelSerializer,
                               serializers.ModelSerializer):

    included_serializers = {}

    url = serializers.HyperlinkedIdentityField(
        view_name='emgapi:experiments-detail',
        lookup_field='experiment_type',
    )

    # runs = relations.ResourceRelatedField(
    #     read_only=True,
    #     many=True,
    #     related_link_view_name='emgapi:experiments-runs-list',
    #     related_link_url_kwarg='release_version',
    # )
    runs = relations.SerializerMethodResourceRelatedField(
        source='get_runs',
        model=emg_models.Run,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:experiments-runs-list',
        related_link_url_kwarg='experiment_type',
        related_link_lookup_field='experiment_type',
    )

    def get_runs(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    class Meta:
        model = emg_models.ExperimentType
        exclude = ('experiment_type_id',)


# Run serializer

class RunHyperlinkedField(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'accession': obj.accession,
            'release_version': obj.pipeline.release_version
        }
        return reverse(
            view_name, kwargs=kwargs, request=request, format=format)


class RunSerializer(ExplicitFieldsModelSerializer,
                    serializers.HyperlinkedModelSerializer):

    included_serializers = {
        'sample': 'emgapi.serializers.SampleSerializer',
    }

    url = RunHyperlinkedField(
        view_name='emgapi:runs-detail',
        lookup_field='accession'
    )

    # attributes
    analysis_status = serializers.SerializerMethodField()

    def get_analysis_status(self, obj):
        return obj.analysis_status.analysis_status

    experiment_type = serializers.SerializerMethodField()

    def get_experiment_type(self, obj):
        return obj.experiment_type.experiment_type

    pipeline_version = serializers.SerializerMethodField()

    def get_pipeline_version(self, obj):
        return obj.pipeline.release_version

    sample_accession = serializers.SerializerMethodField()

    def get_sample_accession(self, obj):
        return obj.sample.accession

    # relationship
    pipeline = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='emgapi:pipelines-detail',
        lookup_field='release_version',
    )
    # pipeline = relations.SerializerMethodResourceRelatedField(
    #     source='get_pipeline',
    #     model=emg_models.Pipeline,
    #     read_only=True,
    #     related_link_view_name='emgapi:pipelines-detail',
    #     related_link_url_kwarg='release_version',
    #     related_link_lookup_field='release_version',
    # )
    #
    # def get_pipeline(self, obj):
    #     # TODO: provide counter instead of paginating relationship
    #     # workaround https://github.com/django-json-api
    #     # /django-rest-framework-json-api/issues/178
    #     return ()

    sample = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='emgapi:samples-detail',
        lookup_field='accession',
    )
    # sample = relations.SerializerMethodResourceRelatedField(
    #     source='get_sample',
    #     model=emg_models.Sample,
    #     read_only=True,
    #     related_link_view_name='emgapi:samples-detail',
    #     related_link_url_kwarg='accession',
    #     related_link_lookup_field='accession',
    # )
    #
    # def get_sample(self, obj):
    #     # TODO: provide counter instead of paginating relationship
    #     # workaround https://github.com/django-json-api
    #     # /django-rest-framework-json-api/issues/178
    #     return ()

    class Meta:
        model = emg_models.Run
        exclude = (
            'job_operator',
            'run_status_id',
        )


class RetrieveRunSerializer(RunSerializer):

    included_serializers = {
        'sample': 'emgapi.serializers.SampleSerializer',
    }


# SampleAnn serializer

# class SampleAnnHyperlinkedField(serializers.HyperlinkedIdentityField):
#
#     def get_url(self, obj, view_name, request, format):
#         kwargs = {
#             'name': obj.var.var_name,
#             'value': obj.var_val_ucv
#         }
#         return reverse(
#             view_name, kwargs=kwargs, request=request, format=format)


class SampleAnnSerializer(ExplicitFieldsModelSerializer,
                          serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(source="multiple_pk")

    var_name = serializers.SerializerMethodField()

    def get_var_name(self, obj):
        return obj.var.var_name

    var_value = serializers.SerializerMethodField()

    def get_var_value(self, obj):
        return obj.var_val_ucv

    unit = serializers.SerializerMethodField()

    def get_unit(self, obj):
        return obj.units

    sample_accession = serializers.SerializerMethodField()

    def get_sample_accession(self, obj):
        return obj.sample.accession

    class Meta:
        model = emg_models.SampleAnn
        fields = (
            'id',
            'sample_accession',
            'var_name',
            'var_value',
            'unit'
        )


# Sample serializer

class SampleSerializer(ExplicitFieldsModelSerializer,
                       serializers.HyperlinkedModelSerializer):

    included_serializers = {
        'study': 'emgapi.serializers.StudySerializer',
    }

    url = serializers.HyperlinkedIdentityField(
        view_name='emgapi:samples-detail',
        lookup_field='accession'
    )

    # biome = serializers.HyperlinkedRelatedField(
    #     read_only=True,
    #     view_name='emgapi:biomes-detail',
    #     lookup_field='lineage',
    # )
    biome = serializers.SerializerMethodField()

    def get_biome(self, obj):
        return obj.biome.lineage

    biome_name = serializers.SerializerMethodField()

    def get_biome_name(self, obj):
        return obj.biome.biome_name

    study_accession = serializers.SerializerMethodField()

    def get_study_accession(self, obj):
        return obj.study.accession

    # relationships
    study = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='emgapi:studies-detail',
        lookup_field='accession',
    )
    # study = relations.SerializerMethodResourceRelatedField(
    #     source='get_study',
    #     model=emg_models.Study,
    #     read_only=True,
    #     related_link_view_name='emgapi:studies-detail',
    #     related_link_url_kwarg='accession',
    #     related_link_lookup_field='accession',
    # )
    #
    # def get_study(self, obj):
    #     # TODO: provide counter instead of paginating relationship
    #     # workaround https://github.com/django-json-api
    #     # /django-rest-framework-json-api/issues/178
    #     return ()

    # runs = serializers.HyperlinkedIdentityField(
    #     view_name='emgapi:samples-runs-list',
    #     lookup_field='accession',
    # )
    runs = relations.SerializerMethodResourceRelatedField(
        source='get_runs',
        model=emg_models.Run,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:samples-runs-list',
        related_link_url_kwarg='accession',
        related_link_lookup_field='accession',
    )

    def get_runs(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    runs_count = serializers.IntegerField()

    # metadata = serializers.HyperlinkedIdentityField(
    #     view_name='emgapi:samples-metadata-list',
    #     lookup_field='accession',
    # )
    metadata = relations.SerializerMethodResourceRelatedField(
        source='get_metadata',
        model=emg_models.SampleAnn,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:samples-metadata-list',
        related_link_url_kwarg='accession',
        related_link_lookup_field='accession'
    )

    def get_metadata(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    class Meta:
        model = emg_models.Sample
        exclude = (
            'is_public',
            'submission_account_id',
        )


class RetrieveSampleSerializer(SampleSerializer):

    included_serializers = {
        'study': 'emgapi.serializers.StudySerializer',
        'runs': 'emgapi.serializers.RunSerializer',
        'metadata': 'emgapi.serializers.SampleAnnSerializer',
    }


# Study serializer

class StudySerializer(ExplicitFieldsModelSerializer,
                      serializers.HyperlinkedModelSerializer):

    included_serializers = {
        'publications': 'emgapi.serializers.PublicationSerializer',
        # 'samples': 'emgapi.serializers.SampleSerializer',
    }

    url = serializers.HyperlinkedIdentityField(
        view_name='emgapi:studies-detail',
        lookup_field='accession',
    )

    # biome = serializers.HyperlinkedRelatedField(
    #     read_only=True,
    #     view_name='emgapi:biomes-detail',
    #     lookup_field='lineage',
    # )
    biome = serializers.SerializerMethodField()

    def get_biome(self, obj):
        return obj.biome.lineage

    biome_name = serializers.SerializerMethodField()

    def get_biome_name(self, obj):
        return obj.biome.biome_name

    # relationships

    # publications = serializers.HyperlinkedIdentityField(
    #     view_name='emgapi:studies-publications-list',
    #     lookup_field='accession',
    # )
    publications = relations.SerializerMethodResourceRelatedField(
        source='get_publications',
        model=emg_models.Publication,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:studies-publications-list',
        related_link_url_kwarg='accession',
        related_link_lookup_field='accession',
    )

    def get_publications(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    # samples = serializers.HyperlinkedIdentityField(
    #     view_name='emgapi:studies-samples-list',
    #     lookup_field='accession',
    # )
    samples = relations.SerializerMethodResourceRelatedField(
        source='get_samples',
        model=emg_models.Sample,
        many=True,
        read_only=True,
        related_link_view_name='emgapi:studies-samples-list',
        related_link_url_kwarg='accession',
        related_link_lookup_field='accession',
    )

    def get_samples(self, obj):
        # TODO: provide counter instead of paginating relationship
        # workaround https://github.com/django-json-api
        # /django-rest-framework-json-api/issues/178
        return ()

    # count

    samples_count = serializers.IntegerField()

    runs_count = serializers.IntegerField()

    class Meta:
        model = emg_models.Study
        exclude = (
            'is_public',
            'submission_account_id',
            'result_directory',
        )


class RetrieveStudySerializer(StudySerializer):

    included_serializers = {
        'publications': 'emgapi.serializers.PublicationSerializer',
        # 'samples': 'emgapi.serializers.SampleSerializer',
    }
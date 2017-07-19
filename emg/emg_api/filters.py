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


import django_filters

from . import models as emg_models


class PublicationFilter(django_filters.FilterSet):

    data_origination = django_filters.CharFilter(
        name='studies__data_origination',
        distinct=True)

    class Meta:
        model = emg_models.Publication
        fields = (
            'data_origination',
        )


class StudyFilter(django_filters.FilterSet):

    biome = django_filters.CharFilter(
        name='biome__lineage',
        distinct=True)

    biome_name = django_filters.CharFilter(
        name='biome__biome_name',
        distinct=True)

    class Meta:
        model = emg_models.Study
        fields = (
            'biome',
            'biome_name',
        )


class SampleFilter(django_filters.FilterSet):

    experiment_type_id = django_filters.ModelChoiceFilter(
        queryset=emg_models.ExperimentType.objects.all(),
        distinct=True)

    experiment_type = django_filters.CharFilter(
        name='runs__experiment_type__experiment_type',
        distinct=True)

    pipeline_version = django_filters.CharFilter(
        name='runs__pipeline__release_version',
        distinct=True)

    biome = django_filters.CharFilter(
        name='biome__lineage',
        distinct=True)

    biome_name = django_filters.CharFilter(
        name='biome__biome_name',
        distinct=True)

    class Meta:
        model = emg_models.Sample
        fields = (
            'experiment_type',
            'experiment_type_id',
            'biome',
            'biome_name',
            'pipeline_version',
            'geo_loc_name',
        )


class PipelineFilter(SampleFilter):

    class Meta:
        model = emg_models.Pipeline
        fields = (
            'experiment_type',
            'experiment_type_id',
        )


class RunFilter(django_filters.FilterSet):

    analysis_status_id = django_filters.ModelChoiceFilter(
        queryset=emg_models.AnalysisStatus.objects.all(),
        distinct=True)

    experiment_type_id = django_filters.ModelChoiceFilter(
        queryset=emg_models.ExperimentType.objects.all(),
        distinct=True)

    analysis_status = django_filters.CharFilter(
        name='analysis_status__analysis_status',
        distinct=True)

    experiment_type = django_filters.CharFilter(
        name='experiment_type__experiment_type',
        distinct=True)

    pipeline_version = django_filters.CharFilter(
        name='pipeline__release_version',
        distinct=True)

    class Meta:
        model = emg_models.Run
        fields = (
            'analysis_status',
            'analysis_status_id',
            'experiment_type',
            'experiment_type_id',
            'pipeline_version',
        )

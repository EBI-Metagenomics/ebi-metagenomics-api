# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-01-14 15:01
from __future__ import unicode_literals

from django.db import migrations


def create_summary_var_names(apps, schema_editor):
    AnalysisMetadataVariableNames = apps.get_model("emgapi", "AnalysisMetadataVariableNames")
    var_names = (
        ("Nucleotide sequences with predicted SSU",
         "Number of sequences with predicted SSU rRNAs. Since pipeline version 5 we generate a file with RNA-counts."),
        ("Nucleotide sequences with predicted LSU",
         "Number of sequences with predicted LSU rRNAs. Since pipeline version 5 we generate a file with RNA-counts.")
    )
    _var_names = list()
    for var_name in var_names:
        _var_names.append(
            AnalysisMetadataVariableNames(
                var_name=var_name[0],
                description=var_name[1]
            )
        )
    AnalysisMetadataVariableNames.objects.bulk_create(_var_names)


class Migration(migrations.Migration):
    dependencies = [
        ('emgapi', '0019_auto_20200110_1455'),
    ]

    operations = [
        migrations.RunPython(create_summary_var_names),
    ]

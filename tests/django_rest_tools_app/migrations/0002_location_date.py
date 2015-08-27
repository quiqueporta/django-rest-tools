# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rest_tools_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
    ]

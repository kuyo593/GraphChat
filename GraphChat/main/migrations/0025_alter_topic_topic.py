# Generated by Django 3.2.7 on 2021-10-02 20:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='topic',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None),
        ),
    ]

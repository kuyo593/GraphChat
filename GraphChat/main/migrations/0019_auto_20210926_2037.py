# Generated by Django 3.2.7 on 2021-09-26 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_userimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='talk_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='talk_from', to='main.user'),
        ),
        migrations.AlterField(
            model_name='talk',
            name='talk_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='talk_to', to='main.user'),
        ),
    ]

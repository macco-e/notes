# Generated by Django 2.2.5 on 2019-09-30 15:17

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_auto_20190930_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='noted_tables',
            field=django_mysql.models.ListCharField(models.CharField(blank=True, max_length=16, null=True), blank=True, max_length=901, size=52),
        ),
    ]
# Generated by Django 2.2.5 on 2019-10-02 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_auto_20191002_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='icon',
            field=models.ImageField(blank=True, default='', upload_to='icons'),
        ),
    ]
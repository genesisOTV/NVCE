# Generated by Django 2.1.1 on 2018-10-07 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_source_names'),
    ]

    operations = [
        migrations.RenameField(
            model_name='source',
            old_name='names',
            new_name='name',
        ),
    ]
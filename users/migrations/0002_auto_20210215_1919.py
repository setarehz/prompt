# Generated by Django 2.2.9 on 2021-02-15 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serviceprovider',
            old_name='name',
            new_name='company_name',
        ),
    ]

# Generated by Django 4.1.3 on 2022-11-21 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_servicemodel_county_servicemodel_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicemodel',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
# Generated by Django 2.2.5 on 2020-07-18 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tax',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='uom',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 2.2.5 on 2020-07-31 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='damgedstock',
            name='dmgponum',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='invponum',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
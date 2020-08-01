# Generated by Django 2.2.5 on 2020-08-01 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master', '0002_auto_20200718_1913'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_auto_20200724_1249'),
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Po',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ponum', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('shipto', models.CharField(max_length=200)),
                ('shipcity', models.CharField(max_length=50)),
                ('shipstate', models.CharField(max_length=50)),
                ('shippincode', models.CharField(max_length=10)),
                ('poreqbydate', models.DateTimeField()),
                ('creation_date', models.DateTimeField()),
                ('createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pocreated', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendordetails', to='vendor.Vendor')),
            ],
        ),
        migrations.CreateModel(
            name='potracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_num', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
                ('tax', models.FloatField()),
                ('disc', models.FloatField()),
                ('pototal', models.FloatField()),
                ('podetail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='po.Po')),
            ],
        ),
        migrations.CreateModel(
            name='poItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ponum', models.CharField(max_length=30)),
                ('qty', models.FloatField()),
                ('subtotal', models.FloatField()),
                ('po_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='products.Products')),
                ('podetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='po', to='po.Po')),
                ('uom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pouom', to='master.UOM')),
            ],
        ),
    ]

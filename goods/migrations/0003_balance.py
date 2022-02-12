# Generated by Django 4.0.2 on 2022-02-07 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_barcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.good')),
            ],
        ),
    ]
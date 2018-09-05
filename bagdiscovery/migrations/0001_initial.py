# Generated by Django 2.0 on 2018-08-20 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('bag', models.CharField(blank=True, max_length=4500, null=True)),
                ('date', models.CharField(blank=True, max_length=400, null=True)),
                ('time', models.CharField(blank=True, max_length=4500, null=True)),
            ],
            options={
                'db_table': 'bag',
                'managed': True,
            },
        ),
    ]
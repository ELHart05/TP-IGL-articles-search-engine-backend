# Generated by Django 5.0 on 2023-12-31 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elasticsearchApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='search',
            field=models.IntegerField(default=0),
        ),
    ]

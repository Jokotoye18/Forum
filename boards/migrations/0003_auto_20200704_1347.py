# Generated by Django 3.0.8 on 2020-07-04 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20200703_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='topic',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]

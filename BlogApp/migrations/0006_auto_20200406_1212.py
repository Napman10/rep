# Generated by Django 3.0.3 on 2020-04-06 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0005_auto_20200406_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

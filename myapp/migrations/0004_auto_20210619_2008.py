# Generated by Django 3.2.4 on 2021-06-19 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210619_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='member2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='member3',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='member4',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='member5',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

# Generated by Django 3.2.4 on 2021-06-19 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_document_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='mentor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='myapp.mentor'),
        ),
    ]

# Generated by Django 3.2.4 on 2021-06-19 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_team_mentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='final_submission',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='phase',
            field=models.CharField(choices=[('1', 'Identify'), ('2', 'Investigate'), ('3', 'Ideate'), ('4', 'Implement'), ('5', 'Inform'), ('6', 'Completed')], default='1', max_length=1),
        ),
    ]
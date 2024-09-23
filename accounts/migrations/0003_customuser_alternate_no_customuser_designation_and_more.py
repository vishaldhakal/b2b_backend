# Generated by Django 5.1.1 on 2024-09-23 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_organization_files_remove_organization_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='alternate_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='designation',
            field=models.CharField(choices=[('CEO', 'Chief Executive Officer'), ('CFO', 'Chief Financial Officer'), ('CTO', 'Chief Technology Officer'), ('CMO', 'Chief Marketing Officer'), ('COO', 'Chief Operating Officer'), ('CIO', 'Chief Information Officer'), ('CSO', 'Chief Security Officer'), ('Other', 'Other')], default='Other', max_length=100),
        ),
        migrations.AddField(
            model_name='organization',
            name='country',
            field=models.CharField(default='Nepal', max_length=100),
        ),
        migrations.AddField(
            model_name='organization',
            name='municipality_ward',
            field=models.CharField(default='Biratnagar', max_length=100),
        ),
        migrations.AddField(
            model_name='organization',
            name='province_state',
            field=models.CharField(default='Province 1', max_length=100),
        ),
        migrations.AlterField(
            model_name='file',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='accounts.organization'),
        ),
    ]

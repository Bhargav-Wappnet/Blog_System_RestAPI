# Generated by Django 4.1.7 on 2023-03-22 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
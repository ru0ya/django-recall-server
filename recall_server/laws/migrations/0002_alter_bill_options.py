# Generated by Django 5.0.6 on 2024-09-10 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("laws", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bill",
            options={"ordering": ["deadline_for_voting"]},
        ),
    ]
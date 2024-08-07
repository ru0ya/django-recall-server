# Generated by Django 5.0.6 on 2024-06-26 16:33

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mps", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="memberofparliament",
            options={"ordering": ("-updated_at", "-created_at")},
        ),
        migrations.RemoveField(
            model_name="memberofparliament",
            name="id",
        ),
        migrations.AddField(
            model_name="memberofparliament",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="memberofparliament",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="memberofparliament",
            name="tokenized_id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-28 15:12

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recall_reasons', models.TextField()),
                ('tokenized_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('recall_supporters', models.ManyToManyField(blank=True, related_name='supported_recalls', to=settings.AUTH_USER_MODEL)),
                ('recalled', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recalls', to=settings.AUTH_USER_MODEL)),
                ('recaller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_recalls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

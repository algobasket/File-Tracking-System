# Generated by Django 4.2.11 on 2024-05-22 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fts_app", "0005_message_is_forwarded_message_is_opened_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userdetail",
            name="phone",
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]

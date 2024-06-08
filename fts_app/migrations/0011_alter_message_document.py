# Generated by Django 4.2.11 on 2024-06-01 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fts_app", "0010_alter_correspondenceusermap_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="document",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="fts_app.storedocument",
            ),
            preserve_default=False,
        ),
    ]
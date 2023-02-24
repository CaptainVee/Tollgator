# Generated by Django 4.1.2 on 2023-02-23 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instructor", "0002_alter_bankaccount_account_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="instructor",
            name="accept_terms_and_conditions",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="instructor",
            name="experience",
            field=models.CharField(default="cow", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="instructor",
            name="skills",
            field=models.CharField(default="1 year", max_length=100),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.2 on 2023-02-23 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instructor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankaccount",
            name="account_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="bankaccount",
            name="account_number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="bankaccount",
            name="country",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

# Generated by Django 4.1.2 on 2023-02-17 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0016_user_currency"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="instructor",
            name="user",
        ),
        migrations.RemoveField(
            model_name="withdraw",
            name="instructor",
        ),
        migrations.DeleteModel(
            name="BankAccount",
        ),
        migrations.DeleteModel(
            name="Instructor",
        ),
        migrations.DeleteModel(
            name="Withdraw",
        ),
    ]

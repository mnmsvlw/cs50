# Generated by Django 4.1.1 on 2022-09-20 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
    ]

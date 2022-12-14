# Generated by Django 4.1.1 on 2022-09-19 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positionwatch', to='auctions.item')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watcher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

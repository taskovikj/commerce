# Generated by Django 4.2.3 on 2023-07-27 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listings',
            field=models.ManyToManyField(related_name='watchlist_listings', to='auctions.listing'),
        ),
    ]
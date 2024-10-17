# Generated by Django 5.0.7 on 2024-10-14 01:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_bids_comments_itemtype_auctionlisting"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlisting",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="watchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
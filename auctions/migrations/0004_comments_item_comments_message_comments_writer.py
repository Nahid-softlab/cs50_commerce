# Generated by Django 5.0.7 on 2024-10-14 02:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_auctionlisting_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="comments",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="itemofcmt",
                to="auctions.auctionlisting",
            ),
        ),
        migrations.AddField(
            model_name="comments",
            name="message",
            field=models.CharField(default="You didn't wrote anything", max_length=300),
        ),
        migrations.AddField(
            model_name="comments",
            name="writer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

# Generated by Django 5.0.7 on 2024-10-14 15:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_alter_bids_bid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bids",
            name="bid",
        ),
        migrations.RemoveField(
            model_name="bids",
            name="userbidding",
        ),
        migrations.AlterField(
            model_name="auctionlisting",
            name="price",
            field=models.IntegerField(default=0),
        ),
    ]

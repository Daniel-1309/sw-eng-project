# Generated by Django 3.2.13 on 2023-05-31 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_menu_item_list_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bill_clear',
            field=models.BooleanField(default=False),
        ),
    ]

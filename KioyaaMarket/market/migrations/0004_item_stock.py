# Generated by Django 5.1.2 on 2024-10-28 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_alter_client_shoppinglist'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.IntegerField(default=500),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.3 on 2023-05-15 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0007_remove_sales_seller_alter_sales_sales_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='imageurl',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
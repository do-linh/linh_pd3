# Generated by Django 3.2.15 on 2022-08-28 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='paypal_checkout',
            new_name='paypal_order',
        ),
    ]
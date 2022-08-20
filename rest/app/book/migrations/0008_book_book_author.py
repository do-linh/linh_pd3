# Generated by Django 3.2.15 on 2022-08-20 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_author'),
        ('book', '0007_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.author'),
        ),
    ]
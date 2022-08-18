# Generated by Django 3.2.15 on 2022-08-15 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_alter_userprofile_role'),
        ('book', '0003_userfavoritelist'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('books', models.ManyToManyField(blank=True, null=True, to='book.Book')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.userprofile')),
            ],
        ),
    ]

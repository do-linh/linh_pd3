# Generated by Django 3.2.15 on 2022-08-18 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_alter_userprofile_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('author_name', models.CharField(max_length=255)),
                ('author_avatar', models.ImageField(blank=True, null=True, upload_to='author/')),
                ('author_description', models.TextField(blank=True, null=True)),
                ('author_dob', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]

# Generated by Django 4.1.6 on 2023-04-13 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_author_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name'], 'permissions': (('can_change_author', 'change author'), ('can_add_book', 'Can add book'))},
        ),
    ]

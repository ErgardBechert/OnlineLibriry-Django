# Generated by Django 4.1.6 on 2023-04-12 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_author_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name'], 'permissions': (('can_mark_returned', 'can_edit'),)},
        ),
    ]
# Generated by Django 4.1.6 on 2023-04-12 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name'], 'permissions': (('can_mark_returned', 'change author'),)},
        ),
    ]
# Generated by Django 4.1.6 on 2023-04-13 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='Books'),
        ),
    ]

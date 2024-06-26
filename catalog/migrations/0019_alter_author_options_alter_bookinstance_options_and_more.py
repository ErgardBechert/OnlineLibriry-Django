# Generated by Django 5.0.6 on 2024-06-16 18:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_alter_book_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name'], 'permissions': (('can_change_author', 'Изменение автора'),)},
        ),
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', "Установка статуса 'Возвращена'"),)},
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, help_text='Дата рождения', null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, help_text='Дата смерти', null=True, verbose_name='Умер'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Выберите жанры для этой книги', to='catalog.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(help_text='13-значный номер <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>', max_length=13, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(help_text='Введите краткое описание книги', max_length=1000),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='due_back',
            field=models.DateField(blank=True, help_text='Дата возврата', null=True),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Уникальный идентификатор для данной книги в библиотеке', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'Обслуживание'), ('o', 'Выдана'), ('a', 'Доступна'), ('r', 'Зарезервирована')], default='m', help_text='Доступность книги', max_length=1),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Введите жанр книги (например, Научная фантастика, Французская поэзия и т.д.)', max_length=200),
        ),
    ]

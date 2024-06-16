from django.urls import reverse # Используется для генерации URL путем разворачивания URL-шаблонов
from django.db import models
from django.contrib.auth.models import User
from datetime import date
import uuid # Необходим для уникальных экземпляров книг

class Genre(models.Model):
    """
    Модель, представляющая жанр книги (например, Научная фантастика, Нон-фикшн).
    """
    name = models.CharField(max_length=200, help_text="Введите жанр книги (например, Научная фантастика, Французская поэзия и т.д.)")

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к определенному экземпляру жанра.
        """
        return reverse('genre_list')

    def __str__(self):
        """
        Строка для представления объекта модели (в админке и т.д.)
        """
        return self.name

class Book(models.Model):
    """
    Модель, представляющая книгу (но не конкретный экземпляр книги).
    """
    image = models.ImageField(null=True, blank=True,default='default.jpg', upload_to='Books')
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN',max_length=13, help_text='13-значный номер <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанры для этой книги")

    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к определенному экземпляру книги.
        """
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """
        Создает строку для жанра. Необходимо для отображения жанра в админке.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Жанр'
    
class BookInstance(models.Model):
    """
    Модель, представляющая конкретный экземпляр книги (т.е. который можно взять в библиотеке).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный идентификатор для данной книги в библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True, help_text="Дата возврата")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Обслуживание'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'Зарезервирована'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Установка статуса 'Возвращена'"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к определенному экземпляру книги.
        """
        return reverse('book_instance_create')

    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return '%s (%s)' % (self.id,self.book.title)

class Author(models.Model):
    """
    Модель, представляющая автора.
    """
    image = models.ImageField(null=True, blank=True,default='default.jpg', upload_to='Authors')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True, help_text="Дата рождения")
    date_of_death = models.DateField('Умер', null=True, blank=True, help_text="Дата смерти")
    about_the_author = models.TextField(max_length=1000)

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к определенному экземпляру автора.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return '%s, %s' % (self.last_name, self.first_name)
    
    class Meta:
        ordering = ['last_name']
        permissions = (
                ("can_change_author", "Изменение автора"),
        )

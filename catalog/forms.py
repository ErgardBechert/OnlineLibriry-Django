
import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import BookInstance
from .models import Book
from .models import Author
from .models import Genre

class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'image': 'Изображение',
            'title': 'Название',
            'author': 'Автор',
            'summary': 'Аннотация',
            'isbn': 'ISBN',
            'genre': 'Жанр',
        }

class AuthorCreateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'  # Используйте '__all__' для указания всех полей модели
        labels = {
            'image': 'Аватар автора',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'date_of_birth': 'Дата рождения',
            'date_of_death': 'Дата смерти',
            'about_the_author': 'Об авторе',
        }

class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['image', 'first_name', 'last_name', 'date_of_birth', 'date_of_death', 'about_the_author']
        labels = {
            'image': 'Аватар автора',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'date_of_birth': 'Дата рождения',
            'date_of_death': 'Дата смерти',
            'about_the_author': 'О авторе',
        }

class BookInstanceCreateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = '__all__'
        labels = {
            'book': 'Книга',
            'imprint': 'Версия',
            'due_back': 'Возврат до',
            'status': 'Статус',
            'borrower': 'Заёмщик',
        }
        widgets = {
            'due_back': forms.DateInput(attrs={'type': 'date'}),
        }

class GenreCreateForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        labels = {
            'name': 'Название жанра',
        }


class RenewBookForm(forms.ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if not data:
            raise ValidationError(_('Это поле обязательно к заполнению'))
        try:
            datetime.datetime.strptime(str(data), '%Y-%m-%d')
        except ValueError:
            raise ValidationError(_('Неверный формат даты'))
        
        # Проверка того, что дата не в прошлом
        if data < datetime.date.today():
            raise ValidationError(_('Неверная дата - продление в прошлом'))

        # Проверка, что дата в диапазоне, который разрешен библиотекарю для изменения (сохранения +4 недели)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Неверная дата - продление более чем на 4 недели вперед'))

        # Не забывайте всегда возвращать очищенные данные
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back',]
        labels = { 'due_back': _('Renewal date'), }
        help_texts = { 'due_back': _('Enter a date between now and 4 weeks (default 3).'), }

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Melta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets= {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),

        }
            
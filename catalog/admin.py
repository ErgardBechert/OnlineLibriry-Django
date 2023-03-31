from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Register your models here.

# Define the admin class
class BookInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin): # ModelAdmin (он описывает расположение элементов интерфейса, где Model - наименование модели) 
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')  #list_display (для добавления дополнительных полей).
    fields = ['image','first_name', 'last_name', ('date_of_birth', 'date_of_death'), 'about_the_author'] # Поля отображаются по вертикали по умолчанию, но будут отображаться горизонтально, если вы дополнительно группируете их в кортеже 
    
    inlines = [BookInline]
# Register the admin class with the associated model

admin.site.register(Author, AuthorAdmin)

# Register the Admin classes for Book using the decorator  # декоратор @register (он делает то же самое, что и метод admin.site.register()):
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status', 'due_back', 'id')

    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

# Каждая секция имеет свой заголовок (или None, если заголовок не нужен) 
# и ассоциированный кортеж полей в словаре - формат сложный для описания, но относительно простой для понимания, 
# если вы посмотрите на фрагмент кода, представленный выше.

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
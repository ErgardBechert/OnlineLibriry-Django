from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_books_word = Book.objects.filter(title__icontains='Убить').count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books_word': num_books_word,'num_genres': num_genres,'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )

from django.views import generic

class BookListView(generic.ListView):
    model = Book

    paginate_by = 7

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context
    
class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_librarian'] = self.request.user.groups.filter(name='Библиотекари').exists()
        return context

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_librarian'] = self.request.user.groups.filter(name='Библиотекари').exists()
        return context

class ProfileView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/profile.html'


    def get_queryset(self):
        if self.request.user.groups.filter(name='Библиотекари').exists():
        # Если пользователь принадлежит к группе 'Библиотекари', то
        # отображаем все зарезервированные книги
            return BookInstance.objects.filter(status__exact='o').order_by('due_back')
        else:
        # Если пользователь не принадлежит к группе 'Библиотекари', то
        # отображаем только зарезервированные книги текущего пользователя
            return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_librarian'] = self.request.user.groups.filter(name='Библиотекари').exists()
        return context

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm, RegisterUserForm

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('profile') )

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

def borrow_book(request, pk):
    copy = get_object_or_404(BookInstance,  pk=pk)

    if request.method == 'POST':
        copy.status = 'o'
        copy.borrower = request.user  # сохраняем пользователя
        copy.save()
        return HttpResponseRedirect(reverse('book-detail', args=[copy.book.pk]))

    return render(request, 'catalog/borrow_book.html', {'copy': copy})


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

from django.contrib.auth.mixins import PermissionRequiredMixin

class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': 'xx.xx.xxxx'}
    permission_required = 'catalog.can_change_author'

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['image', 'first_name','last_name','date_of_birth','date_of_death', 'about_the_author']
    permission_required = 'catalog.can_change_author'

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_change_author'

class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_change_author'

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['image','title','author','summary','isbn', 'genre']
    permission_required = 'catalog.can_change_author'

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_change_author'

class BookInstanceCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = '__all__'
    permission_required = 'catalog.can_change_author'

class GenreCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Genre
    fields = '__all__'
    permission_required = 'catalog.can_change_author'

class GenreListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Genre
    permission_required = 'catalog.can_change_author'

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # чтобы обойти проверку CSRF-токена во время разработки и настроили обработчик POST-запроса на удаление жанра из бд

@csrf_exempt
def delete_genre(request):
    if request.method == 'POST':
        genre_id = request.POST.get('genre_id')
        genre = Genre.objects.get(pk=genre_id)
        genre.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

   
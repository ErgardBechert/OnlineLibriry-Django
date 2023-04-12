from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'), #books/ (^ является маркером начала строки, а $ - маркер конца строки). Как было отмечено в предыдущей части руководства, URL-адрес уже должен содержать /catalog, таким образом полный адрес, на самом деле, имеет вид : /catalog/books/.
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'), #book/, за которым до конца строки (до маркера конца строки - $) следуют одна, или более цифр. В процессе выполнения данного преобразования, оно "захватывает" цифры и передаёт их в функцию отображения как параметр с именем pk.
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
] 

urlpatterns += [
    re_path(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    re_path(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    re_path(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]
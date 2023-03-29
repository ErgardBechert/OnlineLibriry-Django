from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'), #books/ (^ является маркером начала строки, а $ - маркер конца строки). Как было отмечено в предыдущей части руководства, URL-адрес уже должен содержать /catalog, таким образом полный адрес, на самом деле, имеет вид : /catalog/books/.
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'), #book/, за которым до конца строки (до маркера конца строки - $) следуют одна, или более цифр. В процессе выполнения данного преобразования, оно "захватывает" цифры и передаёт их в функцию отображения как параметр с именем pk.
] 

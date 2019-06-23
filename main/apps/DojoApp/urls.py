from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root), # /
    url(r'^debug$', views.debug), # /debug

    url(r'^books$', views.books),
    url(r'^books/add$', views.addBook),
    url(r'^books/new$', views.newBook),
    url(r'^books/(?P<book_id>\d+)$', views.showBook),

    url(r'^post_review$', views.post_review),

    # Register and Login
    url(r'^users/reg_login', views.reg_login),
    url(r'^users/reg', views.register),
    url(r'^users/userLogin', views.userLogin),
    url(r'^users/logout', views.logout),
    # url(r'^users/adminLogin', views.adminLogin),
]

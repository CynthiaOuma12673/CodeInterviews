from django.urls.conf import path
from . import views

urlpatterns=[
    path('',views.index,name='home'),
    path('quiz/',views.quiz,name='quiz'),
    path('new_quiz/', views.new_quiz, name='new_quiz'),
    path('profile/<username>/', views.profile, name='profile'),
    path('my_quiz/<id>', views.user, name='my_quiz'),
    path('search/', views.search_quiz, name='search'),
]
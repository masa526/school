from django.urls import path
from lesson import views

app_name = 'lesson'
urlpatterns = [
    path('', views.lesson_list, name='lesson_list'),
    path('add/', views.lesson_edit, name='lesson_add'),
    path('mod/<int:lesson_id>/', views.lesson_edit, name='lesson_mod'),
]

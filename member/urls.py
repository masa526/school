from django.urls import path
from member import views

app_name = 'member'
urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('add/', views.member_edit, name='member_add'),
    path('mod/<int:member_id>/', views.member_edit, name='member_mod'),
]

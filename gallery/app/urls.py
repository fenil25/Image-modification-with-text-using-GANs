from django.urls import include, path
from app import views

urlpatterns = [
	path('', views.list),
	path('list/', views.list, name = 'list')
]
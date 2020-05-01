from django.urls import include, path
from app import views

urlpatterns = [
	path('', views.list),
	path('list/<dataset>/', views.list, name = 'list')
]
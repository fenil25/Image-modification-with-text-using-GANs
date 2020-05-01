from django.urls import include, path
from app import views

urlpatterns = [
	path('', views.list),
	path('new/', views.transform, name = 'transform'),
	path('list/<dataset>/', views.list, name = 'list')
]
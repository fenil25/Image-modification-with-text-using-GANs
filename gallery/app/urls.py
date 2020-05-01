from django.urls import include, path
from app import views

urlpatterns = [
	path('', views.list),
	path('new/<int:id>/<side>/', views.transform_old, name = 'transform_old'),
	path('new/', views.transform, name = 'transform'),
	path('list/<dataset>/', views.list, name = 'list')
]
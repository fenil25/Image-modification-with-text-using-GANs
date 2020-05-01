from django.urls import include, path
from gallery.app import views

urlpatterns = [
	path('', views.list),
	path('list/', views.list)
]
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Movies import views

urlpatterns = [
    path('basic/', views.Movies.as_view()),
    path('basic/add/', views.MoviesCreateView.as_view()),
    path('basic/<int:id>/destroy', views.Movies_details.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
from django.urls import path
from . import views

urlpatterns = [
  path('', views.submit_google_sheet, name='ListingPrograms'),
#  path('submit/', views.submit_google_sheet, name='submit'),
#  path('modules/', views.listeModules, name='modules'),
#  path('exercices_module/', views.function_two, name='exercices_module'),
  path('exercice/', views.doExercice, name='exercice'),
]
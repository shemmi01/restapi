from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('excel/',ExportImportExcel.as_view()),
    #path('generic-student', StudentGeneric.as_view()),

    path('student/', StudentAPI.as_view()),
    #path('get-book', get_book),
    path('register/',RegisterUser.as_view()),
]
    
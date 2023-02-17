from django.urls import path
from olympbot import views

urlpatterns = [
    path('subjects/<int:user_id>', views.show_subjects),
    path('olympiads/<int:user_id>', views.show_olympiads)
]

from django.urls import path
from feedback_form import views

urlpatterns = [
    path('', views.create_feedback, name='create_feedback'),
]

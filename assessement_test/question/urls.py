from django.urls import path

from . import views

urlpatterns = [
    path("", views.QuestionListAPIView.as_view()),
    path("create/", views.QuestionCreateAPIView.as_view()),
    path("<uuid:id>/", views.QuestionDetailAPIView.as_view()),
    path("choice/<uuid:id>/", views.ChoiceDetailAPIView.as_view()),
    path("choice-create/<uuid:questionId>/", views.ChoiceCreateAPIView.as_view())
]

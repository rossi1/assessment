from django.urls import path, include



urlpatterns = [
    path("question/", include("assessement_test.question.urls"))
]

import os
from collections import OrderedDict

import pandas as df

from django.http import JsonResponse

from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Question, Choices
from .serializers import QuestionSerializer, ExcelSheetSerializer, ChoicesSerializer, QuestionResponseSerializer

class QuestionCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Question
    serializer_class = ExcelSheetSerializer

    @swagger_auto_schema(
        responses={
            '200': QuestionResponseSerializer,
            '400': ExcelSheetSerializer,
        },
        request_body=ExcelSheetSerializer
    )
    def post(self, request, *args, **kwargs):
        return super(QuestionCreateAPIView, self).post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = serializer.validated_data['files']
            if os.path.splitext(data.name)[-1] == ".xlsx":
                read_file = df.read_excel(data, sheet_name='Top Brain')
            else:
                read_file = df.read_csv(data)
            question = read_file['question']
            is_general = read_file['is_general']
            categories = read_file['categories']
            point = read_file['point']
            icon_url = read_file['icon_url']
            duration = read_file['duration']
            choice_1 = read_file['choice_1']
            is_correct_choice_1 = read_file['is_correct_choice_1']
            icon_url_1 = read_file['icon_url_1']
            choice_2 = read_file["Choice_2"]
            is_correct_choice_2 = read_file['is_correct_choice_2']
            icon_url_2 = read_file['icon_url_2']
            choice_3 = read_file["Choice_3"]
            is_correct_choice_3 = read_file['is_correct_choice_3']
            icon_url_3 = read_file['icon_url_3']
            choice_4 = read_file["Choice_4"]
            is_correct_choice_4 = read_file['is_correct_choice_4']
            icon_url_4 = read_file['icon_url_4']
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            index_list = zip(question, is_general, categories, point, icon_url, duration,
            choice_1, is_correct_choice_1, icon_url_1, choice_2, is_correct_choice_2, icon_url_2,
            choice_3, is_correct_choice_3, icon_url_3, choice_4, is_correct_choice_4, icon_url_4
            )
            failed = list()
            success = list()

            amount_saved = 0
            amount_not_saved = 0

            for question, is_general, category, point, icon_url, duration, \
                choice_1, is_correct_choice_1, icon_url_1, choice_2, is_correct_choice_2, icon_url_2, \
                    choice_3, is_correct_choice_3, icon_url_3, choice_4, is_correct_choice_4, icon_url_4 in index_list:
                    request_data = {
                        "question": question, "is_general": is_general, "categories": category,
                        "point": None if df.isna(point) else point, "icon_url": None if df.isna(icon_url) else icon_url,
                        "duration": None if df.isna(duration) else duration,
                        "choices": [
                            {"choice": choice_1, "is_correct_choice": is_correct_choice_1, "is_icon_url": None if df.isna(icon_url_1) else icon_url_1},
                            {"choice": choice_2, "is_correct_choice": is_correct_choice_2, "is_icon_url": None if df.isna(icon_url_2) else icon_url_2},
                            {"choice": choice_3, "is_correct_choice": is_correct_choice_3, "is_icon_url": None if df.isna(icon_url_3) else icon_url_3},
                            {"choice": choice_4, "is_correct_choice": is_correct_choice_4, "is_icon_url": None if df.isna(icon_url_4) else icon_url_4},
                        ]
                    }
                    question_serializer = QuestionSerializer(data=request_data, context={"request": request})
                    if not question_serializer.is_valid():
                        amount_not_saved += 1
                        failed.append(question_serializer.errors)
                    else:
                        question_serializer.save()
                        amount_saved += 1
                        success.append(question_serializer.data)
            response_data = {"total_saved": amount_saved, "total_not_saved": amount_not_saved, "errors": failed, "sucess": success}
            return Response(response_data, status=status.HTTP_200_OK)


class QuestionListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = ('categories',)


class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Question
    serializer_class = QuestionSerializer
    lookup_url_kwarg = 'id'


class ChoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Choices
    serializer_class = ChoicesSerializer
    lookup_url_kwarg = 'id'

param = openapi.Parameter('questionId', openapi.IN_PATH, type=openapi.TYPE_STRING)

class ChoiceCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Choices
    serializer_class = ChoicesSerializer

    @swagger_auto_schema(
        responses={
            '200': ChoicesSerializer,
            '400': ChoicesSerializer
        },
        manual_parameters=[param]

    )
    def post(self, request, *args, **kwargs):
        return super(ChoiceCreateAPIView, self).post(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request, "question_id": self.kwargs.get("questionId", None)}


def server_error(request, *args, **kwargs):
    """
    Generic 500 error handler.
    """
    data = {
        'error': 'internal server error'
    }
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def not_found_request(request, exception, *args, **kwargs):
    """
    Generic 400 error handler.
    """
    data = {
        'error': 'endpoint does not exist'
    }
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)

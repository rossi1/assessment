import os

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Question, Choices


class ExcelSheetSerializer(serializers.Serializer):
    files = serializers.FileField(required=True)

    def validate_files(self, instance):
        if instance.size > 5*1024*1024:
            raise serializers.ValidationError("file too large ( > 5mb )")

        if not os.path.splitext(instance.name)[-1] in [".csv",".xlsx"]:
            raise serializers.ValidationError("file Doesn't have proper extension")

        return instance


class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = "__all__"
        extra_kwargs = {'question': {'read_only': True}}

    def create(self, validated_data):
        try:
            question = Question.objects.get(id=self.context["question_id"])
        except Question.DoesNotExist:
            raise serializers.ValidationError(_("question does not exist"))
        else:
            choice = Choices.objects.create(question=question, **validated_data)
            return choice

  

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(many=True, required=False)

    class Meta:
        model = Question
        exclude = ("date_created",)


    def create(self, validated_data):
        choices = validated_data.pop("choices", None)
        question = Question.objects.create(**validated_data)
        if choices is None:
            raise serializers.ValidationError(_("choices cannot be null"))

        for choice in choices:
            Choices.objects.create(question=question, **choice)
        return question


    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.is_general = validated_data.get('is_general', instance.is_general)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.point = validated_data.get('point', instance.point)
        instance.icon_url = validated_data.get('icon_url', instance.icon_url)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.save()
        choices = validated_data.get('choices', None)
        if choices is not None:
            for choice in choices:
                try:
                    choice = Choices.objects.get(question=instance, id=choice.get('id'))
                    choice.choice = choices.get('choice', choice.choice)
                    choice.is_correct_choice = choices.get('is_correct_choice', choice.is_correct_choice)
                    choice.is_icon_url = choices.get('is_icon_url', choice.is_icon_url)
                except Choices.DoesNotExist:
                    pass
        return instance


class QuestionResponseSerializer(serializers.Serializer):
    total_saved = serializers.IntegerField()
    total_not_saved = serializers.IntegerField()
    errors = serializers.ListSerializer(child=QuestionSerializer())
    success = serializers.ListSerializer(child=QuestionSerializer())

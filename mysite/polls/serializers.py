from rest_framework import serializers
from . models import Question, Choice

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', )



class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("choice_text", "votes", "question")


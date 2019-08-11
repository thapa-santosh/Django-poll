from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_question(question_text="", pub_date=""):
        if question_text != "" and pub_date != "":
            Question.objects.create(question_text=question_text, pub_date=pub_date)


    def setUp(self):
        # add test data
        self.create_question("which is the best programming language?", "Python, R, C, JAVA")
        self.create_question("which is the best novel of 2019?", "Machines like me, The Editor, Spring, Life will be death of me")
        self.create_question("love is wicked", "brick and lace")
        self.create_question("who will win the champions league 2019?", "Tottenham Hotspurs, Liverpool FC")

    @staticmethod
    def create_choice(choice_text="", votes="", question=""):
        if choice_text != "" and votes != "" and question != "":
            Choice.objects.create(choice_text=choice_text, votes=votes, question=question)

    def setUp(self):
        # add test data
        self.create_choice("which is the best programming language?", "Python, R, C, JAVA")
        self.create_choice("which is the best novel of 2019?", "Machines like me, The Editor, Spring, Life will be death of me")
        self.create_choice("love is wicked", "brick and lace")
        self.create_choice("who will win the champions league 2019?", "Tottenham Hotspurs, Liverpool FC")


class GetAllQuestionTest(BaseViewTest):

    def test_get_all_question(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("question-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Question.objects.all()
        serialized = QuestionSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllChoiceTest(BaseViewTest):
    def test_get_all_choice(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("choice-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Choice.objects.all()
        serialized = ChoiceSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
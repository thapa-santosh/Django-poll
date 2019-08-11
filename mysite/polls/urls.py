
from django.urls import path
from .import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListQuestionView, ListChoiceView

app_name = 'polls'
urlpatterns = [

    path('', views.index, name='index'),

    path('index', views.index, name='index'),

    path('<int:question_id>/', views.detail, name='detail'),

    path('<int:question_id>/results/', views.results, name='results'),

    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('Question/', ListQuestionView.as_view(), name="Question-all"),

    path('Choice/', ListChoiceView.as_view(), name="Choice-all"),
]

urlpatterns = format_suffix_patterns(urlpatterns)


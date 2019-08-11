from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics
from .serializers import QuestionSerializer, ChoiceSerializer
from  .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Question, Choice
from django.template import loader, RequestContext
# Create your views here.

def index(request):

    latest_questions = Question.objects.order_by('pub_date')[:5]
    template = loader.get_template(('polls/index.html'))
    context = {
        'latest_questions': latest_questions,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except:
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "please select a choice", })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


class ListQuestionView(generics.ListAPIView):
    """
    proovides a get method handler
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ListChoiceView(generics.ListAPIView):
    """
    proovides a get method handler
    """

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'polls/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'polls/login.html', {})


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Questions
from django.http import FileResponse
import datetime
import time
from .models import UserProfile, Questions, Submission
from django.contrib.auth.models import User, auth



def index(request):
    return render(request, 'ctf/index.html')

def tools(request):
    return render(request, 'ctf/tools.html')

def game(request):
    return render(request, 'ctf/game.html')

def error(request):
    return render(request, 'ctf/404.html')


def about(request):
    return render(request, 'ctf/about.html')


@login_required(login_url='/login')  # This decorator ensures that the user is logged in, otherwise redirects to the specified URL
def inst(request):
    return render(request, 'ctf/instructions.html')


from django.shortcuts import get_object_or_404

def hint(request):
    if request.method == 'POST':
        question = get_object_or_404(Questions, Qid=request.POST.get('id'))
        hint = question.Hint
        questionPoints = question.points
        user = User.objects.get(username=request.user.username)
        userprofile = UserProfile.objects.get(user=user)
        try:
            solved = Submission.objects.get(question=question, user=userprofile)
            return HttpResponse(hint)
        except Submission.DoesNotExist:
            solved = Submission()
            solved.question = question
            solved.user = userprofile
            userprofile.score -= questionPoints * 0.1
            solved.curr_score = userprofile.score
            userprofile.save()  # Simpan perubahan skor pada userprofile
            return HttpResponse(hint)
    return render(request, 'ctf/404.html')





def check(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    questions = Questions.objects.all().order_by('Qid')
    
    if request.method == 'POST':
        req = request.POST
        Qid = req.get('Qid')
        flag = req.get('flag').lower()  # Konversi input flag ke lowercase
        level = req.get('customRadio')
        quest = Questions.objects.get(Qid=int(Qid))
        quest.Qid = Qid
        solved = Submission.objects.filter(question=quest, user=userprofile)
        
        if flag == quest.flag.lower():  # Konversi flag di database ke lowercase
            if not solved:
                solved = Submission()
                userprofile.score += quest.points
                solved.question = quest
                solved.user = userprofile
                solved.curr_score = userprofile.score
                print(solved.sub_time)
                quest.solved_by += 1
                solved.solved = 1
                userprofile.totlesub += 1
                userprofile.save()
                solved.save()
                quest.save()
                print(userprofile.score)
                print("FLAG IS CORRECT!")
                return HttpResponse('1')

            else:
                return HttpResponse('2')
        else:
            print("INCORRECT")
            return HttpResponse('0')
    
    return HttpResponse("")




def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        score = 0

        try:
            user = User.objects.get(username=username)
            return render(request, 'ctf/register.html', {'error': "Username Has Already Been Taken"})
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            userprofile = UserProfile(user=user, score=score)
            userprofile.save()
            login(request, user)

            return redirect("inst")

    elif request.method == 'GET':
        return render(request, 'ctf/register.html') 


def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            userprofile = UserProfile.objects.get(user=user)
            userprofile.save()
            return redirect("inst")
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request, 'ctf/login.html')

 # Redirect ke halaman login jika pengguna belum login
@login_required(login_url='/login')
def profil(request):
    return render(request, 'ctf/profil.html')

@login_required(login_url='/login')
def Quest(request):
        user = User.objects.get(username=request.user.username)
        userprofile = UserProfile.objects.get(user=user)
        questions = Questions.objects.all().order_by('Qid')
        submission = Submission.objects.values().filter(user=userprofile).order_by('question_id')
        print(submission)

        return render(request, 'ctf/quests.html',
                      {'questions': questions, 'userprofile': userprofile, 'submission': submission})


def logout(request):
    auth.logout(request)
    return redirect("/")


def leaderboard(request):
    # data = Submission.objects.all().order_by("-curr_score", "-sub_time")
    sorteduser = UserProfile.objects.all().order_by("-score","latest_sub_time")
    sub = Submission.objects.values().order_by('-user__score', 'user', 'sub_time')
    print(sub)
    count = 4
    sub_list = []
    for element in sorteduser:
        if count <= 4:
            sub = Submission.objects.values().filter(user_id=element.id)
            # sub.submission_set.all()
            # print(sub.submission_set)
            sub_list.append(sub)
            print(sub_list)
            count -= 1
        else:
            return render(request, 'ctf/hackerboard.html', context={'sub': sub_list, 'user': sorteduser})

    return render(request, 'ctf/hackerboard.html', context={'sub': sub_list, 'user': sorteduser})



def download_file(request, question_id):
    question = get_object_or_404(Questions, Qid=question_id)
    file_path = question.file.path
    response = FileResponse(open(file_path, 'rb'))
    return response


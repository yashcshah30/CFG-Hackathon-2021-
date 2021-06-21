import matplotlib.pyplot

from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from twilio.rest import Client
from .credentials import account_sid,auth_token
import random
import re
from django.http.response import JsonResponse
from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth.models import auth
from .models import *
from django.contrib import messages
from .forms import CommentForm
from chartjs.views.lines import BaseLineChartView
from django.views.generic import TemplateView


# # Create your views here.
# def sms(request):
#     client = Client(account_sid,auth_token)
#     num=random(5)
#     message = client.messages \
#                     .create(
#                             body="Thank you for registering.Your OTP is "+str(num),
#                             from_='+13134622764',
#                             to='phone_number'
#                         )
#     return(request,'confirmation.html')


def register_student(request):
    if request.method == 'POST':
        email = request.POST['email']
        team_name = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not User.objects.filter(email = email).exists():
            if password1 == password2:
                user = User.objects.create_user(
                    email = email, username = team_name, password = password1
                )
                number_of_members = request.POST['number_of_members']
                member1 = request.POST['member1']
                member2 = request.POST['member2']
                member3 = request.POST['member3']
                member4 = request.POST['member4']
                member5 = request.POST['member5']
                user.role = 'S'
                user.save()
                team = Team.objects.create(user = user, number_of_members = number_of_members, member1 = member1,
                    member2 = member2 , member3 = member3 , member4 = member4, member5 = member5
                )
                team.save()
                auth.login(request,user)
                return redirect('homepage')
            else:
                messages.info(request,"Passwords not matching")
                return redirect('register_students')
        else:
            messages.info(request,"Email id already exisits.")
            return redirect('register_students')
    else:
        return render(request,"myapp/index.html")

def register_mentor(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not User.objects.filter(email = email).exists():
            if password1 == password2:
                user = User.objects.create_user(
                    email = email, username = username, password = password1
                )
                profile =  request.POST['profile']
                user.role = 'M'
                user.save()
                mentor = Mentor.objects.create(user = user , profile = profile)
                mentor.save()
                auth.login(request,user)
                return redirect('homepage')
            else:
                messages.info(request,"Passwords not matching")
                return redirect('register_students')
        else:
            messages.info(request,"Email id already exisits.")
            return redirect('register_students')
    else:
        return render(request,"myapp/index.html")

def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request, user)
			return redirect('homepage')
		else:
			messages.info(request,"email or password incorrect")
			return redirect('register_students')
	else:
		return render(request,'myapp/index.html')

def user_logout(request):
	auth.logout(request)
	return redirect('register_students')

def homepage(request):
    user_obj = User.objects.filter(username=request.user).first()
    if user_obj.role == 'M':
        team_obj = Team.objects.filter(mentor__isnull=True).all()
        return render(request, "myapp/home_mentor.html", {'team_obj': team_obj})
    elif user_obj.role == 'J':
        team_obj = Team.objects.all()
        return render(request, "myapp/homepage_judge.html", {'team_obj': team_obj})
    else:
        return redirect('phase')


def confirm_team(request, team_id):
    mentor_obj = Mentor.objects.filter(user=request.user).first()
    Team.objects.filter(pk=team_id).update(mentor=mentor_obj)
    return redirect('homepage')

def phase(request):
    team_name = request.user.id
    team = Team.objects.filter(user = team_name)[0]
    #print(team.phase)
    if team.phase == '6':
        print("here")
        return redirect('final')
    phase = team.get_phase_display()
    phase_model = Phase.objects.filter(name = phase).first()
    ques_set = Question.objects.filter(phase = phase_model).all()
    #print(ques_set)
    ans_team = Answer.objects.filter(team = team.id)
    #print(ans_team)
    if request.method == 'POST':
        for ques in ques_set:
            print(ques)
            ans_new = request.POST[ques.question]
            ans = ans_team.filter(ques = ques.id).first()
            if ans is None:
                ans = Answer.objects.create(ques=ques,ans=ans_new,team=team)
                ans.save()
            else:
                ans.ans = ans_new
                ans.save()
        return redirect('phase')
    else:    
        ques_ans = {}
        
        for ques in ques_set:
            #print(ques.id)
            ans = ans_team.filter(ques = ques.id).first()
            if ans is None:
                ques_ans[ques.question] = ""
            else:
                ques_ans[ques.question] = ans.ans 
        images = Document.objects.filter(team = team.id, phase = phase_model.id)
        img = {}
        key = 1
        if images:
            # print(images[0].document)
            for image in images:
                img[key] = image.document
                key+=1
            

        #print(img)
        #print(ques_ans)
        if team.phase == '1':
            return render(request,'myapp/login.html', {'ques_ans' : ques_ans.items(), 'images' : img.items()})
        elif team.phase == '2':
            return render(request,'myapp/login2.html', {'ques_ans' : ques_ans.items(), 'images' : img.items()})
        elif team.phase == '3':
            return render(request,'myapp/login3.html', {'ques_ans' : ques_ans.items(), 'images' : img.items()})
        elif team.phase == '4':
            return render(request,'myapp/login4.html', {'ques_ans' : ques_ans.items(), 'images' : img.items()})
        else:
            return render(request,'myapp/login5.html')
        

def change_phase(request):
    team_name = request.user.id
    team = Team.objects.filter(user = team_name).first()
    phase = team.phase
    next_phase = str(int(phase)+1)
    team.phase = next_phase
    team.save()
    return redirect('phase')
    
def uploadimage(request):
    if request.method == 'POST' and request.FILES['myfile']:
        team_name = request.user.id
        team = Team.objects.filter(user = team_name).first()
        phase = team.get_phase_display()
        phase = Phase.objects.filter(name = phase).first()
        image = request.FILES['myfile']
        img = Document.objects.create(document = image, phase = phase, team = team)
        img.save()
        return redirect('phase')

# def mentorList(request):
#     #mentor = Mentor.objects.filter(user=request.user.id)
#     l = Mentor.objects.filter(teams__mentor = None)
#     print(l)
#     return HttpResponse('done')

def final_submission(request):
    team_name = request.user.id
    team = Team.objects.filter(user = team_name).first()
    phase = team.phase
    next_phase = str(int(phase)+1)
    team.phase = next_phase
    team.final_submission = request.POST['final_submission']
    team.save()
    return redirect('final')

def post_comment(request):
    user_obj = User.objects.filter(username=request.user).first()
    comment_obj = Comment.objects.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = request.POST.get('body')
            comment = Comment.objects.create(user=user_obj, body= new_comment)
            return redirect('comment')
    else:
        comment_form = CommentForm()

    return render(request, 'myapp/comment.html', {'comment_form':comment_form, 'comment_obj':comment_obj})
    

def update_team_profile(request):
    if request.method == 'POST':
        name=request.POST['team_name']
        obj=Team.objects.get(team_name=name)
        obj.member1=request.POST['member1']
        obj.member2=request.POST['member2']
        obj.member3=request.POST['member3']
        obj.member4=request.POST['member4']
        obj.member5=request.POST['member5']
        obj.number_of_members=request.POST['number_of_members']
        return redirect('phase')
    else:
        return render(request,"myapp/profile2.html")

def homepage_judge(request):
    team_obj = Team.objects.all()
    if(request.method=='POST'):
        for obj in team_obj:
            phase1 = request.POST.get(str(obj.id)+'phase1')
            phase2 = request.POST.get(str(obj.id)+'phase2')
            phase3 = request.POST.get(str(obj.id)+'phase3')
            phase4 = request.POST.get(str(obj.id)+'phase4')
            phase5 = request.POST.get(str(obj.id)+'phase5')
            total_score = int(phase1)+int(phase2)+int(phase3)+int(phase4)+int(phase5)
            Team.objects.filter(pk=obj.id).update(phase1_score=phase1, phase2_score=phase2, phase3_score=phase3,phase4_score=phase4,phase5_score=phase5, total_score=total_score)
            
        team_obj = Team.objects.all()

    return render(request, "myapp/homepage_judge.html", {'team_obj': team_obj})

def final(request):
    team_name = request.user.id
    team = Team.objects.filter(user = team_name).first()
    final_ans = {}
    final_images = {}
    ans_team = Answer.objects.filter(team = team.id)
    for i in range(1,6):
        phase = {}
        p = Phase.objects.get(id = i)
        questions = Question.objects.filter(phase = p.id)
        for q in questions:
            ans = ans_team.filter(ques = q.id).first()
            if ans is None:
                phase[q.question] = ""
            else:
                phase[q.question] = ans.ans
        final_ans[i] = phase

        images = Document.objects.filter(team = team.id, phase = p.id)
        img = {}
        key = 1
        if images:
            # print(images[0].document)
            for image in images:
                img[key] = image.document
                key+=1
        final_images[i] = img

        print(final_ans)
        print(final_images)
        final_sub = team.final_submission
    #return HttpResponse("done")
    return render(request,'myapp/final.html',{'final_ans':final_ans, 'final_images': final_images.items(), 'final_sub' : final_sub})

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["Identify", "Investigate","Ideate", "Implement", "Inform"]
        #return ["Team1", "Team2", "Team3"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Team1", "Team2", "Team3"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='myapp/line_chart.html')
line_chart_json = LineChartJSONView.as_view()

def pie_chart(request):
    labels = []
    data = []

    
    labels=['video_uploads','image_uploads']
    data=[40,60]

    return render(request, 'myapp/pie_chart.html', {
        'labels': labels,
        'data': data,
    })

def population_chart(request):
    labels = []
    data = []

    
    labels=['Social','Civic','Environmental','Community']
    data=[30,50,30,25]

    return render(request, 'myapp/pie_chart_domain.html', {
        'labels': labels,
        'data': data,
    })

def graphs(request):
    return render(request,'myapp/reports.html')
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from labRatsApp.models import LabRatUser
from labRatsApp.forms import UserForm,UserForm2,ExperimentForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):

    context = RequestContext(request)
    #context_dict = {'boldmessage': "Cool down tomorrow will be better than this."}
    user_detail = User.objects.all()
    context_dict = {'Users' : user_detail}

    return render_to_response('labRatsApp/index.html', context_dict, context)


def signUp(request):

	context = RequestContext(request)

	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		user_form2 = UserForm2(data=request.POST)
		if user_form.is_valid() and user_form2.is_valid():
			user = user_form.save()

			user.set_password(user.password)
            		user.save()

			user2 = user_form2.save(commit=False)
           		user2.user = user

			if 'picture' in request.FILES:
				user2.picture = request.FILES['picture']

			user2.save()
			registered = True
		else:
            		print user_form.errors,user_form2.errors
	else:
		user_form = UserForm()
		user_form2 = UserForm2()
		

	return render_to_response('labRatsApp/signUp.html', {'user_form' : user_form,'user_form2' : user_form2 , 'registered' : registered}, context)
    

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user is not None:
		    if user.is_active:
		        login(request, user)
		        return HttpResponseRedirect('/labRatsApp/')
		    else:
		        return HttpResponse("Your labRats account is disabled.")
		else:
		    print "Invalid login details: {0}, {1}".format(username, password)
		    return HttpResponse("Invalid login details supplied.")


	else:
		return render_to_response('labRatsApp/login.html', {}, context)



@login_required
def restricted(request):
    return HttpResponse("This is a page that will show when user have login (May be profile page)")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/labRatsApp/')

def about(request):
	context = RequestContext(request)
	return render_to_response('labRatsApp/about.html', {}, context)

def profile(request,username):
	context = RequestContext(request)
	user = User.objects.all().filter(username = username)[0]
	current_user = request.user
	if user is not  None:
		if current_user.username !=  user.username:
			return HttpResponse("Stalker!!, You can not access to this profile.")
		else:
			userDetail = LabRatUser.objects.all().filter(user =  current_user)[0]
			return render_to_response('labRatsApp/profile.html', {'user' : current_user,'userDetail' : userDetail }, context)
			
	else:
		return HttpResponse("Not found this user")



def createExperiment(request,username):
	context = RequestContext(request)

	create = False
	if request.method == 'POST':
		if username is not None:
	            user = User.objects.all().filter(username = username)[0]  	
		    LabUser = LabRatUser.objects.all().filter(user = user)[0]

		    if user.is_active:
			experiment_form = ExperimentForm(data=request.POST)
			if experiment_form.is_valid():
				experiment = experiment_form.save(commit=False)
           			experiment.LabUser = LabUser
				experiment.save()
				create = True
				return HttpResponseRedirect('/labRatsApp/profile/'+username+"/")
			else:	
            			print experiment_form.errors
		  		return HttpResponse("Invalid experiment details supplied.")

		    else:
		        return HttpResponse("Your labRats account is disabled.")
		else:
		    return HttpResponse("Invalid useename is None")

		
	else:
		user = User.objects.all().filter(username = username)[0]
		LabUser = LabRatUser.objects.all().filter(user = user)[0]
		if request.user.username != user.username:
			return HttpResponse("Hacker!! , This is not your username.")
		elif LabUser.userType == "rat":
			return HttpResponse("You are not an experimenter")
		else:
			experiment_form = ExperimentForm()
			return render_to_response('labRatsApp/createExperiment.html', {'experiment_form' : experiment_form,'username':username}, context)

	









from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from labRatsApp.models import LabRatUser,Experiment
from labRatsApp.forms import UserForm, UserDetailsForm, LabRatDetailsForm
from labRatsApp.forms import ExperimentForm, EditUserForm, EditLabRatUserForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    context = RequestContext(request)
    #user_detail = User.objects.all()
    experiments = Experiment.objects.order_by("-experimentID")[:5]
    for e in experiments:
    	e.percent_full = ( e.num_of_participants * 100 ) / e.max_participants

    return render_to_response('labRatsApp/index.html', {'experiments' : experiments}, context)

@login_required
def editUserDetail(request):
	context = RequestContext(request)
	if request.method == 'POST':
		user_form = EditUserForm(data=request.POST)
		user_form2 = EditLabRatUserForm(data=request.POST)
		if user_form.is_valid() and user_form2.is_valid():
			a = User.objects.get(username = request.user.username)
			user = EditUserForm(request.POST,instance = a)
			user.save()
			b = LabRatUser.objects.get(user = request.user)
			user2 = EditLabRatUserForm(request.POST,instance = b)
			user2.save()
			return HttpResponseRedirect('/labRatsApp/profile/'+request.user.username)	
         
		else:
            		print user_form.errors,user_form2.errors

	else:	
		LabUser = LabRatUser.objects.all().filter(user = request.user)[0]

		user_form = EditUserForm(initial = {'first_name':request.user.first_name,'last_name':request.user.last_name,'email':request.user.email})

		user_form2 =  EditLabRatUserForm(initial = {'title':LabUser.title,'phone':LabUser.phone,'webpage':LabUser.webpage,'school':LabUser.school,'age':LabUser.age})	

	return render_to_response('labRatsApp/signUp.html', {'user_form' : user_form,'user_form2' : user_form2, 'type':'Edit','url':'/labRatsApp/editProfile/'}, context)

def signUp(request):
	# Discourage logged in users from creating accounts
	if request.user.is_authenticated():
		return HttpResponseRedirect("/labRatsApp/")

	context = RequestContext(request)
	registered = False

	# Form has been submitted
	if request.method == "POST":
		userForm = UserForm(data=request.POST)
		userDetailsForm = UserDetailsForm(data=request.POST)
		labRatDetailsForm = LabRatDetailsForm(data=request.POST)

		# Check type of user
		userHasValidDetails = userDetailsForm.is_valid()
		isRat = (userDetailsForm.cleaned_data.get('userType') == "rat")

		# Form data is valid
		if userForm.is_valid() and userHasValidDetails and ((isRat and labRatDetailsForm.is_valid()) or not isRat ):
			user = userForm.save()
			user.set_password(user.password)
			user.save()

			userDetails = userDetailsForm.save(commit=False)
			userDetails.user = user

			if 'picture' in request.FILES:
				userDetails.picture = request.FILES['picture']

			userDetails.save()

			if(isRat):
				labRatDetails = labRatDetailsForm.save(commit=False)
				labRatDetails.user = userDetails
				labRatDetails.save()

			registered = True

		# Form data is invalid
		else:
			print userForm.errors, userDetailsForm.errors, labRatDetailsForm.errors

	# Form has not been submitted
	else:
		userForm = UserForm()
		userDetailsForm = UserDetailsForm()
		labRatDetailsForm = LabRatDetailsForm()

	return render_to_response('labRatsApp/register.html', {'registered': registered, 'userForm': userForm, 'userDetailsForm': userDetailsForm, 'labRatDetailsForm': labRatDetailsForm}, context)

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

@login_required
def profile(request,username):
	context = RequestContext(request)
	try:
		user = User.objects.all().filter(username = username)[0]
	except :
		return HttpResponse(content="User not found.", status=404)

	current_user = request.user

	if current_user.username !=  user.username:
		return HttpResponse(content="Access to this profile is forbidden.", status=403)

	userDetail = LabRatUser.objects.all().filter(user = current_user)[0]
	experiment = Experiment.objects.all().filter(user = userDetail)

	'''
	if userDetail.userType == "experimenter":
		return render_to_response('labRatsApp/ExperimenterProfile.html', {'user' : current_user,'userDetail' : userDetail,'experiment' : experiment }, context)
	else:
		return render_to_response('labRatsApp/RatProfile.html', {'user' : current_user,'userDetail' : userDetail }, context)		
	'''
	return render_to_response("labRatsApp/profile.html", {"user" : current_user, "userDetails": userDetail, "experiments": experiment}, context)

@login_required
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
           			experiment.user = LabUser
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


def experimentPage(request,expId):
	context = RequestContext(request)
	if request.method == 'POST':
		return HttpResponse("What is this")
	else:
		experiment_detail = Experiment.objects.all().filter(experimentID = expId)[0]
		return render_to_response('labRatsApp/experiment.html', {'experiment_details' : experiment_detail}, context)

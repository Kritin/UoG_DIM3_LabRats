import datetime, json

from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from labRatsApp.models import LabRatUser, Experiment, ParticipateIn, DemographicsSurvey
from labRatsApp.forms import UserForm, UserDetailsForm, LabRatDetailsForm
from labRatsApp.forms import ExperimentForm, RequirementsForm
from labRatsApp.forms import EditUserForm, EditLabRatUserForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

def index(request):
	context = RequestContext(request)

	experiments = Experiment.objects.filter(status="open")#.order_by("date_end")

	if(request.GET):
		filters = RequirementsForm(data=request.GET)

		if filters.is_valid():
			#apply filters to query
			if filters.cleaned_data.get("ageMin") is not None and filters.cleaned_data.get("ageMin") != "":
				experiments = experiments.exclude(requirement__ageMin__lt=filters.cleaned_data.get("ageMin"))

			if filters.cleaned_data.get("ageMax") is not None and filters.cleaned_data.get("ageMax") != "":
				experiments = experiments.exclude(requirement__ageMax__gt=filters.cleaned_data.get("ageMax"))
			
			if filters.cleaned_data.get("sex") is not None and filters.cleaned_data.get("sex") != "":
				experiments = experiments.filter(Q(requirement__sex=filters.cleaned_data.get("sex")) | Q(requirement__sex="") | Q(requirement__sex__isnull=True))
			
			if filters.cleaned_data.get("firstLanguage") is not None and filters.cleaned_data.get("firstLanguage") != "":
				experiments = experiments.filter(Q(requirement__firstLanguage=filters.cleaned_data.get("firstLanguage")) | Q(requirement__firstLanguage="") | Q(requirement__firstLanguage__isnull=True))

			if filters.cleaned_data.get("educationLevel") is not None and filters.cleaned_data.get("educationLevel") != "":
				experiments = experiments.filter(Q(requirement__educationLevel=filters.cleaned_data.get("educationLevel")) | Q(requirement__educationLevel="") | Q(requirement__educationLevel__isnull=True))
		else:
			print filters.errors
	else:
		filters = RequirementsForm()

	for e in experiments:
		e.percent_full = ( e.num_of_participants * 100 ) / e.max_participants
		e.description_short = (e.description[:256] + "...") if len(e.description) > 256 else e.description

	return render_to_response('labRatsApp/index.html', {'experiments' : experiments, 'filters': filters}, context)

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
		LabUser = LabRatUser.objects.filter(user = request.user)[0]

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
		user = User.objects.filter(username = username)[0]
	except :
		return HttpResponse(content="User not found.", status=404)

	current_user = request.user

	if current_user.username !=  user.username:
		return HttpResponse(content="Access to this profile is forbidden.", status=403)

	userDetails = LabRatUser.objects.filter(user = current_user)[0]

	experiments = Experiment.objects.filter(user = userDetails)
	for e in experiments:
		e.percent_full = ( e.num_of_participants * 100 ) / e.max_participants
		e.description_short = (e.description[:256] + "...") if len(e.description) > 256 else e.description
	
	ratDetails = None
	if(userDetails.userType == "rat"):
		ratDetails = DemographicsSurvey.objects.filter(user = userDetails)[0]
	activeExp = Experiment.objects.filter(user = userDetails,status="open")
	pastExp = Experiment.objects.filter(user = userDetails,status="open")
	

	'''
	if userDetail.userType == "experimenter":
		return render_to_response('labRatsApp/ExperimenterProfile.html', {'user' : current_user,'userDetail' : userDetail,'experiment' : experiment }, context)
	else:
		return render_to_response('labRatsApp/RatProfile.html', {'user' : current_user,'userDetail' : userDetail }, context)		
	'''
	return render_to_response("labRatsApp/profile.html", {"user" : current_user, "userDetails": userDetails, "experiments": experiments, "ratDetails":ratDetails,'activeExperiments':activeExp,'pastExperiments':pastExp}, context)

@login_required
def bid(request,expId):
	context = RequestContext(request)
	try:
		experimentDetails = Experiment.objects.get(experimentID=expId)
	except:
		return HttpResponse("Experiment " + expId + " does not exist.", status=404)
	experimentDetails.num_of_participants = int(experimentDetails.num_of_participants) + 1
	if int(experimentDetails.num_of_participants) == int(experimentDetails.max_participants) -1 :
		experimentDetails.status = "Full"
	try:
		mainUser = LabRatUser.objects.get(user = request.user)
		ratUser = DemographicsSurvey.objects.get(user = mainUser)
	except:
		return HttpResponse("User " + request.user.username + " does not match." , status=404)
	try:
		b = ParticipateIn(user = mainUser,experimentID = experimentDetails ,status = "bidding",date = datetime.date.today())
		b.save()
	except:
		return HttpResponseRedirect('/labRatsApp/')
	
	return HttpResponseRedirect('/labRatsApp/')


@login_required
def createExperiment(request,username):
	context = RequestContext(request)

	create = False
	if request.method == 'POST':
		if username is not None:
	            user = User.objects.filter(username = username)[0]  	
		    LabUser = LabRatUser.objects.filter(user = user)[0]

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
		user = User.objects.filter(username = username)[0]
		LabUser = LabRatUser.objects.filter(user = user)[0]
		if request.user.username != user.username:
			return HttpResponse("Hacker!! , This is not your username.")
		elif LabUser.userType == "rat":
			return HttpResponse("You are not an experimenter")
		else:
			experiment_form = ExperimentForm()
			return render_to_response('labRatsApp/createExperiment.html', {'experiment_form' : experiment_form,'username':username}, context)

def experimentPage(request,expId):
	context = RequestContext(request)

	# Retrieve experiment details
	try:
		experimentDetails = Experiment.objects.get(experimentID=expId)
		experimentDetails.percent_full = ( experimentDetails.num_of_participants * 100 ) / experimentDetails.max_participants
	except:
		return HttpResponse("Experiment " + expId + " does not exist.", status=404)

	# Retrieve author details
	author = User.objects.get(username=experimentDetails.user)
	authorDetails = LabRatUser.objects.get(user=author)

	currentUser = {}

	# Check if current user is the author
	if request.user.username ==  author.username:
		currentUser["isOwner"] = True

		#Get list of accepted users
		acceptedUsers = DemographicsSurvey.objects.values("user__user__username", "school", "firstLanguage", "age", "educationLevel", "sex", "country").filter(user__participatein__experimentID=expId, user__participatein__status="accepted")

		#Get list of bidding users
		biddingUsers = DemographicsSurvey.objects.values("user__user__username", "school", "firstLanguage", "age", "educationLevel", "sex", "country").filter(user__participatein__experimentID=expId, user__participatein__status="bidding")
	else:
		currentUser["isOwner"] = False
		acceptedUser = {}
		biddingUsers = {}

	# Render template
	return render_to_response('labRatsApp/experiment.html', {'experimentDetails' : experimentDetails, 'currentUser': currentUser, 'author': author, 'authorDetails': authorDetails, 'acceptedUsers': acceptedUsers, 'biddingUsers': biddingUsers}, context)
	
@login_required
def modifyParticipantStatus(request, eID, status, username):
	# Check if status is valid
	if status != "accept" and status != "reject":
		return HttpResponse("{'successful': false}", content_type="application/json", status=400)
	
	# Check if experiment is valid
	try:
		user = User.objects.get(labratuser__experiment__experimentID=eID)
	except:
		return HttpResponse("{'successful': false}", content_type="application/json", status=404)

	# Check if current user owns experiment
	if request.user.username != user.username:
		return HttpResponse("{'successful': false}", content_type="application/json", status=403)

	# Set ParticipateIn status and date
	try:
		participant = ParticipateIn.objects.get(experimentID=eID, user__user__username=username)
		if status == "accept":
			participant.status = "accepted"
		else:
			participant.status = "rejected"
		participant.date = datetime.date.today()
		participant.save()
	# User is not a participant in the experiment
	except:
		return HttpResponse("{'successful': false }", content_type="application/json", status=404)

	response = {}
	response["successful"] = True
	response["data"] = DemographicsSurvey.objects.values("user__user__username", "school", "firstLanguage", "age", "educationLevel", "sex", "country").get(user__participatein__user=participant.user, user__participatein__experimentID=eID)
	return HttpResponse(json.dumps(response), content_type="application/json")

def searchExperiment(request):
	context = RequestContext(request)
	if request.method == 'POST':
		expName = request.POST["searchValue"]

		try:
			experiments = Experiment.objects.get(title = expName)
			return HttpResponseRedirect('/labRatsApp/experiment/'+str(experiments.experimentID)+'/')
		except:
			return HttpResponseRedirect('/labRatsApp/experiment/0/')

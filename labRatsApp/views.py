import datetime, json

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail

from labRatsApp.models import LabRatUser, Experiment, ParticipateIn, DemographicsSurvey, Timeslot, EnrolIn, Requirement
from labRatsApp.forms import UserForm, UserDetailsForm, LabRatDetailsForm
from labRatsApp.forms import ExperimentForm, RequirementsForm, TimeslotForm
from labRatsApp.forms import EditUserForm, EditUserDetailsForm
#from labRatsApp.bing_search import run_query

def index(request):
	context = RequestContext(request)

	experiments = Experiment.objects.filter(status="open")
	sortBy = None
	selected = None

	if(request.GET):
		# get filters
		filters = RequirementsForm(data=request.GET)

		if filters.is_valid():
			# apply filters to query
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

			if filters.cleaned_data.get("location") is not None and filters.cleaned_data.get("location") != "":
				experiments = experiments.filter(Q(requirement__location=filters.cleaned_data.get("location")) | Q(requirement__location="") | Q(requirement__location__isnull=True))
		else:
			print filters.errors

		# get sort by
		sortBy = request.GET.get("sortBy")
		if sortBy is not None and sortBy != "" and sortBy == "reward":
			experiments = experiments.order_by("-rewardAmount")
			selected = "reward"
		elif sortBy is not None and sortBy != "" and sortBy == "location":
			experiments = experiments.order_by("location")
			selected = "location"
		elif sortBy is not None and sortBy != "" and sortBy == "dateEnd":
			experiments = experiments.order_by("date_end")
			selected = "dateEnd"

	else:
		filters = RequirementsForm()

	if sortBy is None:
		experiments = experiments.order_by("date_end")

	prepareExperiments(experiments)

	return render_to_response('labRatsApp/index.html', {'experiments' : experiments, 'filters': filters, 'selected': selected}, context)

@login_required
def editUserDetail(request):
	context = RequestContext(request)
	
	# Get current user's details
	currentUser = User.objects.get(username=request.user.username)
	currentLabRatUser = LabRatUser.objects.get(user=request.user)
	currentDemographicSurvey = None
	if currentLabRatUser.userType=="rat":
		currentDemographicSurvey = DemographicsSurvey.objects.get(user__user=request.user)
	user_form = None
	
	# Form has been submitted
	if request.method == 'POST':
		
		user_form = EditUserForm(data=request.POST, instance=currentUser )
		user_details_form = EditUserDetailsForm(data=request.POST, instance=currentLabRatUser)
		lab_rat_form = LabRatDetailsForm(data=request.POST, instance=currentDemographicSurvey)
		
		if user_details_form.is_valid() and (lab_rat_form.is_valid() or not currentLabRatUser.userType == "rat"):

			user_details_form.save()
			user = user_form.save()
			print user.password
			currentUser.set_password(user.password)
			currentUser.save()

			userDetails = user_details_form.save(commit=False)
			userDetails.user = user

			if 'picture' in request.FILES:
				userDetails.picture = request.FILES['picture']

			userDetails.save()

			if currentLabRatUser.userType == "rat":
				lab_rat_form.save()
				
			return HttpResponseRedirect('/labRatsApp/profile/'+request.user.username)	
		 
		else:
			#print user_form.errors, user_rat_form.errors, user_details_form.errors
			print lab_rat_form.errors, user_details_form.errors

	else:	
		LabUser = LabRatUser.objects.filter(user = request.user)[0]
		user_form = EditUserForm(instance=currentUser)
		user_details_form = EditUserDetailsForm(instance=currentLabRatUser)
		if LabUser.userType == "rat":

			lab_rat_form = LabRatDetailsForm(instance=currentDemographicSurvey)
		else:
			lab_rat_form = None
	return render_to_response('labRatsApp/settings.html', {'userForm' : user_form, 'userDetailsForm' : user_details_form, 'labRatDetailsForm' : lab_rat_form,'type':'Edit','url':'/labRatsApp/editProfile/'}, context)

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

				# store user type
				try:
					request.session["userType"] = LabRatUser.objects.get(user=user).userType
				except:
					request.session["userType"] = ""

				# get notifications for current user (using the Django message framework)
				# retrieves all entries from ParticipateIn which have been modified in the past week
				notifications = ParticipateIn.objects.filter(user__user=user, date__gte=(datetime.date.today()-datetime.timedelta(days=7)))
				notifications = notifications.filter(Q(status="accepted") | Q(status="rejected"))
				for notification in notifications:
					if notification.status == "accepted":
						msgStr = "Congratulations! You have been selected to participate in \"" + notification.experimentID.title + "\". "
					else:
						msgStr = "Sorry, you have been rejected from \"" + notification.experimentID.title + "\". "
					messages.info(request, msgStr, extra_tags="/labRatsApp/experiment/"+str(notification.experimentID.experimentID)+"/")
				request.session["msgCount"] = notifications.count()

				# redirect user to home page
				return HttpResponseRedirect('/labRatsApp/')
			else:
				return HttpResponse("Your labRats account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")


	else:
		return render_to_response('labRatsApp/login.html', {}, context)

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
	prepareExperiments(experiments)
	
	ratDetails = None
	activeExp = None
	pastExp = None
	
	currExp = None
	history = None
	currBids = None
	# get lab rat details and experiments
	if userDetails.userType == "rat" :
		ratDetails = DemographicsSurvey.objects.get(user = userDetails)
		history = Experiment.objects.filter(participatein__user=userDetails, date_end__lt=datetime.date.today())
		currExp = Experiment.objects.filter(participatein__user=userDetails, date_end__gte=datetime.date.today(), participatein__status='accepted')
		currBids = Experiment.objects.filter(participatein__user=userDetails, date_end__gte=datetime.date.today(), participatein__status='bidding')

		prepareExperiments(history)
		prepareExperiments(currExp)
		prepareExperiments(currBids)

	# get experimenter experiments
	else:
		current_user.canEdit = True

		activeExp = Experiment.objects.filter(user = userDetails, date_end__gte=datetime.date.today())
		pastExp = Experiment.objects.filter(user = userDetails,date_end__lt=datetime.date.today())

		prepareExperiments(activeExp)
		prepareExperiments(pastExp)

	return render_to_response("labRatsApp/profile.html", {"user" : current_user, "userDetails": userDetails, "history": history, "currentBids": currBids, "currentExperiments": currExp, "ratDetails":ratDetails,'activeExperiments':activeExp,'pastExperiments':pastExp }, context)
	
@login_required
def bid(request,expId):
	context = RequestContext(request)
	try:
		experimentDetails = Experiment.objects.get(experimentID=expId)
	except:
		return HttpResponse(json.dumps({"successful": False, "msg": "Experiment " + expId + " does not exist."}), content_type="application/json")

	try:
		mainUser = LabRatUser.objects.get(user = request.user)
		ratUser = DemographicsSurvey.objects.get(user = mainUser)
	except:
		return HttpResponse(json.dumps({"successful": False, "msg": "User " + request.user.username + " is not a lab rat."}), content_type="application/json")
	try:
		b = ParticipateIn(user=mainUser, experimentID=experimentDetails, status="bidding", date=datetime.date.today())
		b.save()
	except:
		return HttpResponse(json.dumps({"successful": False, "msg": "You've already bid on this experiment"}), content_type="application/json")
	
	return HttpResponse(json.dumps({"successful": True, "msg": "Bid stored successfully."}), content_type="application/json")


@login_required
def createExperiment(request):
	context = RequestContext(request)

	create = False
	if request.method == 'POST':
		if request.user.username is not None:
			user = User.objects.filter(username = request.user.username)[0]  	
			LabUser = LabRatUser.objects.filter(user = request.user)[0]

			if user.is_active:
				experiment_form = ExperimentForm(data=request.POST)
				requirements_form = RequirementsForm(data=request.POST)
				if experiment_form.is_valid() and requirements_form.is_valid():
					experiment = experiment_form.save(commit=False)
					experiment.user = LabUser
					experiment.save()
					requirements = requirements_form.save(commit=False)
					requirements.experiment = experiment
					requirements.save()
					create = True
					return HttpResponseRedirect('/labRatsApp/profile/'+request.user.username+"/")
				else:	
					print experiment_form.errors, requirements_form.errors
			else:
				return HttpResponse("Your labRats account is disabled.")
		else:
			return HttpResponse("Invalid username is None")

		
	else:
		user = User.objects.filter(username = request.user.username)[0]
		LabUser = LabRatUser.objects.filter(user = request.user)[0]
		if LabUser.userType == "rat":
			return HttpResponseForbidden("You are not an experimenter")
		else:
			experiment_form = ExperimentForm()
			requirements_form = RequirementsForm()
	
	return render_to_response('labRatsApp/createExperiment.html', {'experiment_form' : experiment_form, 'requirements_form' : requirements_form, 'username':request.user.username}, context)

def experimentPage(request,expId):
	context = RequestContext(request)

	# Retrieve experiment details
	try:
		experimentDetails = Experiment.objects.get(experimentID=expId)
		experimentDetails.percent_full = ( experimentDetails.num_of_participants * 100 ) / experimentDetails.max_participants
		experimentDetails.tags = experimentDetails.tags.split(", ")
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
		acceptedUsers = {}
		biddingUsers = {}

	# Check if current user is a participant
	try:
		participant = ParticipateIn.objects.get(user__user__username=request.user.username, experimentID=experimentDetails)
		currentUser["isParticipant"] = True
	except:
		participant = None
		currentUser["isParticipant"] = False

	# Check if current user has been accepted
	if participant and participant.status == "accepted":
		currentUser["isAccepted"] = True
	else:
		currentUser["isAccepted"] = False

	# Create timeslot if request is POST and user is the author
	if request.method == "POST" and currentUser["isOwner"]:
		timeslotForm = TimeslotForm(request.POST)

		if timeslotForm.is_valid():
			timeslot = timeslotForm.save(commit=False)
			timeslot.experimentID = experimentDetails
			timeslot.save()
		else:
			print timeslotForm.errors;
	else:
		timeslotForm = TimeslotForm()

	# Retrieve timeslots for experiment
	timeslots = Timeslot.objects.filter(experimentID=experimentDetails)
	for t in timeslots:
		if currentUser["isAccepted"] and EnrolIn.objects.filter(user__user__username=request.user.username, timeslotID=t).exists():
			t.isSelected = True
		else:
			t.isSelected = False

	# Render template
	return render_to_response('labRatsApp/experiment.html', {'experimentDetails' : experimentDetails, 'currentUser': currentUser, 'author': author, 'authorDetails': authorDetails, 'acceptedUsers': acceptedUsers, 'biddingUsers': biddingUsers, 'timeslotForm': timeslotForm, 'timeslots': timeslots }, context)
	
	
@login_required
def modifyExperiment(request,expId):
	context = RequestContext(request)
	print expId
	print request.user.username
	currentUser = User.objects.get(username=request.user.username)
	currentExperiment = Experiment.objects.get(experimentID=expId)
	try:
		currentRequirements = Requirement.objects.get(experiment=expId)
	except:
		currentRequirements = None
	#print currentExperiment.user.user.username
	if request.method == 'POST':
	
		experiment_form = ExperimentForm(data=request.POST, instance=currentExperiment)
		requirements_form = RequirementsForm(data=request.POST, instance=currentRequirements)
		if experiment_form.is_valid() and requirements_form.is_valid():
			
			currentExperiment = experiment_form.save(commit=False)
			currentExperiment.user.user = request.user
			currentExperiment.save()

			currentRequirements = requirements_form.save(commit=False)
			currentRequirements.experiment = currentExperiment
			currentRequirements.save()
			return HttpResponseRedirect('/labRatsApp/profile/'+request.user.username+"/")
		else:	
			print experiment_form.errors, requirements_form.errors


	else:

	
		user = User.objects.filter(username = request.user.username)[0]
		LabUser = LabRatUser.objects.filter(user = request.user)[0]

		if LabUser.userType == "rat":
			return HttpResponse("You are not an experimenter")
		else:
			experiment_form = ExperimentForm(instance=currentExperiment)
			requirements_form = RequirementsForm(instance=currentRequirements)
	return render_to_response('labRatsApp/modifyExperiment.html', {'expId': expId, 'experiment_form' : experiment_form, 'requirements_form' : requirements_form, 'username':request.user.username}, context)

	

	
@login_required
def enrol(request, eID, tID):
	# Check that user is a participant and that user has been accepted
	try:
		ParticipateIn.objects.get(user__user__username=request.user.username, experimentID=eID, status="accepted")
	except:
		return HttpResponse("You are not authorized to do this.", status=403)

	# Remove previous timeslot selection
	EnrolIn.objects.filter(user__user__username=request.user.username, timeslotID__experimentID=eID).delete()

	# Select new timeslot
	enrol = EnrolIn()
	enrol.user = LabRatUser.objects.get(user=request.user)
	enrol.timeslotID = Timeslot.objects.get(timeslotID=tID)
	enrol.save()

	# Redirect to experiment page
	return HttpResponseRedirect("/labRatsApp/experiment/" + eID + "/")

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
		experiment = Experiment.objects.get(experimentID=eID)
		if status == "accept":
			participant.status = "accepted"
			# increase number of participants
			
			experiment.num_of_participants += 1
			experiment.save()
			
		else:
			participant.status = "rejected"
		participant.date = datetime.date.today()
		participant.save()
		#print participant.user.email
		
	except:
		return HttpResponse("{'successful': false }", content_type="application/json", status=404)

	response = {}
	response["successful"] = True
	response["data"] = DemographicsSurvey.objects.values("user__user__username", "school", "firstLanguage", "age", "educationLevel", "sex", "country").get(user__participatein__user=participant.user, user__participatein__experimentID=eID)

	send_mail('Participation status of Experiment ' + experiment.title , 'You have been ' + participant.status, 'labratsapp@gmail.com', [participant.user.user.email], fail_silently=False)
	# User is not a participant in the experiment
	return HttpResponse(json.dumps(response), content_type="application/json")

def search(request):
	context = RequestContext(request)

	experiments = None
	query = ""

	# Retrieve search query
	if request.method == "POST":
		query = request.POST['query'].strip()

		if not query:
			return HttpResponse("Invalid search query.", status=403)
		
		experiments = Experiment.objects.filter(Q(title__contains=query) | Q(description__contains=query) | Q(tags__contains=query))
		prepareExperiments(experiments)

	return render_to_response('labRatsApp/search.html', {'query': query, 'experiments': experiments}, context)

def tag(request, tag):
	context = RequestContext(request)
	# get all experiments that share the same tag
	experiments = Experiment.objects.filter(Q(tags__contains= ", "+tag+", ") | Q(tags__startswith=tag+", ") | Q(tags__endswith=", "+tag) | Q(tags=tag))
	prepareExperiments(experiments)
	return render_to_response('labRatsApp/search.html', {'query': tag, 'experiments': experiments}, context)


def prepareExperiments(experiments):
	for e in experiments:
		e.percent_full = ( e.num_of_participants * 100 ) / e.max_participants
		e.description_short = (e.description[:256] + "...") if len(e.description) > 256 else e.description
		e.tags = e.tags.split(", ")

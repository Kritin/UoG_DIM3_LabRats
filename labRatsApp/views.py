from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from labRatsApp.models import User  
from labRatsApp.forms import UserForm

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

		if user_form.is_valid():
			user = user_form.save()
			#user.set_password(user.password)

			if 'picture' in request.FILES:
				user.picture = request.FILES['picture']

			user.save()
			registered = True
		else:
            		print user_form.errors
	else:
		user_form = UserForm()



	return render_to_response('labRatsApp/signUp.html', {'user_form' : user_form , 'registered' : registered}, context)
    



















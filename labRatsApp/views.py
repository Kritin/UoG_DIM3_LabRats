from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):

    context = RequestContext(request)
    context_dict = {'boldmessage': "Cool down tomorrow will be better than this."}

    return render_to_response('labRatsApp/index.html', context_dict, context)


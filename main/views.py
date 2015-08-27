from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def index_view(request):
    context = RequestContext(request, {
    })
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context))
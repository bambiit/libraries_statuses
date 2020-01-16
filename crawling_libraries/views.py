from django.shortcuts import render
from django.http import HttpResponse
from crawling_libraries.models import Libraries

# Create your views here.


def index(request):
    libraries = Libraries.objects.values('id', 'name')
    return render(request, 'index.html', {'libraries': libraries})

def details(request, library_id):
    library = Libraries.objects.get(id=library_id)
    return render(request, 'details.html', {'library': library})
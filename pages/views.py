from django.shortcuts import render, get_object_or_404
from . models import Page 

# Create your views here.
def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'pages/page_details.html', {'page':page})
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Blog

# Create your views here.
# def blog(request):
#     blogs = Blog.objects.all()
#     return render(request, 'basic/blogs.html', {'blogs':blogs})

# def blog_detail(request, id):
#     blog = get_object_or_404(Blog, id=id)
#     return render(request, 'basic/blog_details.html', {'blog': blog})

def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blogs.html', {'blogs':blogs})

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blog/blog_details.html', {'blog': blog})
from django.shortcuts import render, HttpResponse
from .models import LoginAttempt
from django.contrib import messages

def fake_admin_login(request):
    # return HttpResponse('Hi Fake admin')
    if request.method == "POST":
        LoginAttempt.objects.create(
            username=request.POST.get("username", ""),
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            path=request.path,
        )
        messages.error(request, "Please enter the correct username and password.")
    return render(request, "fake_admin/fake_admin_login.html")
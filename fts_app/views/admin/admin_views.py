from django.shortcuts import render
from django.http import HttpResponse
from ..decorators import check_session_exists  


@check_session_exists 
def login(request):
    # Your login view logic here
    return HttpResponse("Admin Login functionality")

@check_session_exists 
def dashboard(request): 
    return render(request, 'admin/dashboard-admin.html')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.hashers import check_password
from fts_app.models import User, UserRoleMap, Role
from pprint import pprint


def login(request):
    class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput)

    form = LoginForm(request.POST or None)  # Instantiate the LoginForm

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        # Retrieve the user from your custom user table
        user = User.objects.filter(username=username).first()

        if user is not None and check_password(password, user.password):
            # Check user's role
            user_role_map = UserRoleMap.objects.filter(user=user).first()
            if user_role_map is not None:
                role_id = user_role_map.role_id
                role_name = user_role_map.role.role_name.lower()
                
                # Store user information in session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['role_id'] = role_id
                request.session['role'] = role_name
                
                # Redirect based on role
                if role_name == 'admin':
                    request.session['home_url'] = 'dashboard-admin'
                    return redirect('dashboard-admin') 

                if role_name in ['gms', 'dakghar']:
                    request.session['home_url'] = 'dashboard-'+role_name
                    return redirect('dashboard-'+role_name)

                if role_name in ['hos', 'go', 'co','do','gm']:
                    request.session['home_url'] = 'dashboard-department'
                    return redirect('dashboard-department')     
            else:
                # Handle user without assigned role
                messages.error(request, 'User has no assigned role.')
        else:
            # Invalid login
            messages.error(request, 'Invalid username or password.')

    roles = Role.objects.all()
    if not roles.exists():
        return redirect('install')

    return render(request, 'login.html', {'form': form}) 




def logout(request):
    request.session.clear() 
    return redirect('/') 


 


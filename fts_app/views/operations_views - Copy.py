from django.shortcuts import render, redirect
from django.http import HttpResponse
from fts_app.models import StoreDocument, Role, User, Message

def list_correspondence(request): 
    data = {'section' : "list"} 
    return render(request,'correspondence.html',data);   



def add_correspondence(request): 
    uid = request.session.get('user_id')
    messages = Message.objects.filter(to_user_id=uid).select_related('document')
    # return HttpResponse(messages)
    data = {'section': "add", 'messages': messages}   
    return render(request, 'correspondence.html', data) 



def edit_correspondence(request):
    data = {'section' : "edit"}
    request.name = "edit" 
    return render(request, 'correspondence.html',data);



def monitoring_documents(request):
    
    return render(request, 'monitoring-documents.html');     


def delete_correspondence(request):  
   
   return redirect('/')
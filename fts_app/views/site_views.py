# site_views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from fts_app.models import StoreDocument, Role, User, Message, UserDetail, UserRoleMap , Department , SubDepartment, Correspondence, CorrespondenceUserMap, DepartmentRoleMap  
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Prefetch
from django.utils.dateparse import parse_date
import datetime
from .decorators import check_session_exists 
from django.db.models import F


def fetch_documents_for_correspondences(correspondences):
    for correspondence in correspondences:
        document_ids = correspondence.documents.split(',')
        documents = StoreDocument.objects.filter(pk__in=document_ids)
        correspondence.documents = documents

def red_cornered_open(request):
    correspondences = Correspondence.objects.filter(priority='high')
    fetch_documents_for_correspondences(correspondences)
    data = {'section': "red_cornered_open", 'correspondences': correspondences,'corr_count' : correspondences.count()}
    return render(request, 'public.html', data)

def red_cornered_closed(request):
    correspondences = Correspondence.objects.filter(priority='high', status=0)
    fetch_documents_for_correspondences(correspondences)
    data = {'section': "red_cornered_closed", 'correspondences': correspondences,'corr_count' : correspondences.count()}
    return render(request, 'public.html', data)

def all_documents_open_closed(request):
    correspondences = Correspondence.objects.all()
    fetch_documents_for_correspondences(correspondences)
    data = {'section': "all_documents_open_closed", 'correspondences': correspondences,'corr_count' : correspondences.count()}
    return render(request, 'public.html', data)

def all_documents_closed(request):
    correspondences = Correspondence.objects.filter(status=0)
    fetch_documents_for_correspondences(correspondences)
    data = {'section': "all_documents_closed", 'correspondences': correspondences,'corr_count' : correspondences.count()}
    return render(request, 'public.html', data)

def daily_entry_report(request):
    data = {'section': "daily_entry_report"}
    return render(request, 'public.html', data)  


# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from .models import CurrencyApp
from django.http import HttpResponse
import unicodedata
import json
import requests
from django.shortcuts import render,redirect
import datetime
#from django.http import JsonResponse


from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)
from .forms import UserLoginForm,UserRegForm


def login_view(request):
	#import pdb;pdb.set_trace()
	title='Login'
	form=UserLoginForm(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get("username")
		password=form.cleaned_data.get("password")
		user=authenticate(username=username,password=password)
		login(request,user)
		print(request.user.is_authenticated())
		return redirect('/first_page')
	return render(request,'login.html',{'form':form,'title':title})

def register_view(request):
	#import pdb;pdb.set_trace()
	title='Register'
	form=UserRegForm(request.POST or None)

	if form.is_valid():
		user=form.save(commit=False)
		password=form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		return redirect('/')
	return render(request,'register.html',{'form':form,'title':title})

def logout_view(request):
	logout(request)
	return render(request,'logout.html',{})

def first_page(request):
	return render(request,'first_page.html',{})


@csrf_exempt
def calculations(request):
	
	if request.is_ajax():
		#import pdb;pdb.set_trace()
		current_user = request.user
		currency1=request.POST.get('currency1')
		#currency1=unicodedata.normalize('NFKD', currency1).encode('ascii','ignore')
		r=requests.get('http://api.fixer.io/latest?base='+currency1).json()

		price1=float(request.POST.get('price'))
		#price=unicodedata.normalize('NFKD', price).encode('ascii','ignore')

		currency2=request.POST.get('currency2')
		#currency2=unicodedata.normalize('NFKD', currency2).encode('ascii','ignore')
		if currency2 in r['rates']:
			price2=float(r['rates'][currency2])
			result=price1 * price2

		now = datetime.datetime.now()
		string1=str(current_user)+':  '+str(currency1)+'  '+str(price1)+'  to  '+str(currency2)+'  at  '+str(now)
		CurrencyApp.objects.create(text=string1)

		latest={'currency1':currency1,'price1':price1,'currency2':currency2,'result':result}
		response=HttpResponse(json.dumps({'latest':latest}),content_type="application/json")
		return response
	#response = HttpResponse(json.dumps({'latest':latest}), content_type="application/json")
	#return response
		#return JsonResponse(latest)
	else:
		pass
		


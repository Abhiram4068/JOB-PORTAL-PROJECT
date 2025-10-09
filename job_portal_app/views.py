from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.db import models
from .models import *
import requests
from bs4 import BeautifulSoup
from django.contrib import messages


def index_fun(request):
    template=loader.get_template('index.html')
    user_name = request.session.get('username', False)
    return HttpResponse(template.render({'user_name':  user_name}))


def user_register_fun(request):
    template=loader.get_template('user_register.html')

    if 'submit' in request.POST:
        fname=request.POST["fname"]
        phno=request.POST["phno"]
        email=request.POST["email"]
        uname=request.POST["uname"]
        password=request.POST["password"]
        place=request.POST["place"]
        district=request.POST["district"]
        country=request.POST["country"]
        pincode=request.POST["pincode"]
        insert_val_login=user_login(username=uname, password=password)
        insert_val_login.save()
        insert_val_reg=user_registered(fullname=fname,phno=phno,email=email,place=place,district=district,country=country,pincode=pincode,login_id=insert_val_login.login_id)
        insert_val_reg.save()
        
    return HttpResponse(template.render())

def user_login_fun(request):
    show_alert = False
   
    template=loader.get_template('user_login.html')
    
    if "login" in request.POST:        
        uname=request.POST['uname']
        password=request.POST['password']
        
        
        loginned_user=user_login.objects.get(username=uname,password=password)
        
        if loginned_user:
            request.session['login_id']=loginned_user.login_id
            request.session['username']=loginned_user.username
      
            # q1=user_registered.objects.get(login_id=request.session['lid'])
            return redirect('index')
        else:
             show_alert = True
        
    return HttpResponse(template.render({'show_alert':show_alert},request))


def user_logout_fun(request):
    request.session.flush()
    return redirect('index')

        


def about_fun(request):
    template=loader.get_template('about.html')
    user_name = request.session.get('username', False)
    return HttpResponse(template.render({'user_name':  user_name}))

def contact_fun(request):
    template=loader.get_template('contact.html')
    user_name = request.session.get('username', False)
  
    return HttpResponse(template.render({'user_name':  user_name}))

def find_job_list_fun(request):
    template = loader.get_template('find_job_list.html')
    user_name = request.session.get('username', False)
    user_role=request.GET.get('job_name')
    user_loc=request.GET.get('job_location')
    if user_loc:
        url=f'https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords={user_role}%2C&cboWorkExp1=&txtLocation={user_loc}'
    else:
        url=f'https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords={user_role}%2C&cboWorkExp1=&txtLocation='

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    jobs=soup.find_all('div',class_='srp-job-bx')
    matched_jobs=[]
    for job in jobs:
        job_role=job.find('h3').a.text.strip()
        job_location=job.find('div',class_="srp-loc").text
        job_experience=job.find('div',class_="srp-exp").text
        job_company_name=job.find('span',class_='srp-comp-name').text
        job_posting_time=job.find('span',class_='posting-time').text
        job_salary=job.find('div',class_='srp-sal').text

        matched_jobs.append({
            'job_role':job_role,
            'job_location':job_location,
            'job_experience':job_experience,
            'job_company_name':job_company_name,
            'job_posting_time':job_posting_time,
            'job_salary':job_salary
        })
    job_complete_details = {'matched_jobs': matched_jobs}
    context = {**job_complete_details, 'user_name': user_name}

    return HttpResponse(template.render(context,request))


def filter_job_list_fun(request):
    template = loader.get_template('filter_job_list.html')
    user_name = request.session.get('username', False)

    # Get query parameters
    user_role = request.GET.get('job_role', '')
    user_loc = request.GET.get('job_location', '')
    user_exp = request.GET.get('job_exp', '')

    # Build URL for scraping
    url = f'https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords={user_role}%2C&cboWorkExp1={user_exp}&txtLocation={user_loc}'

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_='srp-job-bx')

    matched_jobs = []
    for job in jobs:
        job_role = job.find('h3').a.text.strip()
        job_location = job.find('div', class_='srp-loc').text
        job_experience = job.find('div', class_='srp-exp').text
        job_company_name = job.find('span', class_='srp-comp-name').text
        job_posting_time = job.find('span', class_='posting-time').text
        job_salary = job.find('div', class_='srp-sal').text

        matched_jobs.append({
            'job_role': job_role,
            'job_location': job_location,
            'job_experience': job_experience,
            'job_company_name': job_company_name,
            'job_posting_time': job_posting_time,
            'job_salary': job_salary
        })

    matchedjobs = {'matched_jobs': matched_jobs}
    context={**matchedjobs, 'user_name':  user_name}
    
    return HttpResponse(template.render(context, request))

def save_job(request):
    if "save_job_button" in request.POST:
        job_role=request.POST["job_role"]
        job_company_name=request.POST["job_company_name"]
        job_location=request.POST["job_location"]
        job_salary=request.POST["job_salary"]
        job_experience=request.POST["job_experience"]
        user_id=request.session['login_id']
        save_these_jobs=saved_jobs(job_role=job_role,company_name=job_company_name,job_location=job_location,job_salary=job_salary,
                                   job_experience=job_experience,login_id=user_id)
        save_these_jobs.save()
        
        return HttpResponse("<script>alert('Job saved successfully!');window.location.href='/filter_job_list';</script>")
    return HttpResponse("<script>alert('Oops something went wrong!');window.location.href='/filter_job_list';</script>")

def view_saved_jobs_fun(request):
    user_id = request.session.get("login_id")
    all_saved_jobs = saved_jobs.objects.filter(login_id=user_id)
    context={
        "all_saved_jobs":all_saved_jobs,
        "user_id":user_id
    }
    return render(request, "view_saved_jobs.html", context)


def login_save_job_button_fun(request):
    template=loader.get_template("user_login.html")
    return HttpResponse(template.render())


def delete_saved_job(request):
    if "delete_save_job_button" in request.POST:
        job_role=request.POST["job_role"]
        job_company_name=request.POST["company_name"]
        job_location=request.POST["job_location"]
        job_salary=request.POST["job_salary"]
        job_experience=request.POST["job_experience"]
        user_id=request.session['login_id']
        
        saved_jobs.objects.filter(
            login_id=user_id,
            job_role=job_role,
            company_name=job_company_name,
            job_location=job_location,
            job_salary=job_salary,
            job_experience=job_experience
        ).delete()
        return HttpResponse("<script>alert('Job removed!!!');window.location.href='/view_saved_jobs';</script>")
        

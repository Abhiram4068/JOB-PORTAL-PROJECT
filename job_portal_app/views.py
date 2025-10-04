from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.db import models
from .models import *
import requests
from bs4 import BeautifulSoup


def index_fun(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render())

def about_fun(request):
    template=loader.get_template('about.html')
    return HttpResponse(template.render())

def contact_fun(request):
    template=loader.get_template('contact.html')
    return HttpResponse(template.render())

def find_job_list_fun(request):
    template = loader.get_template('find_job_list.html')

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

    return HttpResponse(template.render(job_complete_details,request))


def filter_job_list_fun(request):
    template = loader.get_template('filter_job_list.html')

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

    context = {'matched_jobs': matched_jobs}
    return HttpResponse(template.render(context, request))


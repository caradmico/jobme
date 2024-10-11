from django.shortcuts import render, redirect
from .models import Job
from time import sleep
from random import randint
from warnings import warn
from bs4 import BeautifulSoup
import requests
from celery import shared_task  # Celery import

def scrape_craigslist_jobs():
    queries = [
        'admin+office', 'real+estate', 'nonprofit', 'accounting+finance',
        'systems+networking', 'manufacturing', 'sales', 'technical+support',
        'business+management', 'software+QA+DBA', 'art+media+design',
        'marketing+advertising+PR', 'tv+film+video+radio'
    ]
    locations = ['sfbay', 'newyork', 'losangeles']  # Add more locations as needed
    num_pages_to_scrape = 2
    pages = range(0, num_pages_to_scrape * 120, 120)

    jobs_to_create = []  # To collect jobs for bulk insert

    for location in locations:
        for query in queries:
            for page in pages:
                base_url = f"https://{location}.craigslist.org/search/jjj?query={query}&s={page}"
                
                try:
                    response = requests.get(base_url)
                    response.raise_for_status()  # Ensures any request failure raises an error
                except requests.RequestException as e:
                    warn(f'Request failed: {e}')
                    continue
                
                sleep(randint(1, 5))  # Random delay
                
                soup = BeautifulSoup(response.text, 'html.parser')
                posts = soup.find_all('li', class_='cl-static-search-result')

                for post in posts:
                    try:
                        # Extract job link safely
                        job_link_tag = post.find('a')
                        if job_link_tag:
                            job_link = job_link_tag.get('href')
                        else:
                            print(f"Missing job link in post: {post}")
                            continue

                        # Extract job title safely
                        job_title_tag = post.find('div', class_='title')
                        if job_title_tag:
                            job_title = job_title_tag.text.strip()
                        else:
                            print(f"Missing job title in post: {post}")
                            continue

                        print(f"Job Title: {job_title}, Job Link: {job_link}")

                        # Prevent duplicates by checking if the job URL already exists
                        if Job.objects.filter(url=job_link).exists():
                            continue

                        # Add jobs to the list for bulk creation later
                        jobs_to_create.append(
                            Job(
                                title=job_title,
                                company="N/A",
                                location=location,
                                salary="N/A",
                                date_posted="N/A",
                                source="Craigslist",
                                url=job_link
                            )
                        )

                    except Exception as e:
                        print(f"Error while processing post: {e}")
                        continue

    # Bulk create the jobs after collecting them (for efficiency)
    if jobs_to_create:
        Job.objects.bulk_create(jobs_to_create)

# Displaying the scraped jobs
def job_list(request):
    # Fetch all jobs from the database
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def fetch_jobs(request):
    # Trigger the scraping job in the background via Celery
    scrape_craigslist_jobs_task.delay()
    return redirect('job_list')

@shared_task
def scrape_craigslist_jobs_task():
    scrape_craigslist_jobs()

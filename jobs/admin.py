from django.contrib import admin
from .models import Job
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from jobs.cron.scrape_jobs import Command as ScrapeCommand  # Import the scraper command

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'date_posted')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('scrape-jobs/', self.admin_site.admin_view(self.scrape_jobs), name='scrape_jobs')
        ]
        return custom_urls + urls

    def scrape_jobs(self, request):
        # Run the scrape_jobs command when the button is pressed
        try:
            ScrapeCommand().handle()  # Trigger the scrape_jobs command
            self.message_user(request, "Jobs scraped successfully!", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error scraping jobs: {e}", level=messages.ERROR)
        
        return HttpResponseRedirect("../")

    # Add the button to the admin page
    change_list_template = "admin/jobs/job/change_list.html"

from django_cron import CronJobBase, Schedule
from jobs.cron.scrape_jobs import Command as ScrapeCommand

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # 24 hours (can be changed as needed)

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'jobs.my_cron_job'  # Unique code for your cron job

    def do(self):
        ScrapeCommand().handle()  # Run the scraping logic
        print("Craigslist jobs scraped and saved to the database!")

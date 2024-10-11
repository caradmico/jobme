from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, null=True, blank=True)
    date_posted = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=50, default="Craigslist")  # Keeping default
    url = models.URLField(max_length=500)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Clean up whitespace, etc.
        self.title = self.title.strip()
        if self.company:
            self.company = self.company.strip()
        self.location = self.location.strip()
        if self.salary:
            self.salary = self.salary.strip()
        if self.date_posted:
            self.date_posted = self.date_posted.strip()

        # Call the original save() method
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.company or 'Unknown company'} ({self.location})"

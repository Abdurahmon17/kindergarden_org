from datetime import date
from django.db import models
from django.utils import timezone

class MonthlyReport(models.Model):
    report_date = models.DateField(default=timezone.now, blank=True)
    prepared_portions = models.PositiveIntegerField(default=0)
    possible_portions = models.PositiveIntegerField(default=0)
    difference_percent = models.FloatField(default=0.0, blank=True, null=True)
    warning = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('report_date',)
        ordering = ['-report_date']

    def save(self, *args, **kwargs):
        if not self.report_date:
            self.report_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.report_date.strftime('%Y-%m')} Report"

    @property
    def formatted_date(self):
        return self.report_date.strftime('%Y-%m')

    @property
    def month(self):
        return self.report_date.strftime('%B')

    @property
    def year(self):
        return self.report_date.year

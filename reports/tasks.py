from celery import shared_task
from reports.models import MonthlyReport
import logging
from datetime import date

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def generate_monthly_report(self, year, month, prepared_portions, possible_portions, difference_percent, warning):
    try:
        logger.info(f"Generating report for {year}-{month:02d}")
        logger.info(f"Input data: prepared={prepared_portions}, possible={possible_portions}, percent={difference_percent}, warning={warning}")

        # year va month dan report_date hosil qilish
        report_date = date(year, month, 1)

        report, created = MonthlyReport.objects.update_or_create(
            report_date=report_date,
            defaults={
                'prepared_portions': prepared_portions,
                'possible_portions': possible_portions,
                'difference_percent': difference_percent,
                'warning': warning,
            }
        )
        logger.info(f"Report {report.id} {'created' if created else 'updated'}: prepared={prepared_portions}, possible={possible_portions}, percent={difference_percent}, warning={warning}")

        return {
            'status': 'success',
            'report_id': report.id,
            'prepared': prepared_portions,
            'possible': possible_portions,
            'percent': difference_percent,
            'warning': warning
        }

    except Exception as e:
        logger.exception(f"Error generating report for {year}-{month:02d}: {e}")
        self.retry(exc=e, countdown=60)
        return {'status': 'error', 'message': str(e)}
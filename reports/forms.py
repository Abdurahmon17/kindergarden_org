from django import forms
from django.utils import timezone
from .models import MonthlyReport

class MonthlyReportForm(forms.ModelForm):
    class Meta:
        model = MonthlyReport
        fields = ['report_date', 'prepared_portions', 'possible_portions', 'difference_percent', 'warning']
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
            'warning': forms.CheckboxInput(),
        }
        labels = {
            'report_date': 'Hisobot sanasi',
            'prepared_portions': 'Tayyorlangan porsiyalar',
            'possible_portions': 'Mumkin porstiyalar',
            'difference_percent': 'Farq foizi',
            'warning': 'Ogohlantirish',
        }

    def clean_report_date(self):
        date = self.cleaned_data.get('report_date')
        if not date:
            return timezone.now().date()  # avtomatik bugungi sana
        if date.year < 2000 or date.year > timezone.now().year + 1:
            raise forms.ValidationError("Yil 2000 dan katta va kelasi yildan kichik bo'lishi kerak.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        prepared = cleaned_data.get('prepared_portions')
        possible = cleaned_data.get('possible_portions')
        difference_percent = cleaned_data.get('difference_percent')

        if prepared is not None and possible is not None:
            if possible == 0 and (difference_percent is not None and difference_percent != 0):
                raise forms.ValidationError("Mumkin porstiyalar 0 bo'lsa, farq foizi 0 bo'lishi kerak.")
        return cleaned_data

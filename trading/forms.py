from django import forms
from .models import CandlePriceGuess, CandleColorGuess
import datetime
from django.utils import timezone

class CandlePriceGuessForm(forms.ModelForm):
    class Meta:
        model = CandlePriceGuess
        fields = ['guessed_value']

    def clean(self):
        cleaned_data = super().clean()
        now = timezone.localtime().time()  # استفاده از زمان محلی
        start_time = datetime.time(7, 00)
        end_time = datetime.time(12, 00)
        if not (start_time <= now <= end_time):
            raise forms.ValidationError("حدس زدن فقط بین ساعت 10:30 تا 15:30 امکان‌پذیر است.")
        return cleaned_data

class CandleColorGuessForm(forms.ModelForm):
    class Meta:
        model = CandleColorGuess
        fields = ['guessed_color']

    def clean(self):
        cleaned_data = super().clean()
        now = timezone.localtime().time()
        start_time = datetime.time(7, 00)
        end_time = datetime.time(12, 00)
        if not (start_time <= now <= end_time):
            raise forms.ValidationError("حدس زدن فقط بین ساعت 10:30 تا 15:30 امکان‌پذیر است.")
        return cleaned_data

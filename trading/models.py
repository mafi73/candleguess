from django.db import models
from django.conf import settings
from django.db import models

class CandlePriceGuess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    guess_date = models.DateField(auto_now_add=True)
    guessed_value = models.DecimalField(max_digits=10, decimal_places=2)
    guess_time = models.TimeField(auto_now_add=True)
    is_correct = models.BooleanField(null=True, blank=True)  # پس از اعلام قیمت 18:00 به‌روز می‌شود

    class Meta:
        unique_together = ('user', 'guess_date')

    def __str__(self):
        return f"{self.user.username} - {self.guess_date} - {self.guessed_value}"

class CandleColorGuess(models.Model):
    COLOR_CHOICES = (
        ('red', 'قرمز'),
        ('green', 'سبز'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    guess_date = models.DateField(auto_now_add=True)
    guessed_color = models.CharField(max_length=5, choices=COLOR_CHOICES)
    guess_time = models.TimeField(auto_now_add=True)
    is_correct = models.BooleanField(null=True, blank=True)  # پس از اعلام نتیجه به‌روز می‌شود

    class Meta:
        unique_together = ('user', 'guess_date')

    def __str__(self):
        return f"{self.user.username} - {self.guess_date} - {self.guessed_color}"


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CandlePriceGuessForm, CandleColorGuessForm
from .models import CandlePriceGuess, CandleColorGuess
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from datetime import date , datetime , timedelta
from django.utils.timezone import make_aware


# ویوی ثبت‌نام
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'trading/signup.html', {'form': form})


# ویوی ورود
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'trading/login.html', {'form': form})


# ویوی خروج
def logout_view(request):
    logout(request)
    return redirect('login')


# صفحه اصلی
@login_required
def home(request):
    return render(request, 'trading/home.html')


# حدس قیمت
# @login_required
# def guess_price_view(request):
#     today = timezone.now().date()
#     if CandlePriceGuess.objects.filter(user=request.user, guess_date=today).exists():   
#         now = timezone.now()
#         next_guess_time = datetime.combine(today + timedelta(days=1), datetime.min.time())
#         remaining_seconds = int((next_guess_time - now).total_seconds())
#         return render(request, 'trading/guess_already_done.html', {
#             'message': 'شما امروز قبلاً حدس قیمت زده‌اید.',
#             'remaining_seconds': remaining_seconds
#             })
    
#     if request.method == 'POST':
#         form = CandlePriceGuessForm(request.POST)
#         if form.is_valid():
#             guess = form.save(commit=False)
#             guess.user = request.user
#             guess.guess_date = today
#             guess.guess_time = timezone.localtime().time()
#             guess.save()
#             return redirect('guess_success')
#     else:
#         form = CandlePriceGuessForm()
    
#     return render(request, 'trading/guess_price_form.html', {'form': form})

@login_required
def guess_price_view(request):
    today = timezone.now().date()
    if CandlePriceGuess.objects.filter(user=request.user, guess_date=today).exists():
        # محاسبه زمان باقی‌مانده تا فردا
        now = timezone.now()
        next_guess_time = make_aware(datetime.combine(today + timedelta(days=1), datetime.min.time()))
        remaining_seconds = int((next_guess_time - now).total_seconds())
        return render(request, 'trading/guess_already_done.html', {
            'message': 'شما امروز قبلاً حدس قیمت زده‌اید.',
            'remaining_seconds': remaining_seconds
        })
    
    if request.method == 'POST':
        form = CandlePriceGuessForm(request.POST)
        if form.is_valid():
            guess = form.save(commit=False)
            guess.user = request.user
            guess.guess_date = today
            guess.guess_time = timezone.localtime().time()
            guess.save()
            return redirect('guess_success')
    else:
        form = CandlePriceGuessForm()
    
    return render(request, 'trading/guess_price_form.html', {'form': form})

# حدس رنگ
@login_required
def guess_color_view(request):
    today = timezone.now().date()
    if CandleColorGuess.objects.filter(user=request.user, guess_date=today).exists():
        now = timezone.now()
        next_guess_time = make_aware(datetime.combine(today + timedelta(days=1), datetime.min.time()))
        remaining_seconds = int((next_guess_time - now).total_seconds())

        return render(request, 'trading/guess_already_done.html', {
            'message': 'شما امروز قبلاً حدس رنگ زده‌اید.',
            'remaining_seconds': remaining_seconds
            })
    
    if request.method == 'POST':
        form = CandleColorGuessForm(request.POST)
        if form.is_valid():
            guess = form.save(commit=False)
            guess.user = request.user
            guess.guess_date = today
            guess.guess_time = timezone.localtime().time()
            guess.save()
            return redirect('guess_success')
    else:
        form = CandleColorGuessForm()
    
    return render(request, 'trading/guess_color_form.html', {'form': form})


# موفقیت در ثبت حدس
@login_required
def guess_success_view(request):
    return render(request, 'trading/guess_success.html')


# مدیریت اعتبارسنجی کامل توسط ادمین
@staff_member_required
def validate_result(request):
    if request.method == "POST":
        real_price = request.POST.get("real_price")
        real_color = request.POST.get("real_color")
        today = date.today()

        # اعتبارسنجی قیمت
        CandlePriceGuess.objects.filter(guess_date=today).update(is_correct=False)
        price_guesses = CandlePriceGuess.objects.filter(guess_date=today)
        correct_price_guesses = []

        for guess in price_guesses:
            if float(guess.guessed_value) == float(real_price):
                guess.is_correct = True
                guess.save()
                correct_price_guesses.append(guess)

        # اعتبارسنجی رنگ
        CandleColorGuess.objects.filter(guess_date=today).update(is_correct=False)
        color_guesses = CandleColorGuess.objects.filter(guess_date=today)
        correct_color_guesses = []

        for guess in color_guesses:
            if guess.guessed_color == real_color:
                guess.is_correct = True
                guess.save()
                correct_color_guesses.append(guess)

        context = {
            "real_price": real_price,
            "real_color": real_color,
            "correct_price_guesses": correct_price_guesses,
            "correct_color_guesses": correct_color_guesses,
        }

        return render(request, "admin/result_summary.html", context)

    return render(request, "admin/validate_result.html")

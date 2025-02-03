from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),           # صفحه ورود به عنوان صفحه اصلی
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('guess-price/', views.guess_price_view, name='guess_price'),
    path('guess-color/', views.guess_color_view, name='guess_color'),
    path('guess-success/', views.guess_success_view, name='guess_success'),
    path('dashboard/validate-result/', views.validate_result, name='validate_result'),
]
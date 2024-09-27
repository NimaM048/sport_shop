from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'register'

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('check_otp', views.CheckOtpView.as_view(), name='verification'),
    path('logout', views.user_logout, name='logout'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile_courses', views.ProfileCoursesView.as_view(), name='profile_course'),
    path('profile_financial', views.ProfileFinancialView.as_view(), name='profile_financial'),
    path('profile_comments', views.ProfileCommentsView.as_view(), name='profile_comments'),
    path('profile_notifications', views.ProfileNotificationsView.as_view(), name='profile_notifications'),
    path('profile_useredit', views.edit_user_profile, name='profile_useredit'),
    path('profile_number_edit', views.NumberEdit.as_view(), name='profile_number_edit'),
    path('pass_register', views.signup, name='pass_register'),
    path('pass_login/', views.login_view, name='pass_login'),
    path('passwrod_change', views.PasswordsChangeView.as_view(), name='change_password'),
    path('add_course/<int:series_id>/', views.AddCourseToProfileView.as_view(), name='add_course_to_profile'),
]

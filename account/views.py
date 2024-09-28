from datetime import timedelta
from random import randint
from uuid import uuid4

from django.utils.encoding import force_bytes
from django_user_agents.utils import get_user_agent
import ghasedakpack as ghasedakpack
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView

from account.froms import OtpForm, CheckOtp, UserEditForm, NumberEditForm, FormRegister, PasswordChanged, FormLogin

from account.models import Otp, User, UserSession, Notification
from cart.models import OrderItem, Order
from home.models import SeriesModel, UserCourse

SMS = ghasedakpack.Ghasedak("")


class Register(View):
    def get(self, request):
        form = OtpForm()
        return render(request, 'account/login-register.html', context={"form": form})

    def post(self, request):
        form = OtpForm(request.POST)
        if form.is_valid():
            randcode = randint(10000, 99999)
            cd = form.cleaned_data
            SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': 'randcode', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd["phone"], code=randcode, token=token)
            print(randcode)
            return redirect(reverse("register:verification") + f'?token={token}')

        else:
            form.add_error('phone', "یک شماره ی صحیح وارد کنید")

        return render(request, 'account/login-register.html', context={'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtp()
        return render(request, 'account/verification.html', context={"form": form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtp(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            try:
                otp = Otp.objects.get(code=cd['code'], token=token)

                # Assuming the OTP is valid for 5 minutes (adjust as necessary)
                expiration_time = otp.created_at + timedelta(minutes=5)

                from django.utils import timezone
                if timezone.now() <= expiration_time:  
                    user, is_created = User.objects.get_or_create(phone=otp.phone)
                    login(request, user)
                    otp.delete()  # Delete OTP after successful login
                    # Add success message
                    messages.success(request, "با موفقیت وارد شدید")

                    return redirect('home:home')
                else:
                    form.add_error('code', 'کد OTP منقضی شده است.') 

            except Otp.DoesNotExist:
                form.add_error('code', 'کد وارد شده نادرست است.') 

        return render(request, 'account/verification.html', context={'form': form})


def user_logout(request):
    logout(request)
    return redirect("/")


class ProfileView(TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = self.request.user  # Get the currently logged-in user

       
        paid_series = SeriesModel.objects.filter(
            order_items__order__is_paid=True,
            order_items__order__user=user
        ).distinct()

        context['items'] = paid_series 
        context['learning_courses_count'] = paid_series.count() 
        return context


class ProfileCoursesView(TemplateView):
    template_name = 'account/profile-courses.html'
    model = SeriesModel  # Reference to your SeriesModel

    def get_context_data(self, **kwargs):
        context = super(ProfileCoursesView, self).get_context_data(**kwargs)
        user = self.request.user  # Get the currently logged-in user

        
        paid_series = SeriesModel.objects.filter(
            order_items__order__is_paid=True,  # Use the correct related name 'order_items'
            order_items__order__user=user
        ).distinct()

        
        free_series = SeriesModel.objects.filter(series_users__user=user, free=True).distinct()
        # Combine paid and free series into a single list
        all_series = paid_series | free_series

        context['items'] = all_series  
        return context


class AddCourseToProfileView(View):
    def post(self, request, series_id):
        if not request.user.is_authenticated:
            return redirect('register:pass_login')
        series = get_object_or_404(SeriesModel, id=series_id, free=True)
        user = request.user

        # Check if the user has already added this course
        if not UserCourse.objects.filter(user=user, series=series).exists():
            UserCourse.objects.create(user=user, series=series)

        return redirect('home:series_episod', pk=series_id)

class ProfileFinancialView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile-financial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileCommentsView(TemplateView):
    template_name = 'account/profile-comments.html'


class ProfileNotificationsView(TemplateView):
    template_name = 'account/profile-notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['notifications'] = Notification.objects.filter(user=self.request.user).order_by('-created_at')
        else:
            context['notifications'] = []
        return context


@login_required
def edit_user_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات شما با موفقیت بروزرسانی شد')
            return redirect('register:profile_useredit')  # redirect to profile page after updating
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'account/profile-edit.html', {'form': form})


class NumberEdit(View):
    template_name = 'account/edit_number.html'

    def get(self, request):
        form = NumberEditForm(initial={'phone_number_new': ''})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NumberEditForm(request.POST)
        if form.is_valid():
            request.user.phone = form.cleaned_data['phone_number_new']
            request.user.save()
            messages.success(request, 'اطلاعات با موفقیت بروزرسانی شد.')  # success message in Persian
            return redirect('register:profile_number_edit')  # Redirect to profile page
        return render(request, self.template_name, {'form': form})

def signup(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            fullname = form.cleaned_data['fullname']

            
            if User.objects.filter(fullname=fullname).exists():
                messages.error(request, 'نام کاربری وارد شده قبلا ثبت شده است.')
                return render(request, 'account/pass_register.html', {'form': form})

            # Create a new user
            user = User(phone=phone, fullname=fullname)
            user.set_password(password) 
            user.save()
            login(request, user)  # Login the newly created user
            return redirect(reverse_lazy('home:home')) 
        # Add success message
        messages.success(request, "با موفقیت وارد شدید")

    else:
        form = FormRegister()

    return render(request, 'account/pass_register.html', {'form': form})


from django.contrib import messages

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChanged
    success_url = reverse_lazy('home:home')
    template_name = 'account/change_password.html'

    def form_valid(self, form):
        messages.success(self.request, 'رمز عبور شما با موفقیت تغییر کرد')
        return super().form_valid(form)


def login_view(request):
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['fullname'], password=cd['password'])
            if user is not None:
                login(request, user)

                # Save the IP address of the user
                session_key = request.session.session_key
                ip_address = request.META.get('REMOTE_ADDR')
                user_agent = request.META.get('HTTP_USER_AGENT')
                UserSession.objects.create(user=user, session_key=session_key, ip_address=ip_address,
                                           user_agent=user_agent)

                
                messages.success(request, "با موفقیت وارد شدید")

                return redirect('home:home')
            else:
                form.add_error(None, "نام کاربری یا کلمه عبور اشتباه است.")
                return render(request, 'account/pass_login.html', {'form': form})
    else:
        form = FormLogin()
    return render(request, 'account/pass_login.html', {'form': form})

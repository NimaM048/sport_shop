import os

from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.core import validators
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from account.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.forms import PasswordChangeForm

from cart.models import Order
from home.models import SeriesModel
from sport_shop import settings


class OtpForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': "form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground placeholder:text-right px-5",
            "placeholder": "شماره تلفن خود را وارد کنید"}),
        validators=[RegexValidator(
            regex=r'^\d{10,11}$',
            message='شماره تلفن باید 11 رقم باشد',
            code='invalid_phone_number'
        )]
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise ValidationError('لطفا شماره تلفن خود را وارد کنید.')
        return phone


class CheckOtp(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': "form-input w-full h-11 peer !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border invalid:!border-error rounded-xl text-lg tracking-9 text-center text-foreground invalid:!text-error placeholder:text-right px-5",
            "placeholder": "کد را وارد کنید"}),
        validators=[RegexValidator(
            regex=r'^\d{5}$',
            message='لطفا کد 5 رقمی وارد کنید',
        )]
    )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("fullname", 'email', "biography", 'web_site', 'github', "linkdin", 'telegram', 'profile_picture')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
            'fullname': forms.TextInput(attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
            'biography': forms.TextInput(attrs={
                'class': 'form-textarea w-full !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
            'web_site': forms.TextInput(attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
            'github': forms.TextInput(attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
            'linkdin': forms.TextInput(attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
            'telegram': forms.TextInput(attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("ایمیل در حاضر مطلق با کاربر دیگریست.")
        if not email:
            raise ValidationError('لطفا ایمیل خود را وارد کنید.')

        return email

    def save(self, commit=True):
        instance = super(UserEditForm, self).save(commit=False)

        # Check if the profile picture has changed.
        if 'profile_picture' in self.changed_data:
            # If there's already a profile picture, attempt to delete the old file
            if instance.pk:  # Check if the instance is already saved
                old_instance = User.objects.get(pk=instance.pk)
                if old_instance.profile_picture:
                    try:
                        # Construct the file path and remove the old file
                        os.remove(os.path.join(settings.MEDIA_ROOT, old_instance.profile_picture.path))
                    except FileNotFoundError:
                        pass  # It's okay if the file does not exist (for example, if it's been deleted already)

        if commit:
            instance.save()
        return instance


from django import forms
from django.core.exceptions import ValidationError
import re

import re
from django import forms
from django.core.exceptions import ValidationError


class NumberEditForm(forms.Form):
    phone_number_new = forms.CharField(
        required=True,  # Make new phone number required
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
        error_messages={
            'required': 'لطفا شماره تماس جدید را وارد کنید.',  # Please enter a new phone number.
            'invalid': 'فرمت شماره تماس نامعتبر است.'  # Invalid phone number format.
        }
    )

    def clean_phone_number_new(self):
        phone_number = self.cleaned_data.get('phone_number_new')
        # Updated regex for phone number validation to match exactly 12 digits
        if not re.match(r'^\d{11}$', phone_number):
            raise ValidationError(
                'لطفا یک شماره تماس 11رقمی وارد کنید.')  # Please enter the phone number correctly and ensure it has exactly 12 digits.
        return phone_number

    class Meta:
        model = User
        fields = ('phone',)
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'}),
        }


class FormRegister(forms.Form):
    fullname = forms.CharField(label='نام کاربری', max_length=150)  # Persian label
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)  # Persian label
    password_confirm = forms.CharField(label='تایید رمز عبور', widget=forms.PasswordInput)  # Persian label
    phone = forms.CharField(label='شماره تلفن', max_length=11)  # Persian label

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        # Validation logic for username
        if not fullname.isalnum():
            raise ValidationError("نام کاربری باید فقط شامل حروف و اعداد باشد.")
        if User.objects.filter(fullname=fullname).exists():
            raise ValidationError("نام کاربری وارد شده قبلا ثبت شده است.")
        return fullname

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        # Check for valid phone number format
        if len(phone) != 11 or not phone.isdigit():
            raise ValidationError(_("لطفا شماره تماس معتبر وارد کنید."))

            # Check for uniqueness
        if User.objects.filter(phone=phone).exists():  # Replace 'YourModel' with the relevant model
            raise ValidationError(_("این شماره تماس قبلاً ثبت شده است."))

        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "رمز عبور با تایید رمز عبور مطابقت ندارد.")

    def __init__(self, *args, **kwargs):
        super(FormRegister, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                                                       'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5'})


class PasswordChanged(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5',
                'placeholder': 'کلمه عبور فعلی',
            }
        ),
        error_messages={
            'required': 'لطفا کلمه عبور فعلی خود را وارد کنید',
        },
    )
    new_password1 = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5',
                'placeholder': 'کلمه عبور جدید',
            }
        ),
        error_messages={
            'required': 'لطفا کلمه عبور جدید خود را وارد کنید',
        },
        validators=[
            MinLengthValidator(8, message='کلمه عبور باید حداقل ۸ کاراکتر داشته باشد'),
            RegexValidator(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
                message='کلمه عبور باید حداقل یک حرف کوچک، یک حرف بزرگ و یک عدد داشته باشد',
            ),
        ],
    )
    new_password2 = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5',
                'placeholder': 'تکرار کلمه عبور جدید',
            }
        ),
        error_messages={
            'required': 'لطفا تکرار کلمه عبور جدید خود را وارد کنید',
        },
        validators=[
            MinLengthValidator(8, message='تکرار کلمه عبور باید حداقل ۸ کاراکتر داشته باشد'),
            RegexValidator(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
                message='تکرار کلمه عبور باید حداقل یک حرف کوچک، یک حرف بزرگ و یک عدد داشته باشد',
            ),
        ],
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', 'کلمه عبور جدید و تکرار آن یکسان نیستند')


class FormLogin(forms.Form):
    fullname = forms.CharField(label='نام کاربری', max_length=150)
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    phone = forms.CharField(label='شماره تلفن', max_length=11, required=False)

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-input w-full h-11!ring-0!ring-offset-0 bg-secondary border-border '
                         'focus:border-border rounded-xl text-sm text-foreground px-5'
            })

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        phone = cleaned_data.get('phone')
        fullname = cleaned_data.get('fullname')
        if not self.validate_phone(phone):
            self.add_error('phone', "شماره تلفن معتبر نیست.")  # Phone number is incorrect
        try:
            user = User.objects.get(phone=phone, fullname=fullname)
            if not user.check_password(password):
                self.add_error('password', "رمز عبور اشتباه است.")  # Password is incorrect
        except User.DoesNotExist:
            self.add_error('phone', "شماره تلفن یا نام کاربری اشتباه است.")
            return cleaned_data

    def validate_phone(self, phone):
        # Add your phone number validation logic here
        # For example, you can check if the phone number is a valid Iranian phone number
        if len(phone) != 11 or not phone.isdigit() or not phone.startswith('09'):
            return False
        return True

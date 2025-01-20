from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from apps.managers.forms import ManagerRegisterForm
from apps.managers.models import Manager
from apps.master.helpers.unique import *


class AuthViews:
    @staticmethod
    def register(request):
        if request.method == 'POST':
            register_data = ManagerRegisterForm(request.POST)
            if register_data.is_valid():
                first_name_ = register_data.cleaned_data.get('first_name')
                last_name_ = register_data.cleaned_data.get('last_name')
                email_ = register_data.cleaned_data.get('email')
                phone_ = register_data.cleaned_data.get('phone')
                password_ = register_data.cleaned_data.get('password')
                confirm_password_ = register_data.cleaned_data.get('confirm_password')

                print(settings.EMAIL_HOST_USER)
                # Save the data to the database
                new_manager = Manager.objects.create(
                    first_name=first_name_,
                    last_name=last_name_,
                    email=email_,
                    phone=phone_,
                    password=make_password(password_)
                )
                new_manager.save()

                # Send OTP to the registered email
                otp_ = generate_otp()
                subject = 'DL91 - OTP Verification'
                message = f"""
                Dear {first_name_} {last_name_},
                
                Your OTP for DL91 registration is: {otp_}"""
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [f'{email_}']
                )
                new_manager.otp = otp_
                new_manager.save()
                messages.success(request, 'Registration successful. Please check your email for OTP verification.')
                return render(request, 'dashboard/email_verification.html', {'email': email_})
            else:
                error_messages = [str(error) for errors in register_data.errors.values() for error in errors]
                for error in error_messages:
                    messages.error(request, error)
                    return redirect('register')

        register_form = ManagerRegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'dashboard/register.html', context)
    
    def verify_email(request):
        otp_ = request.POST['otp']
        email_ = request.POST['email']

        get_manager = Manager.objects.filter(email=email_).first()

        if not otp_:
            messages.error(request, 'No OTP provided. Please try again.')
            return render(request, 'dashboard/email_verification.html', {'email': email_})
        else:
            if not get_manager.otp == otp_:
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'dashboard/email_verification.html', {'email': email_})
            else:
                get_manager.is_active = True
                get_manager.save()
                messages.success(request, 'Email verification successful. You can now login.')
                return redirect('login')
            
    def login(request):
        if request.method == 'POST':
            email_ = request.POST['email']
            password_ = request.POST['password']

            get_manager = Manager.objects.filter(email=email_).first()
            
            if get_manager and get_manager.is_active:
                is_valid = check_password(password_, get_manager.password)
                if is_valid:
                    # Create session
                    request.session['manager_id'] = str(get_manager.dl91_id)
                    request.session['manager_name'] = f"{get_manager.first_name} {get_manager.last_name}"
                    # Redirect to dashboard
                    return redirect('dashboard')
                    # Login successful
                    messages.success(request, 'Login successful.')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid password. Please try again.')
            else:
                messages.error(request, 'Account not found or inactive. Please try again.')
                return redirect('login')
        return render(request, 'dashboard/login.html')

    def logout(request):
        request.session.clear()
        messages.success(request, 'Logout successful.')
        return redirect('login')


class DashboardViews:
    def dashboard(request):
        return render(request, 'dashboard/dashboard.html')
    


# from django.http import HttpResponse

    # Define your views here.
    # def dashboard(request):
    #     events = [
    #         {
    #             'id': 1,
    #             'title': 'Event 1',
    #             'date': '2022-01-01',
    #             'location': 'Location 1',
    #             'artist': 'artist 1'
    #         },
    #         {
    #             'id': 2,
    #             'title': 'Event 2',
    #             'date': '2022-02-01',
    #             'location': 'Location 2'
    #         }
    #     ]
    #     return HttpResponse(events[1]['title'])

    # def events(request):
    #     return HttpResponse("This is a events view")

    # def artists(request):
    #     return HttpResponse("This is a artists view")


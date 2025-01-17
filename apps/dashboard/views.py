from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from apps.managers.forms import ManagerRegisterForm
from apps.managers.models import Manager


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
                # Save the data to the database
                new_manager = Manager.objects.create(
                    first_name=first_name_,
                    last_name=last_name_,
                    email=email_,
                    phone=phone_,
                    password=make_password(password_)
                )
                new_manager.save()
                messages.success(request, "Registration successfully completed!")
                return redirect('register')
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


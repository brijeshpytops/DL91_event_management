from django.shortcuts import render

from apps.managers.forms import ManagerRegisterForm


class AuthViews:
    def register(request):
        if request.method == 'POST':
            pass
        register_form = ManagerRegisterForm()
        context = {
            'register_form':register_form
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


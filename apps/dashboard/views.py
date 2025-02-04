from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse

from apps.managers.forms import ManagerRegisterForm, VenueForm, RequiredThingForm
from apps.managers.models import Manager, Venue, RequiredThing
from apps.artist.models import Artist
from apps.master.helpers.unique import *
from apps.events.forms import EventForm
from apps.events.models import Event

from functools import wraps
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch

import qrcode
import zipfile

# provide me decorator for authenticated view: login_required
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'manager_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not logged in. Please log in to access the dashboard.')
            return redirect('login')
    return wrapper

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

    def forgot_password(request):
        if request.method == 'POST':
            email_ = request.POST['email']
            get_manager = Manager.objects.filter(email=email_).first()
            if get_manager:
                # send email with forgot password link with manager id
                subject = 'DL91 - Forgot Password link'
                message = f"""
                Dear {get_manager.first_name} {get_manager.last_name},

                Click on the link below to reset your password:
                http://localhost:8000/reset-password/{str(get_manager.dl91_id)}
                                
                """
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [f'{email_}']
                )
                messages.success(request, 'Check your email for link for password reset.')
                return redirect('login')
            else:
                messages.error(request, 'Account not found. Please try again.')
                return redirect('forgot_password')
        return render(request, 'dashboard/forgot-password.html')

    def reset_password(request, manager_id):
        manager = Manager.objects.filter(dl91_id=manager_id).first()
        if request.method == 'POST':
            new_password_ = request.POST['new_password']
            confirm_password_ = request.POST['confirm_password']
            if new_password_ == confirm_password_:
                print(new_password_, confirm_password_)
                manager.password = make_password(new_password_)
                manager.save()
                messages.success(request, 'Password reset successful.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match. Please try again.')
                return redirect('reset_password', manager_id=manager_id)
        return render(request, 'dashboard/reset_password.html', {'manager_id': manager_id})

    def logout(request):
        request.session.clear()
        messages.success(request, 'Logout successful.')
        return redirect('login')


class DashboardViews:
    @login_required
    def dashboard(request):
        return render(request, 'dashboard/dashboard.html')
    
    @login_required
    def events(request):
        manager_id_ = request.session.get('manager_id')  # Get the manager_id from the session
        if not manager_id_:
            messages.error(request, 'Manager not found in session. Please log in again.')
            return redirect('login')  # Redirect to the login page if no manager_id

        events = Event.objects.filter(manager_id=manager_id_)  # Fetch events for the manager

        if request.method == "POST":
            form = EventForm(request.POST, request.FILES)

            if form.is_valid():
                event = form.save(commit=False)
                event.manager_id = manager_id_  # Assign the manager_id to the event
                event.save()
                messages.success(request, 'Event created successfully!')
                return redirect('events')  # Redirect to refresh the page
            else:
                print(form.errors)  # Log form errors for debugging
                messages.error(request, 'Error creating event. Please try again.')
                return redirect('events')
        else:
            form = EventForm()

        print(events)
        context = {'form': form, 'events': events, 'manager_id': manager_id_}
        return render(request, 'dashboard/events.html', context)

    @login_required
    def generate_event_tickets(request, event_id):
        event = Event.objects.get(dl91_id=event_id)
        
        # Get ticket count from GET request (default 100)
        ticket_count = int(request.GET.get('ticket_count', 100))

        # Create a ZIP file buffer
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i in range(1, ticket_count + 1):  # Generate tickets dynamically
                ticket_buffer = BytesIO()
                pdf = canvas.Canvas(ticket_buffer, pagesize=letter)
                width, height = letter

                # Full Blue Background
                pdf.setFillColor(colors.HexColor("#3b1c32"))  # Dark Blue
                pdf.rect(0, 0, width, height, fill=True, stroke=False)

                # White Ticket Container
                ticket_width, ticket_height = 7.5 * inch, 3.5 * inch
                ticket_x, ticket_y = (width - ticket_width) / 2, (height - ticket_height) / 2
                pdf.setFillColor(colors.white)
                pdf.roundRect(ticket_x, ticket_y, ticket_width, ticket_height, 10, fill=True, stroke=False)

                # Event Image
                if event.event_image:
                    img = ImageReader(event.event_image.path)
                    pdf.drawImage(img, ticket_x + 0.5 * inch, ticket_y + ticket_height - 2.5 * inch, width=1.5 * inch, height=1.5 * inch)

                # Title & Event Details
                pdf.setFillColor(colors.black)
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawString(ticket_x + 2.2 * inch, ticket_y + ticket_height - 1.0 * inch, event.event_name)

                pdf.setFont("Helvetica", 12)
                pdf.drawString(ticket_x + 2.2 * inch, ticket_y + ticket_height - 1.4 * inch, f"Date: {event.event_date}")
                pdf.drawString(ticket_x + 2.2 * inch, ticket_y + ticket_height - 1.7 * inch, f"Time: {event.event_start_time} - {event.event_end_time}")
                pdf.drawString(ticket_x + 2.2 * inch, ticket_y + ticket_height - 2.0 * inch, f"Venue: {event.venue}")
                pdf.drawString(ticket_x + 2.2 * inch, ticket_y + ticket_height - 2.3 * inch, f"Artist: {event.artist}")

                # Generate QR Code
                ticket_code = f"{event.dl91_id}{i:05d}"  # Unique ticket code (EVT00001, EVT00002, ...)
                qr_data = f"Event: {event.event_name}\nDate: {event.event_date}\nTime: {event.event_start_time} - {event.event_end_time}\nVenue: {event.venue}\nArtist: {event.artist}\nTicket Code: {ticket_code}"
                qr = qrcode.make(qr_data)
                qr_buffer = BytesIO()
                qr.save(qr_buffer, format="PNG")
                qr_buffer.seek(0)
                qr_image = ImageReader(qr_buffer)

                # Draw QR Code
                pdf.drawImage(qr_image, ticket_x + ticket_width - 1.8 * inch, ticket_y + 1 * inch, width=1.5 * inch, height=1.5 * inch)

                # Ticket Code
                pdf.setFont("Helvetica-Bold", 14)
                pdf.setFillColor(colors.HexColor("#ffcc00"))  # Yellow Ticket Code
                pdf.drawString(ticket_x + 1 * inch, ticket_y + 0.6 * inch, f"Ticket Code: {ticket_code}")

                # Save PDF
                pdf.showPage()
                pdf.save()

                # Save PDF to ZIP
                ticket_buffer.seek(0)
                zip_file.writestr(f"ticket_{ticket_code}.pdf", ticket_buffer.getvalue())

        # Return ZIP file
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="event_tickets_{event.event_name}.zip"'
        return response
    
    @login_required
    def artists(request):
        if request.method == 'POST':
            manager_id_ = request.session['manager_id']
            profile_picture_ = request.FILES.get('profile_picture')
            stage_name_ = request.POST['stage_name']
            artist_fields_ = request.POST['artist_fields']
            contact_ = request.POST['contact']
            instagram_profile_link_ = request.POST['instagram_profile_link']
            spotify_link_ = request.POST['spotify_link']
            artist_charge_ = request.POST['artist_charge']
            description_ = request.POST['description']

            print(
                manager_id_,
                profile_picture_,
                stage_name_,
                artist_fields_,
                contact_,
                instagram_profile_link_,
                spotify_link_,
                artist_charge_,
                description_)

            new_artist = Artist.objects.create(
                manager_id=manager_id_,
                profile_picture=profile_picture_,
                stage_name=stage_name_,
                artist_fields=artist_fields_,
                contact=contact_,
                instagram_profile=instagram_profile_link_,
                spotify_link=spotify_link_,
                artist_charge=artist_charge_,
                description=description_
            )
            new_artist.save()
            messages.success(request, 'Artist added successfully.')
            return redirect('artists')
        
        # Get artists based on the manager's ID from the session
        artists = Artist.objects.filter(manager_id=request.session['manager_id']).order_by('-created_at')

        # Get total artist count
        total_artist = artists.count()

        # Paginate the artist list
        paginator = Paginator(artists, 5)  # 5 artists per page
        page_number = request.GET.get('page', 1)

        try:
            artists = paginator.page(page_number)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            artists = paginator.page(1)

        # Pass both artists and total_artist to the context
        context = {
            'artists': artists,
            'total_artist': total_artist
        }
        return render(request, 'dashboard/artists.html', context)

    @login_required
    def view_artist(request, artist_id):
        get_artist = Artist.objects.filter(dl91_id=artist_id).first()
        if get_artist:
            # Pass the artist to the context
            context = {
                'artist': get_artist
            }
            return render(request, 'dashboard/artist_view.html', context)
        else:
            messages.error(request, 'Artist not found.')
            return redirect('artists')

    @login_required
    def edit_artist(request, artist_id):
        get_artist = Artist.objects.filter(dl91_id=artist_id).first()

        if request.method == 'POST':
            # Update fields from form inputs
            get_artist.stage_name = request.POST.get('stage_name', get_artist.stage_name)
            get_artist.contact = request.POST.get('contact', get_artist.contact)
            get_artist.artist_charge = request.POST.get('artist_charge', get_artist.artist_charge)
            
            # Handle profile picture update
            if 'profile_picture' in request.FILES:
                get_artist.profile_picture = request.FILES['profile_picture']
            
            try:
                get_artist.save()
                messages.success(request, "Artist updated successfully.")
            except Exception as e:
                messages.error(request, f"Error updating artist: {str(e)}")
            
            return redirect('artists')
        messages.error(request, "Invalid request method.")
        return redirect('artists')
        
    @login_required
    def delete_artist(request, artist_id):
        get_artist = Artist.objects.filter(dl91_id=artist_id).first()
        if get_artist:
            get_artist.delete()
            messages.success(request, 'Artist deleted successfully.')
            return redirect('artists')
        else:
            messages.error(request, 'Artist not found.')
            return redirect('artists')

    @login_required
    def venues_view(request):
        manager_id_ = request.session['manager_id']
        venues = Venue.objects.filter(manager_id=manager_id_)
        if request.method == "POST":
            form = VenueForm(request.POST)
            if form.is_valid():
                venue = form.save(commit=False)
                venue.manager_id = manager_id_
                venue.save()
                messages.success(request, 'Venue created successfully!')
                return redirect('venues_view')
        form = VenueForm()
        return render(request, 'dashboard/venues.html', {'form': form,'venues': venues})

    @login_required
    def things_view(request):
        manager_id_ = request.session['manager_id']
        things = RequiredThing.objects.filter(manager_id=manager_id_)
        if request.method == "POST":
            form = RequiredThingForm(request.POST)
            if form.is_valid():
                thing = form.save(commit=False)
                thing.manager_id = manager_id_
                thing.save()
                messages.success(request, 'Thing created successfully!')
                return redirect('things_view')
        form = RequiredThingForm()
        return render(request, 'dashboard/things.html', {'form': form, 'things': things})

    @login_required
    def profile(request):
        return render(request, 'dashboard/profile.html')
    


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


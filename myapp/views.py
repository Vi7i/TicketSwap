from django.shortcuts import render,redirect
from myapp.models import *
from django.conf import settings
from django.contrib import messages
import string
import random
from django.utils import timezone
from datetime import *
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone as django_timezone
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .apps import MyappConfig
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from django.utils import timezone
import pytz



def startpage(request):
    return render(request,'startpage.html')

@csrf_exempt
def verify_email(request):
    if request.method=="POST":
        email=request.POST.get('emailid')
       
       
        def generate_random_string(length=8):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(length))
            return random_string
        token=generate_random_string()
        confirm=emailverification.objects.filter(email=email)
        print(token,confirm)
        if not confirm:
            emailverification.objects.create(email=email,token=token)
            reset_url = f"{request.scheme}://{request.get_host()}/register1/{email}/{token}/"
            send_mail(
                    'Email verification',
                    f'Please click the following link to verify your email: {reset_url}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            messages.success(request, 'An email has been sent with instructions to verify your email.')
        elif confirm:
            veri=User.objects.filter(email=email)
            if veri:
                messages.error(request, 'This account is already registered.')
                return render(request,"verify_email.html")
            else:
                obj2=emailverification.objects.get(email=email)
                obj2.token=token
                obj2.save()
                
                print("yes",token,email)
                reset_url = f"{request.scheme}://{request.get_host()}/register1/{email}/{token}/"
                send_mail(
                    'Email verification',
                    f'Please click the following link to verify your email: {reset_url}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'An email has been sent with instructions to verify your email.')
            return render(request,"verify_email.html")
    return render(request,"verify_email.html")



@csrf_exempt
def confirmedemail(request,email,token):
    confirm=emailverification.objects.get(email=email,token=token)
    if confirm:
         if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            pass1 = request.POST.get("pass1")
            pass2 = request.POST.get("pass2")
            location=request.POST.get("location")
            phonenumber=request.POST.get("phone")
            if pass1 == pass2:
                print(name,email,pass1,pass2,location,phonenumber)
                user = User.objects.create_user(username=name, email=email, password=pass1,location=location,phonenumber=phonenumber)
                user.is_user = True
                user.save() 
                return redirect("login")
            else:
                messages.error(request,"incorrect")
         return render(request, "register.html",{'email':email})





@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('emailid')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('reset_password')

        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = default_token_generator.make_token(user)
        print(uid,token)
        reset_url = f"{request.scheme}://{request.get_host()}/reset_password_confirm/{uid}/{token}/"
        send_mail(
            'Password reset',
            f'Hello {user.username} Please click the following link to reset your password: {reset_url} By Team White|Ticket',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, 'An email has been sent with instructions to reset your password.')
        return redirect('reset_password')

    return render(request, 'reset_password.html')

@csrf_exempt
def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print(uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid token.')
        return redirect('login')
        
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')

            if password1 == password2:
                user.set_password(password1)
                user.save()
                return redirect('login')

            else:
                messages.error(request, 'Passwords do not match.')

        return render(request, 'new_password.html')

    else:
        messages.error(request, 'Invalid token.')
        return redirect('login')
    

#login
@csrf_exempt
def login1(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("pass")
        user = authenticate(request, username=name, password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,f"successfully logged in as { request.user.username }")
            return redirect("home")
            
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")

@csrf_exempt
def home(request):
    if hasattr(request.user, "is_user") and request.user.is_user:
        if request.method == 'POST':
            # ✅ Ticket Upload Form
            if 'upload_form' in request.POST:
                ticket_name = request.POST.get("ticket_name")
                ticket_quantity = request.POST.get("ticket_quantity")
                ticket_price = request.POST.get("ticket_price")
                doe_str = request.POST.get("doe")
                type = request.POST.get("ticket_type")
                image = request.FILES.get("ticket-image")

                # Parse datetime and make timezone-aware
                try:
                    doe_datetime = datetime.strptime(doe_str, '%Y-%m-%dT%H:%M')
                    doe_aware = django_timezone.make_aware(doe_datetime, pytz.utc)
                except Exception as e:
                    messages.error(request, f"Invalid date format: {e}")
                    return HttpResponseRedirect(request.path_info)

                # ✅ Validate uploaded image or PDF
                if image:
                    if not (image.content_type.startswith('image/') or image.content_type == 'application/pdf'):
                        messages.error(request, 'Only image or PDF files are allowed.')
                        return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, 'Please upload an image or PDF file.')
                    return HttpResponseRedirect(request.path_info)

                # ✅ Create ticket with image
                Ticket.objects.create(
                    ticket_name=ticket_name,
                    number_of_tickets=ticket_quantity,
                    price=ticket_price,
                    date_of_expiry=doe_aware,
                    type=type,
                    image=image,
                    uploaded_by=request.user,
                )
                messages.success(request, "Successfully uploaded a ticket.")
                return HttpResponseRedirect(request.path_info)

            # ✅ Contact Form
            if 'contact_form' in request.POST:
                query = request.POST.get("queries")
                Contact.objects.create(queries=query, query_by=request.user)
                messages.success(request, "Successfully sent a query.")
                return HttpResponseRedirect(request.path_info)

        # GET request
        from django.utils.timezone import localtime
        india_tz = pytz.timezone('Asia/Kolkata')
        current_datetime = localtime(django_timezone.now(), india_tz).strftime('%Y-%m-%dT%H:%M')
        return HttpResponse(render(request, 'user_dashboard.html', {'current_datetime': current_datetime}))
    # Always return an HttpResponse for all code paths
    return HttpResponseRedirect("/login")

    
def profile(request):
    if request.method=="POST":
        profile_img = request.FILES.get("profile")
        bio=request.POST.get("bio")
        user=User.objects.get(pk=request.user.id)
        if profile_img:
            user.profile=profile_img
        user.about=bio
        print(bio,profile_img)
        user.save()
        messages.success(request,f"Profile Updated")
        return redirect('home')
    return render(request,"profile.html")


def profile_view(request,id):
    user=User.objects.get(pk=id)
    return render(request,'profile_view.html')

@csrf_exempt
@csrf_exempt
def all_tickets(request):
    if request.method == "GET":
        all_tickets = Ticket.objects.all()
        all_ticket_list = []
        current_utc_timestamp = django_timezone.now()  # Ensure correct timezone handling

        for ticket in all_tickets:
            expiry_timestamp = ticket.date_of_expiry

            # Ensure expiry time is aware (convert if needed)
            if expiry_timestamp.tzinfo is None or expiry_timestamp.tzinfo.utcoffset(expiry_timestamp) is None:
                expiry_timestamp = django_timezone.make_aware(expiry_timestamp, pytz.utc)

            # Debug print
            print(f"Checking ticket: {ticket.ticket_name}, Expiry: {expiry_timestamp}, Current Time: {current_utc_timestamp}")

            if expiry_timestamp > current_utc_timestamp and ticket.number_of_tickets > 0:
                all_ticket_list.append({
                    'id': ticket.id,
                    'name': ticket.ticket_name,
                    'quantity': ticket.number_of_tickets,
                    'price': ticket.price,
                    'type': ticket.type,
                    'expiry_date': expiry_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })

        return JsonResponse(all_ticket_list, safe=False)


@csrf_exempt           
def book(request,ticket_id):
    ticket=Ticket.objects.get(id=ticket_id)
    if ticket:
        if request.method=="POST":
            quantity=int(request.POST.get("quantity"))
            total_price=quantity*ticket.price
            if ticket.number_of_tickets >0:
                updated=int(ticket.number_of_tickets)-int(quantity)
                ticket.number_of_tickets=updated
                ticket.save()
            book=Book.objects.create(ticket=ticket,booked_by=request.user,total_price=total_price,total_tickets=quantity)
            messages.success(request,f"successfully booked check status on mybooks")
            return redirect("home")
    return render(request,"book.html",{'ticket':ticket})


@csrf_exempt
def complaint(request,ticket_id):
    ticket=Ticket.objects.get(id=ticket_id)
    if request.method=="POST":
        ticket_name=request.POST.get("ticket_name")
        uploaded_by=request.POST.get("uploaded_by")
        complaint_by=request.POST.get("complaint_by")
        ticket_price=request.POST.get("ticket_price")
        actual_price=request.POST.get("actual_price")
        print(ticket_price,ticket_name,uploaded_by,complaint_by,actual_price)
        Complaint.objects.create(ticket_name=ticket_name,uploaded_by=uploaded_by,complaint_by=complaint_by,ticket_price=ticket_price,actual_price=actual_price)
        messages.success(request,f"successfully sent a complaint against that ticket")
        return redirect("home")
    return render(request,"complaint.html" ,{"ticket":ticket})




import razorpay
from ticketswap.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRETKEY


client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRETKEY))
client.set_app_details({"title": "users", "version": MyappConfig.version})

def my_books(request):
    mybook=Book.objects.filter(booked_by=request.user)
    return render(request,'mybooks.html',{'mybook':mybook})

def payment(request,bookedid):
    book=Book.objects.get(pk=bookedid)
    amount_in_paisa = int(book.total_price * 100)
    if book:
        DATA = {
        "amount": amount_in_paisa,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        },
        'payment_capture':'1',

        }
    
        payment1=client.order.create(data=DATA)
        order_id = payment1['id']
        ob = book.ticket
        ph=ob.uploaded_by.phonenumber
        
        context = {
        'amount': amount_in_paisa,
        'api_key': RAZORPAY_API_KEY,
        'order_id': order_id,
        'id1':bookedid,
        'ph': ph,
        }
        return render(request,"payment.html",context)

@csrf_exempt
def thankyou(request,bookedid):
    payment1=Book.objects.get(pk=bookedid)
    if payment1:
        payment1.payment=True
        payment1.save()
        messages.success(request,"payment successfull")
        # Render thankyou page with auto download script
        return render(request,'thankyou.html', {'bookedid': bookedid})
    return render(request,'thankyou.html')


def view_uploads(request):
    tickets=Ticket.objects.filter(uploaded_by=request.user)
    print(tickets)
    l=[]
    for ticket in tickets:
        print(ticket.id)
        book=Book.objects.filter(ticket=ticket.id)
        
        if book:
            l.append(book)
    print(l)
    return render(request,"view_uploads.html",{'tickets':l})


def delete_user(request,id):
    if request.method=="POST":
        user=User.objects.get(id=id)
        if user:
            user.delete()
            return redirect("home")
        
@login_required        
def approve_user(request, user_id):
    # Ensure only staff/admins can approve users
    if not request.user.is_staff:
        raise PermissionDenied

    user = get_object_or_404(User, id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, f"User {user.username} has been approved successfully!")
    return redirect('home')

def delete_complaint(request,id):
    if request.method=="POST":
        complaint=Complaint.objects.get(id=id)
        if complaint:
            complaint.delete()
            return redirect("home")

def delete_ticket(request,id):
    if request.method=="POST":
        ticket=Ticket.objects.get(id=id)
        if ticket:
            ticket.delete()
            return redirect("home")

from django.http import FileResponse, Http404, HttpResponseRedirect, HttpResponse
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import weasyprint

def logoutuser(request):
    logout(request)
    return redirect("login")

@login_required
def download_ticket(request, bookedid):
    try:
        booking = Book.objects.get(pk=bookedid, booked_by=request.user)
    except Book.DoesNotExist:
        raise Http404("Booking does not exist")

    if not booking.payment:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # Render ticket PDF
    html_string = render_to_string('ticket_pdf.html', {'booking': booking, 'request': request})
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf_file = html.write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    filename = f"ticket_{booking.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
    return response

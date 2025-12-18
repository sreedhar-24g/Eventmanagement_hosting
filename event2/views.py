from django.shortcuts import render,redirect
from .models import booking, Donation
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail


# Create your views here.
def homepage(request):
    return render(request,'home-page.html')


def signup(request):
    if request.method == 'POST':
        a= request.POST.get('first_name')
        b= request.POST.get('last_name')
        c= request.POST.get('username')
        d= request.POST.get('email')
        e= request.POST.get('password')
        f= request.POST.get('password1')

        if User.objects.filter(username=c).exists():
            messages.info(request,'Username already taken')
            return redirect('signup')

        user = User.objects.create(
            first_name=a,
            last_name=b,
            username=c,
            email=d
        )
        if e!=f:
            messages.info(request,'Password do not match')
            return redirect('signup')
        
        user.set_password(e)
        user.save()
        messages.info(request,'Signup Successful')
        return redirect('signin')
    
    return render (request,'signup.html')

def signin(request):
    if request.method=="POST":
        a= request.POST.get('username')
        b= request.POST.get('password')

        if not User.objects.filter(username=a).exists():
            messages.info(request,'Invalid Username')
            return redirect('signin')
        user = authenticate(username=a, password=b)

        if user is None:
            messages.info(request,'Invalid Password')
            return redirect('signin')
        else:
            login(request,user)
            return redirect('dashboard')
            

            
    return render(request,'signin.html')

@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'index.html') 

@login_required(login_url='signin')
def send_email(request):
    if request.method == "POST":
        receiver_email = request.POST['email']

        send_mail(
            "Get in touch message",
            "This is an email from Django.",
            settings.EMAIL_HOST_USER,
            [receiver_email],
            fail_silently=False,  
        )

        messages.success(request, "Email sent successfully!")
        return redirect('dashboard')

    return redirect('dashboard')
 
@login_required(login_url='signin')
def event(request):

    return render(request, 'events.html' ) 

@login_required(login_url='signin')
def services(request):
    return render(request, 'services.html') 

@login_required(login_url='signin')
def testimonials(request):
    return render(request, 'testimonials.html') 

@login_required(login_url='signin')
def contact(request):
    return render(request, 'contact.html') 

@login_required(login_url='signin')
def profile(request):
    user_profile = request.user.userprofile

    if request.method == "POST":
        if "delete_pic" in request.POST:
            user_profile.profile_pic.delete()
            user_profile.profile_pic = None
            user_profile.save()
            messages.success(request, "Profile picture deleted!")
            return redirect("profile")

        user_profile.phone = request.POST.get("phone")
        user_profile.address = request.POST.get("address")
        user_profile.about = request.POST.get("about")

        if "profile_pic" in request.FILES:
            user_profile.profile_pic = request.FILES["profile_pic"]

        user_profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "profile.html", {"user_profile": user_profile})

@login_required(login_url='signin')
def learnmore1(request):
    return render(request, 'learn_more_1.html')

@login_required(login_url='signin')
def learnmore2(request):
    return render(request, 'learn_more_2.html')

@login_required(login_url='signin')
def learnmore3(request):
    return render(request, 'learn_more_3.html') 

@login_required(login_url='signin')
def donate(request):
    return render(request, 'donate.html') 

@login_required(login_url='signin')
def process_donation(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = int(request.POST.get('amount', 0))
        payment_method = request.POST.get('payment_method')
        upi_app = request.POST.get('upi_app')
        upi_id = request.POST.get('upi_id')

        
        if amount % 500 != 0:
            messages.error(request, "Donation amount must be in multiples of ₹500.")
            return redirect('donate')

       
        donation = Donation.objects.create(
            user=request.user,
            name=name,
            email=email,
            amount=amount,
            payment_method=payment_method,
            upi_app=upi_app if payment_method == 'UPI' else None,
            upi_id=upi_id if payment_method == 'UPI' else None,
        )
        donation.save()

        messages.success(request, f"Thank you, {name}! Your donation of ₹{amount} has been received successfully.")
        return redirect('dashboard')

    return redirect('donate')

@login_required(login_url='signin')
def booking_view(request):
    mydata=booking.objects.filter(user=request.user)
    
    if request.method=="POST":
        
        a11=request.POST['event_name']
        a12=request.POST['event_type']
        a13=request.POST['date']
        a14=request.POST['guest_count']
        a15=request.POST['venue']
        a16=request.POST['description']

        obj=booking(user=request.user,eventname=a11,event_type=a12,date=a13,guest_count=a14,venue=a15,description=a16)
        obj.save()
        return redirect('myevents')
    
    return render(request,'events.html',{'data': mydata})

@login_required(login_url='signin')
def myevents(request):
    today = date.today()
    search_query=request.GET.get('search','')

    events=booking.objects.filter(user=request.user)

    if search_query:
        events = events.filter(event_type__icontains=search_query)
    
    event_types = [choice[0] for choice in booking.EVENT_TYPE_CHOICES]

    upcoming_events = booking.objects.filter(user=request.user, date__gte=today).order_by('date')
    past_events = booking.objects.filter(user=request.user, date__lt=today).order_by('-date')

    for event in upcoming_events:
        event.days_left = (event.date - today).days


    return render(request, 'my_events.html', {'upcoming_events': upcoming_events,'past_events': past_events,'today': today,'search_query': search_query,
        'event_types': event_types}) 



@login_required(login_url='signin')
def search_event(request):
    today = date.today()
    search_query=request.GET.get('search','')

    events=booking.objects.filter(user=request.user)

    if search_query:
        events = events.filter(event_type__icontains=search_query)
    
    event_types = [choice[0] for choice in booking.EVENT_TYPE_CHOICES]


    upcoming_events = events.filter(user=request.user, date__gte=today).order_by('date')
    past_events = events.filter(user=request.user, date__lt=today).order_by('-date')

    for event in upcoming_events:
        event.days_left = (event.date - today).days

    return render(request, 'my_events_search.html', {'upcoming_events': upcoming_events,'past_events': past_events,'today': today,'search_query': search_query,
        'event_types': event_types}) 




@login_required(login_url='signin')
def UpdateData(request,id):
    mydata=booking.objects.get(id=id)
    if request.method=="POST":
        a11=request.POST['event_name']
        a12=request.POST['event_type']
        a13=request.POST['date']
        a14=request.POST['guest_count']
        a15=request.POST['venue']
        a16=request.POST['description']

        mydata.eventname=a11
        mydata.event_type=a12
        mydata.date=a13
        mydata.guest_count=a14
        mydata.description=a15
        mydata.venue=a16
        mydata.save()
        return redirect('event')
    return render(request,'update_event.html',{'data': mydata})

@login_required(login_url='signin')
def DeleteData(request,id):
    mydata=booking.objects.get(id=id)
    mydata.delete()
    return redirect('myevents')


def signout(request):
    logout(request)
    return redirect('signin')


"""
URL configuration for eventmanagement_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from event2 import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage, name='home'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/',views.send_email,name='send_email'),
    path('event/',views.event,name='event'),
    path('services/',views.services,name='services'),
    path('testimonials/',views.testimonials,name='testimonials'),
    path('contact/',views.contact,name='contact'),
    path('profile/',views.profile,name='profile'),
    path('signout/',views.signout,name='signout'),
    path('booking/',views.booking_view,name='booking'),
    path('myevents/',views.myevents,name='myevents'),
    path('learnmore_1',views.learnmore1,name='learnmore1'),
    path('learnmore_2',views.learnmore2,name='learnmore2'),
    path('learnmore_3',views.learnmore3,name='learnmore3'),
    path('donate',views.donate,name='donate'),
    path('process_donation/', views.process_donation, name='process_donation'),
    path('myevents_search/',views.search_event,name='searchevent'),
    path('UpdateData/<int:id>',views.UpdateData, name='UpdateData'),
    path('deletedata/<int:id>',views.DeleteData, name='DeleteData'),
    path('accounts/', include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

import time
import calendar
from datetime import date, datetime, timedelta
import datetime
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core import mail
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib import messages
from TrackaTruck.models import *
from Project.email_info import EMAIL_HOST_USER
from django.db import models
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from TrackaTruck.forms import TruckForm
from TrackaTruck.forms import TrailerForm
from TrackaTruck.forms import RecordForm
from TrackaTruck.forms import TruckMaintenanceForm


# Create your views here.
monthNames = "January February March April May June July August September October November December"
monthNames = monthNames.split()
bankholiday = []
Holidays = ((1,1,"New Years Day"),(25,12,"Christmas Day"),(26,12,"Boxing Day"))
goodFriday = ""
easterMonday = ""
easterSunday = ""
celebDays  = []

def add_csrf(request, **kwargs):
    """Add csrf and user to dictionary."""
    cald = dict(user=request.user, **kwargs)
    cald.update(csrf(request))
    return cald

"""Holidays"""
def check_not_bank_holiday(mMonth, mDay):
     global Holidays
     for e in bankholiday:
          if e[0] == mDay and e[1] == mMonth: return 119
     for e in Holidays:
          if e[0] == mDay and e[1] == mMonth: return 119
     if goodFriday[0] == mDay and goodFriday[1] == mMonth: return 119
     if easterMonday[0] == mDay and easterMonday[1] == mMonth: return 119
     return 0
    
""" Get the Easter dates for given year """   
def calc_easter(year):
    global goodFriday
    global easterMonday
    global easterSunday
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    easterSunday = int(day), int(month), "Easter Sunday"
    if day == 1 or day == 2:
        for x in range(25,32):
            if(date(int(year),int(month)-1,x)).strftime("%A") == "Friday":
                goodFriday = int(x),int(month)-1, "Good Friday"
        easterMonday = int(day)+1, int(month), "Easter Monday"
    else:
        goodFriday = int(day)-2, int(month), "Good Friday"
        easterMonday = int(day)+1, int(month), "Easter Monday"

""" Check when Good Friday and Easter Monday fall """    
def checkEaster(mDay, mMonth, mYear):
    calc_easter(mYear)
    global goodFriday
    global easterMonday
    if mDay == int(goodFriday[0]) and mMonth == int(goodFriday[1]):
        return 4
    elif mDay == int(easterMonday[0]) and mMonth == int(easterMonday[1]):
        return 1
    return 0

""" Special dates not public holidays """
def get_celebratory_dates(mDay, mMonth, mYear):
    global celebDays
    celebDays= [ ]
    eSun = (date(mYear,mMonth,mDay))
    mSunday = eSun - timedelta(days=21)
    celebDays.append((mSunday.day,mSunday.month,"Mothers Day"))
    celebDays.append((14,2,"Valentines Day"))
    celebDays.append((11,11,"Armistice Day"))
    celebDays.append((25,1,"Burns Night" ))
    for z in range(8,15):
        if date(int(mYear),11,z).strftime("%A") == "Sunday":
            celebDays.append((z,11,"Rememberance Sunday"))
    for z in range(17,24):
        if date(int(mYear),6,z).strftime("%A") == "Sunday":
            celebDays.append((z,6,"Fathers Day"))
    for z in range(25,31):
        if date(int(mYear),3,z).strftime("%A") == "Sunday":
            celebDays.append((z,3,"BST Begins"))
    for z in range(25,31):
        if date(int(mYear),10,z).strftime("%A") == "Sunday":
            celebDays.append((z,10,"BST Ends"))


""" Calculate Bank Holidays """
def calc_bankholiday(year):
    global bankholiday
    bankholiday = []
    for x in range(1,8):
        if date(int(year),5,x).strftime("%A") == "Monday":   
            bankholiday.append((x,5,"May Day"))
    for y in range(25,32):
        if date(int(year),5,y).strftime("%A") == "Monday":
            bankholiday.append((y,5,"Bank Holiday"))            
    for z in range(25,32):
        if date(int(year),8,z).strftime("%A") == "Monday":
            bankholiday.append((z,8,"Bank Holiday"))
    if date(int(year),12,25).strftime("%A") == "Friday":
        bankholiday.append((28,12,"Bank Holiday"))    
    if date(int(year),12,25).strftime("%A") == "Saturday":
        bankholiday.append((26,12,"Boxing Day"))
        bankholiday.append((27,12,"Bank Holiday"))
        bankholiday.append((28,12,"Bank Holiday"))
    if date(int(year),12,25).strftime("%A") == "Sunday":
        bankholiday.append((26,12,"Boxing Day"))
        bankholiday.append((27,12,"Bank Holiday"))
    if date(int(year),1,1).strftime("%A") == "Saturday":
        bankholiday.append((3,1,"Bank Holiday"))
    elif date(int(year),1,1).strftime("%A") == "Sunday":
        bankholiday.append((2,1,"Bank Holiday"))

""" Check Bank Holidays """
def checkBholiday(mDay, mMonth, mYear):
    global bankholiday
    calc_bankholiday(mYear)
    for e in bankholiday:
        if mDay == e[0] and mMonth == e[1]:
            return 1
    return 0

""" Check Special day names """
def check_holiday_name(mDay, mMonth):
    hStr = " "
    if(mDay == 1 and mMonth == 1):
        hStr = "New Years Day"
    if(mDay == 14 and mMonth == 2):
        hStr = "Valentines Day"
    if(mDay == 1 and mMonth == 3):
        hStr = "St Davids Day"
    if(mDay == 17 and mMonth == 3):
        hStr = "St Patricks Day"
    if(mDay == 23 and mMonth == 4):
        hStr = "St Georges Day"
    if(mDay == 30 and mMonth == 11):
        hStr = "St Andrews Day"
    if(mDay == 24 and mMonth == 12):
        hStr = "Christmas Eve"
    if(mDay == 25 and mMonth == 12):
        hStr = "Christmas Day"
    if(mDay == 31 and mMonth == 12):
        hStr = "New Years Eve"
    return hStr


"""Index Page"""
def index (request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/index.html', {}, context)

"""Login"""
def login_view(request):
    context = RequestContext(request)
    username = password = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/welcome/')
            else:
                return HttpResponse("Your account is disabled, please contact us")
        else:
             return HttpResponseRedirect('/invalid/')

    else:
        return render(request, 'TrackaTruck/login.html', {}, context_instance=RequestContext(request))

"""Invalid Details"""    
def invalid(request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/invalid.html', {}, context)

"""Logout"""
@login_required    
def logout_view(request):
    logout(request)
    return render(request, 'TrackaTruck/logout.html')

"""Welcome Page"""
@login_required
def welcome(request):
    user_profile = request.user.profile.company_Name
    return render(request, 'TrackaTruck/welcome.html')

"""Add Truck Page"""
@login_required
def add_truck(request):
    if request.method == "POST":
        form = TruckForm(request.POST)
        
        if form.is_valid():
            truck = form.save(commit=False)
            truck.created_Date = timezone.now()
            truck.author = request.user
            truck.save()
            print('truck form ')
            send_mail('Re: Truck Added', 'Hi, \n You have added a new Truck to your account.\n Regards Track-A-Truck', 'trackatruck746@gmail.com',
                      [request.user.email], fail_silently=False)
            return redirect('/truck_list/')
    else:
        form = TruckForm()
    return render(request, 'TrackaTruck/addTruck.html', {'form' : form})  
            
"""Truck Records Page"""
@login_required
def truck_list(request):
    context = RequestContext(request)
    return render_to_response('TrackaTruck/truckList.html', {'obj': Truck.objects.all().order_by("year")}, context)

"""Add Trailer Page"""    
@login_required
def add_trailer(request):
    if request.method == "POST":
        form = TrailerForm(request.POST)
        
        if form.is_valid():
            trailer = form.save(commit=False)
            trailer.created_Date = timezone.now()
            trailer.author = request.user
            trailer.save()
            send_mail('Re: Trailer Added', 'Hi, \n You have added a new Trailer to your account. \n Regards Track-A-Truck', 'trackatruck746@gmail.com',
                      [request.user.email], fail_silently=False)
            return redirect('/trailer_list/')
    else:
        form = TrailerForm()
    return render(request, 'TrackaTruck/trailer.html', {'form' : form})

"""Trailer Records Page"""
def trailer_list(request):
    context = RequestContext(request)
    return render_to_response('TrackaTruck/trailerList.html', {'obj': Trailer.objects.all().order_by("trailer_Year")}, context )

"""Tracker Page"""
@login_required
def tracker(request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/tracker.html', {}, context)

"""Add Record Page"""
@login_required
def record(request, year, month, day):
    global nextYear, thisYear
    tDay = date.today()
    other_records = []
    RecordsFormset = modelformset_factory (Record, exclude=("author","date"), can_delete=True)
    other_records = Record.objects.filter(date__year=year,date__month=month, date__day=day)
    if request.method == "POST":
        print('print')
        result = RecordsFormset(request.POST)
        
        if result.is_valid():
            record = result.save(commit=False)
            for record in records:
                record.author = request.user
                record.date = date(int(year), int(month), int(day))
                record.created_Date = timezone.now()
                record.save()
            
                return HttpResponseRedirect('/calendar/')
    else:
        result = RecordsFormset(queryset=(Record.objects.filter(date__year=year,date__month=month, date__day=day)))
    return render(request, 'TrackaTruck/record.html',  dict(author=request.user,records=result, other_records=other_records,
                                                            day=day, month=month, year=year))

"""Calendar Year Page"""
@login_required
def year_View(request, year=None):
    global nextYear, thisYear, thisMonth, thisDay
    if year:
        year = int(year)
    else:
        year = time.localtime()[0]
        thisYear, thisMonth, thisDay = time.localtime()[:3]
        thisYear = datetime.datetime.today().year
        nextYear = thisYear +1
    lst = []
    for y in [year]:
        monthlst = []
        for n, month in enumerate(monthNames):
            record = current = False
            records = Record.objects.filter(date__year=y, date__month=n+1)
            if records:
                record = True
            if y == thisYear and n+1 == thisMonth:
                current = True
            monthlst.append(dict(n=n+1, name = month, record=record, current=current))
        lst.append((y,monthlst))

        records = Record.objects.filter(date__year=y, date__month=n+1)
        
    return render(request, 'TrackaTruck/calendar.html', dict(user=request.user, year=year, years=lst,tYear = thisYear,
                                                             nYear = nextYear, tMonth=thisMonth, tDay = thisDay))


"""Calendar Month Page"""
@login_required
def month(request, year, month, change=None):
    global nextYear, thisYear, thisMonth, thisDay, currentYear, bankholiday, Holidays, easterSunday
    year, month =int(year), int(month)
    thisYear = datetime.datetime.today().year
    thisMonth = datetime.datetime.today().month
    thisDay = datetime.datetime.today().day
    weekDay = True
    bankholiday = False
    hName = "" 

    """variables"""
    cal = calendar.Calendar()
    month_Days = cal.itermonthdays(year, month)
    thisYear, thisMonth, thisDay = time.localtime()[:3]
    lst = [[]]
    week = 0
    calc_easter(int(year))
    calc_bankholiday(int(year))
    
    """month list which contains the list of days """
    for day in month_Days:
        records = current = bankholiday = False
        if day:
            hName = " " 
            if date(int(year),int(month),int(day)).strftime("%A") == 'Saturday' or date(int(year),int(month),int(day)).strftime("%A") == 'Sunday':
                weekDay = False
            else:
                weekDay = True
            
            records = Record.objects.filter(date__year= year, date__month= month, date__day= day)
            record = records.order_by("title")
            current = (day == thisDay and year == thisYear and month == thisMonth)
            hName = check_holiday_name(day, month)
            bankholiday = (day == int(goodFriday[0]) and month == int(goodFriday[1]))
            if bankholiday:
                hName = goodFriday[2]
            else:
                bankholiday = (day == int(easterMonday[0]) and month == int(easterMonday[1]))
                if bankholiday:
                    hName = easterMonday[2]
            for e in Holidays:
                 if (day == int(e[0]) and month == int(e[1])):
                    bankholiday = True
                    hName = e[2]
            for e in celebDays:
                 if (day == int(e[0]) and month == int(e[1])):
                    hName = e[2]    
            if (day == easterSunday[0] and month == easterSunday[1]):
                hName = "Easter Sunday"
        lst[week].append((day, records, current, bankholiday, weekDay, hName))
        if len(lst[week]) == 7:
            lst.append([])
            week+=1
        
    return render(request, 'TrackaTruck/month.html', dict(user=request.user, year=year, tYear = thisYear,
                                                          month=month,tMonth=thisMonth, tDay = thisDay, month_Days=lst,
                                                      monthName = monthNames[month-1]))



"""Maintenance Checklist Page"""
@login_required
def maintenance_checklist(request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/maintenance.html',{}, context)

"""Truck Maintenance Checklist Page"""
@login_required
def truck_maintenance_checklist(request):
     if request.method == "POST":
        form = TruckMaintenanceForm(request.POST)
        
        if form.is_valid():
            truckmain = form.save(commit=False)
            truckmain.created_Date = timezone.now()
            truckmain.author = request.user
            truckmain.save()
            
            return redirect('/truck_maintenance_record/')
     else:
        form = TruckMaintenanceForm()
     return render(request, 'TrackaTruck/truckMaintenance.html', {'form' : form })

"""Delete Truck Maintenance Entry"""    
@login_required
def deleteTruckMaintenance(request, id=None):
   context = RequestContext(request)
   instance = TruckMaintenance.objects.get(id=id)
   instance.delete()

   return redirect('/truck_maintenance_record/')

"""Edit Truck Maintenance Entry"""
@login_required
def editTruckMaintenance(request, id=None):
    context = RequestContext(request)
    if id:
        m = get_object_or_404(TruckMaintenance, pk=id)
        
    form = TruckMaintenanceForm(request.POST, instance= m)
    
    if request.method == "POST":
        if form.is_valid():
            truckmain = form.save(commit=False)
            truckmain.updated_Date = timezone.now()
            truckmain.author = request.user
            truckmain.save()
            return redirect('/truck_maintenance_record/') 
    else:
        form = TruckMaintenanceForm(instance=m)

    return render_to_response('TrackaTruck/editTruckMaintenance.html',{'form':form}, context)

"""Trailer Maintenance Checklist Page"""
@login_required
def trailer_maintenance_checklist(request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/trailerMaintenance.html', {}, context)

"""Truck Maintenance Records Page"""
@login_required
def truck_maintenance_record(request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/truck_maintenance_record.html',{'obj': TruckMaintenance.objects.all()}, context)


"""Delete Truck"""
@login_required
def deleteTruck(request, id=None):
   context = RequestContext(request)
   instance = Truck.objects.get(id=id)
   instance.delete()

   return redirect('/truck_list/')

"""Edit Truck"""
@login_required
def editTruck(request, id=None):
    context = RequestContext(request)
    if id:
        t = get_object_or_404(Truck, pk=id)
        
    form = TruckForm(request.POST, instance= t)
    
    if request.method == "POST":
        if form.is_valid():
            truck = form.save(commit=False)
            truck.updated_Date = timezone.now()
            truck.author = request.user
            truck.save()
            return redirect('/truck_list/')
           
    else:
        form = TruckForm(instance=t)

    return render_to_response('TrackaTruck/editTruck.html',{'form':form}, context)

"""Delete Trailer"""
@login_required
def deleteTrailer(request, id=None):
   context = RequestContext(request)
   instance = Trailer.objects.get(id=id)
   instance.delete()

   return redirect('/trailer_list/')

"""Edit Trailer"""
@login_required
def editTrailer(request, id=None):
    context = RequestContext(request)
    if id:
        r = get_object_or_404(Trailer, pk=id)
        
    form = TrailerForm(request.POST, instance= r)
    
    if request.method == "POST":
        if form.is_valid():
            trailer = form.save(commit=False)
            trailer.updated_Date = timezone.now()
            trailer.author = request.user
            trailer.save()
            return redirect('/trailer_list/')
           
    else:
        form = TrailerForm(instance=r)

    return render_to_response('TrackaTruck/editTrailer.html',{'form':form}, context)

"""Record List Page"""
@login_required
def record_list(request):
    context = RequestContext(request)
    if request.method == "POST":
        truck["truck"] = (True if "truck" in request.POST else False)
    return render_to_response('TrackaTruck/recordList.html', {'obj': Record.objects.all().order_by("date", "title")}, context )

"""Delete Record"""
@login_required
def deleteRecord(request, id=None):
   context = RequestContext(request)
   instance = Record.objects.get(id=id)
   instance.delete()

   return redirect('/record_list/')

"""Delete All Records"""
@login_required
def deleteAllRecord(request):
    Record.objects.all().delete()

    return redirect('/record_list/')

"""Edit Record Page"""
@login_required
def editRecord(request, id=None):
    context = RequestContext(request)
    if id:
        e = get_object_or_404(Record, pk=id)
        
    form = RecordForm(request.POST, instance= e)
    
    if request.method == "POST":
        if form.is_valid():
            record = form.save(commit=False)
            record.updated_Date = timezone.now()
            record.author = request.user
            record.save()
            return redirect('/record_list/')
           
    else:
        form = RecordForm(instance=e)

    return render_to_response('TrackaTruck/editRecord.html',{'form':form}, context)

"""About Page"""
def about(request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/about.html', {}, context)

"""Contact Page"""
def contact(request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/contact.html', {}, context)

"""Help Page"""
def help_page(request):
    context = RequestContext(request)
    return render(request, 'TrackaTruck/help.html', {}, context)

def _show_users(request):
    user_session = request.session
    if not "show_users" in user_session:
        user_session["show_users"] = True
    return user_session["show_users"]

"""Settings"""
@login_required
def settings(request):
    context = RequestContext(request)
    user_session = request.session
    _show_users(request)
    if request.method == "POST":
        user_session["show_users"] = (True if "show_users" in request.POST else False)
    return render(request, 'TrackaTruck/settings.html', {}, context, add_csrf(request, show_users=user_session["show_users"]))

"""Errors"""
def errors(request):
    error = 0
    if truck.make == 'Please Select': return 1
    if error > 0:
        return error
    
    return 0

"""Reminders"""
def reminders(request):
    reminders = []
    year, month, day = time.localtime()[3]
    reminders = Record.objects.filter(date__year=year,date__month=month, date__day=day, author = request.user,
                                      remind = True)
    reminders = reminders.order_by('title')
    next_day = datetime.now() + timedelta(days=1)
    year, month, day = next_day.timetuple()[:3]
    return list(reminders)+ list(Record.objects.filter(date__year=year,date__month=month, date__day=day, author = request.user,
                                      remind = True))




    
    
    

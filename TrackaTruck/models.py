import time
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from django.contrib import admin
from datetime import date
from django import forms


# Create your models here.



make = [('Please Select', 'Please Select'), ('Bedford', 'Bedford'), ('Daf', 'Daf'),
        ('ERF', 'ERF'),('Foden', 'Foden'), ('Freightliner', 'Freightliner'),
        ('Isuzu', 'Isuzu'),('Iveco', 'Iveco'), ('Kenworth', 'Kenworth'),('Leyland', 'Leyland'),
        ('Mack', 'Mack'), ('Man', 'Man'), ('Mercedes', 'Mercedes'),('Peterbilt', 'Peterbilt'),
        ('Renault', 'Renault'),('Scammell', 'Scammell'), ('Scania', 'Scania'),
        ('Volvo', 'Volvo') ]
model = [('Please Select','Please Select'), ('Axor', 'Axor'),('FH Globetrotter', 'FH Globetrotter'), ('LF45', 'LF45'),
         ('Magnum', 'Magnum'), ('R420', 'R420'),('R440', 'R440'), ('R480', 'R480'), ('Stralis', 'Stralis'), ('TGM', 'TGM'),('TGX', 'TGX'),
         ('XF105', 'XF105'),('65', '65'),('105510', '105510'),]
trailer = [('Please Select', 'Please Select'), ('Bulk Tipping', 'Bulk Tipping'), ('Car Transporter', 'Car Transporter'),
           ('Crane', 'Crane'), ('Curtain Side', 'Curtain Side'), ('Drawbar', 'Drawbar'), ('Ejector', 'Ejector'),
           ('Flat', 'Flat'),('Livestock Carrier', 'Livestock Carrier'), ('Low Loader', 'Low Loader'),
           ('Moving Floor', 'Moving Floor'), ('Refrigerated', 'Refrigerated'),
           ('Skeletal', 'Skeletal'), ('Skip', 'Skip'),('Step Frame', 'Step Frame'),('Tanker','Tanker'), ('Tipper Crane', 'Tipper Crane')]
title = [('Please Select', 'Please Select'), ('MOT', 'MOT'),('Tax', 'Tax'),
         ('Maintenance Check', 'Maintenance Check')]
marking_code = [('Please Select', 'Please Select'),('Serviceable', 'Serviceable'), ('Item Requires Attention', 'Item Requires Attention'),
              ('Not Checked', 'Not Checked'), ('Not Applicable', 'Not Applicable')]
fleetNumber = [(0.0, 'Please Select'),(1.0, 'One'), (2.0, 'Two'),
              (3.0, 'Three'), (4.0, 'Four')]
option = [('Please Select', 'Please Select'), ('Yes','Yes'), ('No','No')]
vehicle = [('Please Select', 'Please Select'), ('Truck', 'Truck'), ('Trailer', 'Trailer')]

year_dropdown = []
for y in range(1950, (datetime.datetime.now().year +1)):
    year_dropdown.append((y, y))

class Truck (models.Model):
    vehicle_Reg = models.CharField(max_length=40, blank=False, null = True)
    make = models.CharField(choices = make, max_length=15, default='Please Select')
    model = models.CharField(choices = model,max_length=40, default='Please Select')
    year = models.IntegerField(('year'), choices=year_dropdown, default=datetime.datetime.now().year)
    created_Date = models.DateField(default=timezone.now)
    updated_Date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', null=True)
    

    def __str__(self):
        return self.vehicle_Reg
    def formkey(self):
        return int(self.truckid.value)
    

class Trailer (models.Model):
    trailer_Number = models.CharField(max_length=40, blank=False, null = True)
    trailer_Type = models.CharField(choices = trailer, max_length=15, default='Please Select')
    trailer_Year = models.IntegerField(('year'), choices=year_dropdown, default=datetime.datetime.now().year)
    created_Date = models.DateTimeField(default=timezone.now)
    updated_Date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', null=True)
    

    def __str__(self):
        return self.trailer_Number

class Record (models.Model):
    vehicle_trailer = models.CharField(choices = vehicle, max_length=50, default = 'Please Select')
    title = models.CharField(choices = title, max_length=20, default='Please Select')
    vehicle_Reg = models.ForeignKey(Truck, max_length=100, null=True)
    trailer_Number = models.ForeignKey(Trailer, max_length=100, null=True)
    date = models.DateField(blank=True, null=True)
    created_Date = models.DateTimeField(default=timezone.now)
    updated_Date = models.DateTimeField(default=timezone.now)
    time = models.TimeField(null=True)
    notes = models.CharField(max_length=50, null=True)
    reminder = models.BooleanField(default=False)
    author = models.ForeignKey('auth.User', null=True)
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    company_Name = models.CharField(max_length=40, blank=True)
    address = models.TextField(max_length=500,blank=True)

    User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

    ordering = ["user"]
    
    def __str__(self):
        return str(self.user)
    def __str__(self):
        return self.company_Name
    
  

    
class TruckMaintenance(models.Model):
    company_Name = models.ForeignKey(UserProfile, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    vehicle_Reg = models.ForeignKey(Truck, max_length=100, default='Please Select')
    make = models.CharField(choices = make, max_length=100, default='Please Select')
    model = models.CharField(choices = model,max_length=100, default='Please Select')
    fleet_Number = models.CharField(choices = fleetNumber, max_length=100, default='Please Select')
    odo_Reading = models.CharField(max_length=40, blank=False, null = True)
    chassis = models.CharField(max_length=40, blank=False, null = True)
    tachograph_Calibration = models.DateField(default=timezone.now)
    ved_Expiry = models.DateField(default=timezone.now)
    last_Two_Year_Date = models.DateField(default=timezone.now)
    inspection_Date = models.DateField(default=timezone.now)
    dFT_Plate_Condition_Details = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    speed_Limiter_Plate_Condition_Details = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    seat_Belts_Supplementary_Restraint_Systems_Condition = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    cab_Floor_and_Steps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    seats_Driver_Seat_All_Adjustments_Fully_Functional = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    other_Seats_and_Crew_Amenities = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    mirrors_Internal = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    view_To_Front = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    condition_Of_Glass = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    screen_Wipers = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    speedometer = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    engine_Tachometer = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    audible_Warning = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    driving_Controls = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    steering_Wheel_Free = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    steering_Wheel_Security = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    steering_Column = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    anti_Theft = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    pressure_Warning = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    pressure_Build = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    other_Gauges = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    hand_Lever = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    service_Brake = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    service_Brake_ABS = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    hand_Operated_Brake = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    electrical_Wiring = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    front_Fog = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    panel = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    cab_Heater = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    bumper = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    condition_Of_Wings = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    cab_Panels = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    cab_Security = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    cab_Doors = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    cab_Floor = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    mirrors_and_Indirect = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    front_Lamps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    headlamps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    spot_Lamps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    engine_Mountings = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    oil_Leaks = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    fuel_Tanks = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    exhaust_Systems = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    exhaust_Brakes = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    radiator_Mounting = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    cooling_System = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    fan = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    fuel_Pump = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    speed_Limiter = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    injectors = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    air_Intake = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    air_Compressor = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    road_Wheels = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    sideguards = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    spare_Wheel = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    vehicle_To_Trailer = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    condition_Of_Wings_Back = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    security_Of_Body = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    demountable_Bodies = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    security_Of_Containers = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    tipping_Gear = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    tailboard = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    cranes = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    ancillary_Equipment = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    condition_Of_Chassis = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    wiring_Electrical = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    electrical_Connections = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    leak_Oil = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    fuel_Tanks_Systems = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    exhaust_System = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    suspension_Pins = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    suspension_Units = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    spring_Units = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    shock_Absorbers = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    wheel_Bearings = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    stub_Axle = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    steering_Mechanism = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    steering_Alignment = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    steering_Gear = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    power_Steering = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    axle_Alignment = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    clutch_Operation = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    gearbox = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    changing_Speed = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    power_Take = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    final_Drive = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    speed_Shift = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    differential_Lock = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    load_Transfer = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    transmission = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    electronic_Braking = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    hydraulic_Fluid = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    mechanical_Brake = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    drum_Lining = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    brake_Actuators = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    brake_Systems = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    trailer_Coupling = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    load_Sensing = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    air_Brake = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    anti_Lock = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    supply_Dump = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    multi_Circuit = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    braking_Devices = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    rear_Marking = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    rear_Lamps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    rear_Fog = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    reflectors = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    direction_Indicators = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    side_Marker = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    stop_Lamps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    reversing_Lamps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    position_Lamps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    other_Lamps = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    paintwork = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    licences = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    legal_Writing = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    reg_Plates = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    other_Dangerous = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    smoke_Emission = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    size_Of_Tyre = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    condition_Of_Tyre = models.CharField(choices = marking_code, max_length=100, default='Please Select')
    attention = models.CharField(max_length=40, blank=True, null=True)
    done_By = models.CharField(max_length=40, blank=True, null=True)
    action = models.CharField(max_length=250, blank=True, null=True)
    imo_No = models.CharField(max_length=40, blank=True, null=True)
    signature_Of_Inspector = models.TextField(max_length=500, blank=True, null=True)
    signature = models.CharField(max_length=40, blank=True, null=True)
    position = models.CharField(max_length=40, blank=True, null=True)
    comments = models.TextField(max_length=500, blank=True, null=True)
    percent = models.CharField(max_length=4, blank=True, null=True)
    test = models.CharField(max_length=40, blank=True, null=True)
    road_Speed = models.CharField(choices = option, max_length=100, default='Please Select')
    speed = models.CharField(max_length=4, blank=True, null=True)
    road_Test = models.TextField(max_length=500, blank=True, null=True)
    options = models.CharField(choices = option, max_length=100, default='Please Select')
    date_Completed = models.DateField(default=timezone.now)
    created_Date = models.DateTimeField(default=timezone.now)
    updated_Date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', null=True)

    def __str__(self):
        return self.vehicle_Reg
    def __str__(self):
        return self.company_Name
    
class Error (models.Model):
    error = models.IntegerField(default=0)
    message = models.CharField(max_length = 300, null = False, blank = False)

    def __str__(self):
        error_message = str(self.error) + "-"+ self.message
        return error_message



class TruckAdmin(admin.ModelAdmin):
    list_display = ["vehicle_Reg", "make", "model", "year", "author", "created_Date","updated_Date","id",]
    readonly_fields = ["created_Date", "updated_Date", "author", "id",]
    list_filter = ["vehicle_Reg", "author", "created_Date",]
    ordering = ["vehicle_Reg"]
    

class TrailerAdmin(admin.ModelAdmin):
    list_display = ["trailer_Number", "trailer_Type","trailer_Year", "author","created_Date", "updated_Date", "id"]
    readonly_fields = ["id", "created_Date", "updated_Date", "author",]
    list_filter = ["trailer_Number", "author", "created_Date",]
    ordering = ["trailer_Number"]
    
class RecordAdmin(admin.ModelAdmin):
    list_display = ["vehicle_trailer", "title", "vehicle_Reg", "trailer_Number","date", "time","notes", "reminder","author", "created_Date", "updated_Date","id"]
    readonly_fields = ["id", "created_Date", "updated_Date", "author",]
    list_filter = ["vehicle_trailer","author", "created_Date",]
    ordering = ["title"]
    
class TruckMaintenanceAdmin(admin.ModelAdmin):
    list_display = ["company_Name","address","vehicle_Reg", "make", "model", "fleet_Number", "odo_Reading","chassis", "tachograph_Calibration",
                    "ved_Expiry","last_Two_Year_Date","inspection_Date", "dFT_Plate_Condition_Details",
                    "speed_Limiter_Plate_Condition_Details","seat_Belts_Supplementary_Restraint_Systems_Condition",
                    "cab_Floor_and_Steps", "seats_Driver_Seat_All_Adjustments_Fully_Functional", "other_Seats_and_Crew_Amenities",
                    "mirrors_Internal", "view_To_Front", "condition_Of_Glass", "screen_Wipers", "speedometer","engine_Tachometer",
                    "audible_Warning","driving_Controls","steering_Wheel_Free","steering_Wheel_Security","steering_Column",
                    "anti_Theft","pressure_Warning","pressure_Build","other_Gauges","hand_Lever","service_Brake","service_Brake_ABS",
                    "hand_Operated_Brake","electrical_Wiring","front_Fog","panel","cab_Heater","bumper","condition_Of_Wings",
                    "cab_Panels","cab_Security","cab_Doors","cab_Floor", "mirrors_and_Indirect", "front_Lamps","headlamps",
                    "spot_Lamps","engine_Mountings","oil_Leaks", "fuel_Tanks","exhaust_Systems", "exhaust_Brakes","radiator_Mounting",
                    "cooling_System","fan","fuel_Pump", "speed_Limiter","injectors", "air_Intake","air_Compressor", "road_Wheels",
                    "sideguards","spare_Wheel","vehicle_To_Trailer","condition_Of_Wings_Back","security_Of_Body","demountable_Bodies",
                    "tipping_Gear","tailboard","cranes","ancillary_Equipment","condition_Of_Chassis","wiring_Electrical","electrical_Connections",
                    "leak_Oil","fuel_Tanks_Systems","exhaust_System","suspension_Pins","suspension_Units","spring_Units","shock_Absorbers",
                    "wheel_Bearings","stub_Axle","steering_Mechanism","steering_Alignment","steering_Gear","power_Steering","axle_Alignment",
                    "clutch_Operation","gearbox","changing_Speed","power_Take","final_Drive","speed_Shift","differential_Lock","load_Transfer",
                    "transmission","electronic_Braking","hydraulic_Fluid","mechanical_Brake","drum_Lining","brake_Actuators","brake_Systems",
                    "trailer_Coupling","load_Sensing","air_Brake","anti_Lock","supply_Dump","multi_Circuit","braking_Devices","rear_Marking",
                    "rear_Lamps","rear_Fog","reflectors","direction_Indicators","side_Marker","stop_Lamps","reversing_Lamps","position_Lamps",
                    "other_Lamps","paintwork","licences","legal_Writing","reg_Plates","other_Dangerous","smoke_Emission","size_Of_Tyre",
                    "condition_Of_Tyre","attention","done_By","action","imo_No","signature_Of_Inspector","signature","position","date_Completed",
                    "comments","percent","test","road_Speed","speed","road_Test", "options","author", "created_Date", "updated_Date",]
    readonly_fields = ["author", "created_Date", "updated_Date",]
    list_filter = ["company_Name", "vehicle_Reg", "author", "created_Date",]
    ordering = ["vehicle_Reg"]
    

class ErrorAdmin(admin.ModelAdmin):
    model = Error

    list_display = ["error", "message"]
    ordering = ["error"]
    
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    
    list_display = ["user", "company_Name"]
    search_fields = ["user"]
    readonly_fields = ["user"]
    ordering = ["user"]

    def __str__(self):
        return str(user)
    

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False
    
admin.site.register(Truck, TruckAdmin)
admin.site.register(Trailer, TrailerAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(TruckMaintenance, TruckMaintenanceAdmin)
admin.site.register(Error, ErrorAdmin)
admin.site.register(UserProfile, UserProfileAdmin)




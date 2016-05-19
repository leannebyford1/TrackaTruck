from django import forms
from django.forms import ModelForm, Form
from TrackaTruck.models import Truck
from TrackaTruck.models import Trailer
from TrackaTruck.models import Record
from TrackaTruck.models import TruckMaintenance
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

# Create your tests here.



class TruckForm(forms.ModelForm):

    class Meta:
        model = Truck
        fields = ('vehicle_Reg', 'make', 'model', 'year','id',)
        exclude = ('created_Date',)



class TrailerForm(forms.ModelForm):

    class Meta:
        model = Trailer
        fields = ('trailer_Number', 'trailer_Type','trailer_Year',)
        exclude = ('created_Date',)

class RecordForm(forms.ModelForm):

    class Meta:
        model = Record
        fields = ('vehicle_trailer', 'title', 'vehicle_Reg', 'trailer_Number',
                      'date', 'time', 'notes', 'reminder',)
        exclude = ('created_Date',)


        
        
class TruckMaintenanceForm(forms.ModelForm):

    class Meta:
        model = TruckMaintenance
        fields = ('company_Name','address','vehicle_Reg', 'make', 'model','chassis', 'odo_Reading','tachograph_Calibration',
                  'last_Two_Year_Date', 'inspection_Date','ved_Expiry','dFT_Plate_Condition_Details',
                  'speed_Limiter_Plate_Condition_Details','seat_Belts_Supplementary_Restraint_Systems_Condition', 'cab_Floor_and_Steps',
                  'seats_Driver_Seat_All_Adjustments_Fully_Functional', 'other_Seats_and_Crew_Amenities',
                  'mirrors_Internal', 'view_To_Front', 'condition_Of_Glass', 'screen_Wipers', 'speedometer',
                  'engine_Tachometer', 'audible_Warning','driving_Controls','steering_Wheel_Free','steering_Wheel_Security','steering_Column',
                  'anti_Theft','pressure_Warning','pressure_Build','other_Gauges','hand_Lever','service_Brake','service_Brake_ABS',
                  'hand_Operated_Brake','electrical_Wiring','front_Fog','panel','cab_Heater', 'bumper','condition_Of_Wings',
                  'cab_Panels','cab_Security','cab_Doors','cab_Floor', 'mirrors_and_Indirect', 'front_Lamps','headlamps',
                  'spot_Lamps','engine_Mountings','oil_Leaks', 'fuel_Tanks','exhaust_Systems', 'exhaust_Brakes','radiator_Mounting',
                  'cooling_System','fan','fuel_Pump', 'speed_Limiter','injectors', 'air_Intake','air_Compressor','road_Wheels',
                  'sideguards','spare_Wheel','vehicle_To_Trailer','condition_Of_Wings_Back','security_Of_Body','demountable_Bodies',
                  'tipping_Gear','tailboard','cranes','ancillary_Equipment','condition_Of_Chassis','wiring_Electrical','electrical_Connections',
                  'leak_Oil','fuel_Tanks_Systems','exhaust_System','suspension_Pins','suspension_Units','spring_Units','shock_Absorbers',
                  'wheel_Bearings','stub_Axle','steering_Mechanism','steering_Alignment','steering_Gear','power_Steering','axle_Alignment',
                  'clutch_Operation','gearbox','changing_Speed','power_Take','final_Drive','speed_Shift','differential_Lock','load_Transfer',
                  'transmission','electronic_Braking','hydraulic_Fluid','mechanical_Brake','drum_Lining','brake_Actuators','brake_Systems',
                  'trailer_Coupling','load_Sensing','air_Brake','anti_Lock','supply_Dump','multi_Circuit','braking_Devices','rear_Marking',
                  'rear_Lamps','rear_Fog','reflectors','direction_Indicators','side_Marker','stop_Lamps','reversing_Lamps','position_Lamps',
                  'other_Lamps','paintwork','licences','legal_Writing','reg_Plates','other_Dangerous','smoke_Emission','size_Of_Tyre',
                  'condition_Of_Tyre','attention','done_By','action','imo_No','signature_Of_Inspector', 'date_Completed',
                  'signature', 'position','test', 'speed', 'percent', 'comments','options',)
        exclude = ('created_Date',)
                  
                  

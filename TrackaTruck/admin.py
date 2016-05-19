from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django.contrib import admin
from .models import Truck
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

#from .models import Trailer
#from .models import TruckAdmin
# Register your models here.

#admin.site.register (Truck)
#admin.site.register(Trailer)

class AdminSite(AdminSite):
    site_title = ugettext_lazy('Track-A-Truck Admin')
    site_header = ugettext_lazy('Track-A-Truck Administration')
    index_title = ugettext_lazy('Site Administration')
    

    class Media:
        css = { 'all': ('static/admin/css/base.css', ) }

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Company Details'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,  )






admin.site.unregister (User)
admin.site.register (User, UserAdmin)


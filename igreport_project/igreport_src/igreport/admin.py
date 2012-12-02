from django.contrib import admin
from igreport.models import UserProfile
from django.forms import ModelForm, ModelChoiceField
from rapidsms.contrib.locations.models import Location

class UserProfileForm(ModelForm):
    district = ModelChoiceField(Location.objects.filter(type__name='district').order_by('name'))
    class Meta:
        model = UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm

admin.site.register(UserProfile, UserProfileAdmin)

from django.contrib import admin



# Register your models here.

from .models import *


admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Flight)
admin.site.register(Airport)


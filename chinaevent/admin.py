from django.contrib import admin
from chinaevent.models import Candidate

# Register your models here.
@admin.register(Candidate)
class TestRequest(admin.ModelAdmin):
    list_display = ('name', 'university', 'email')

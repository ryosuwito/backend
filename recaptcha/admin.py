from django.contrib import admin

# Register your models here.
from .forms import AdminAuthenticationForm


admin.AdminSite.login_form = AdminAuthenticationForm

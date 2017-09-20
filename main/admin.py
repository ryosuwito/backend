from django.contrib import admin
from main.models import OnlineApplication, TestRequest
from main.forms import OnlineApplicationForm
from django.core.exceptions import ObjectDoesNotExist


@admin.register(OnlineApplication)
class OnlineApplicationAdmin(admin.ModelAdmin):
    def get_scheduled_test(application):
        if application.status == OnlineApplication.APP_STATUS_FAIL_RESUME:
            return "Not Applicable"
        elif application.status == OnlineApplication.APP_STATUS_PASS_RESUME:
            try:
                return application.test_request.get_datetime()
            except ObjectDoesNotExist:
                return "Oops no test request!"
        else:
            return "None"

    get_scheduled_test.short_description = "Scheduled Test"
    list_display = ('name', 'university', 'email', 'position', 'status', get_scheduled_test, 'info_src')
    list_editable = ('status',)
    list_filter = ('status',)


@admin.register(TestRequest)
class TestRequest(admin.ModelAdmin):
    list_display = ('application', 'get_absolute_url', 'version', 'get_datetime', 'status')
    list_selected_related = ('application')
    list_display_links = ('application',)

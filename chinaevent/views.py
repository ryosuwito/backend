from django.shortcuts import render

from .forms import RegistrationForm


def beijing_2018(request):
    return render(request, "chinaevent/beijing2018.html")


def register(request):
    template = "chinaevent/register.html"
    confirm_template = "chinaevent/register_confirm.html"
    if not request.POST:
        return render(request, template, {'form': RegistrationForm()})
    else:
        # handle post request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            model_instance = form.save()
            return render(request, confirm_template, {
                'form': None
            })
        else:
            return render(request, template, {'form': form})

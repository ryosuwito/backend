from django.shortcuts import render


def index(request):
    return render(request, "main/main_page.html")


def career(request):
    return render(request, "main/career.html")


def culture(request):
    return render(request, "main/culture.html")


def what(request):
    return render(request, "main/what_we_do.html")

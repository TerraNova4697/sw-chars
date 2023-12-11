from django.shortcuts import render
from django.urls import reverse


def home_view(request):
    context = {
        'chars_url': reverse('swchars:chars'),
        'items_url': reverse('swchars:items'),
    }
    return render(request, 'swchars/chars_list.html', context)

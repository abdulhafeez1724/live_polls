from django.shortcuts import render
from .models import Poll

def poll_view(request):
    polls = Poll.objects.all()
    return render(request, 'polls/index.html', {'polls': polls})

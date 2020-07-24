from django.shortcuts import render
from backoffice.models import Ticket
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.profile.role != 'moderator':
        return render(request,'archive/home.html')
    return render(request,'backoffice/home.html')

@login_required
def ticket_detail(request,ticket_id):
    if request.user.profile.role != 'moderator':
        return render(request,'archive/home.html')
    status = [x[0] for x in Ticket.status]
    tk = Ticket.objects.get(pk=ticket_id)
    if request.method=="POST":
        if 'tk_status' in request.POST:
            tk.usr_manager = request.user
            tk.state = request.POST['tk_status']
            tk.save()

    context = {
        'ticket':tk,
        'status':status
    }
    return render(request,'backoffice/ticket_detail.html',context)

@login_required
def tickets(request):
    if request.user.profile.role != 'moderator':
        return render(request,'archive/home.html')
    tags = [x[0] for x in Ticket.categories]
    status = [x[0] for x in Ticket.status]
    tickets = Ticket.objects.all().order_by('-created_at')
    if request.method == 'POST':
        if 'Tag' in request.POST:
            tickets = tickets.filter(tag=request.POST['Tag'])
        if 'Status' in request.POST:
            tickets = tickets.filter(state=request.POST['Status'])
        if 'Moderator' in request.POST:
            tickets = tickets.filter(usr_manager=request.POST['Moderator'])
        if 'not_managed' in request.POST:
            tickets = tickets.filter(usr_manager=None)

    ticket_paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = ticket_paginator.get_page(page_number)
    context = {
        'tags':tags,
        'status':status,
        'page_obj':page_obj
    }
    return render(request,'backoffice/tickets.html',context)
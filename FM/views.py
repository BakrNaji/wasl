from django.shortcuts import render, redirect, get_object_or_404
from The_Investor.models import *
from The_Owner.models import *
from .models import *
from .forms import InvForm , PromoForm
# Create your views here.


from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

from django.shortcuts import render
from .models import FinancialReport


def invreq(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        add_req = InvForm(request.POST, request.FILES)
        if add_req.is_valid():
            req_instance = add_req.save(commit=False)
            req_instance.investor = request.user.investor
            req_instance.project = project
            req_instance.save()

    context = {
        'form': InvForm(),
    }
    
    return render(request, 'pages/invreq.html', context)



def promoreq(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        add_promo = PromoForm(request.POST, request.FILES)
        if add_promo.is_valid():
            promo_instance = add_promo.save(commit=False)
            promo_instance.owner = request.user.owner
            promo_instance.project = project
            promo_instance.save()

    context = {
        'pform': PromoForm(),
    }

    return render(request, 'pages/promoreq.html', context)

# from django.shortcuts import render
# from .models import FinancialReport

# def financial_reports_view(request):
#     reports = FinancialReport.objects.all()
#     return render(request, 'FM/financial_reports.html', {'reports': reports})



from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income,2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income':income,
        'page_obj' : page_obj,
        'currency' : currency
    }
    return render(request, 'income/index.html', context)


def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method=='GET':
        return render(request, 'income/add_income.html',context)
    if request.method == 'POST':
        amount= request.POST['amount']
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'income/add_income.html',context)

        description= request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_income.html',context)


        UserIncome.objects.create(owner=request.user,amount=amount,date=date,
                               description=description,source=source)
        messages.success(request,'Record saved successfully')
        return redirect('income')


def income_edit(request, id):
    sources = Source.objects.all()
    income= UserIncome.objects.get(pk=id)
    context ={
        'income':income,
        'values':income,
        'sources' : sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'income/edit-income.html',context)

        description= request.POST['description']
        date = request.POST['expense_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit-income.html',context)

        income.owner=request.user
        income.amount=amount
        income.date=date
        income.description=description
        income.source=source

        income.save()
        messages.success(request,'Income Updated successfully')
        return redirect('income')


def delete_income(request,id):
    income= UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed')
    return redirect('income')




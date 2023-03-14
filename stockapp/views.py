from django.shortcuts import render
from django.http import HttpResponse 
import pandas as pd
import time
import os
from django.conf import settings
from .models import Broker, Stock, Holdings, HoldingsPerMonth, YesterdayTransaction
from django.db import transaction
from .tasks import extract_csv, extract_csv_per_month, save_daily_transactions
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime, timedelta
from celery import group, chain, chord

# def testCelery(request):
#     group(extract_csv.delay(), save_csv_per_month.delay())
#     return HttpResponse("Done")

# Create your views here.
def save_csv_data(request):
    # Create a group of tasks to be executed in parallel
    parallel_tasks = group(extract_csv.s(), extract_csv_per_month.s())

    # Create a chord by combining the group of tasks with a callback task
    chord_task = chord(parallel_tasks)(save_daily_transactions.s())

    # Execute the chord asynchronously
    result = chord_task.apply_async()

    # Wait for the result
    result.get()

    # # Group the tasks together
    # task_group = group(extract_csv.s(), extract_csv_per_month.s())

    # # Chain the group task with the final task
    # task_chain = chain(task_group, save_daily_transactions.s())

    # # Launch the task chain
    # result = task_chain.apply_async()

    # # Wait for the tasks to complete and retrieve the results
    # results = result.get()
    #print(results)
    # extract_csv.apply()
    # extract_csv_per_month.apply()
    # save_daily_transactions.apply()
    return HttpResponse("Done")


# def save_csv_per_month(request):
#     extract_csv_per_month.delay()
#     return HttpResponse("Done")


# def daily_transactions(request):
#     save_daily_transactions.delay()
#     return HttpResponse("Done")


def testing(request):
    queryset_data = HoldingsPerMonth.objects.filter(broker = 5, stock="CFCL").order_by("-date")
    list_data = list(queryset_data)
    for i in range(len(list_data)):
        print(list_data[i].date, list_data[i].broker, list_data[i].stock, list_data[i].total_shares)
    queryset_data = HoldingsPerMonth.objects.filter(broker = 8).order_by("-date").first()
    #list_data = list(queryset_data)
    print(queryset_data.date, queryset_data.broker, queryset_data.stock, queryset_data.total_shares)
    return HttpResponse("test")


def getAllBrokers(request):
    queryset = Broker.objects.all().values()
    return JsonResponse(list(queryset), safe=False)


def bar_graph(request):
    # get parameter from ajax
    #symbol = request.GET.get("stockName")
    
    #bar chart
    symbol = request.GET.get("stocks")
    if symbol is None:
        symbol = "BFC"

    labels = []
    values = []
    data = Holdings.objects.filter(stock=symbol).order_by('-total_shares')[:15]
    for i in data:
        if int(i.total_shares) >= 0:
            labels.append(i.broker)
            values.append(i.total_shares)


    #line chart
    stock = request.GET.get("stock")
    broker = request.GET.get("broker")
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get("todate")

    if stock is None:
        stock = "BFC"
    
    if broker is None:
        broker = "5"

    if fromdate is None or fromdate == "":
        #fromdate = datetime.today()
        fromdate = "2021-01-08"
        #print("From Date: ", fromdate)
    if todate is None or todate == "":
        #todate = datetime.today() - timedelta(days=32)
        todate = "2021-02-25"
        #print("To Date: ", todate)

    chart_labels = []
    chart_values = []
    queryset_data = HoldingsPerMonth.objects.filter(broker = broker, stock = stock, date__range=(fromdate, todate)).order_by("-date")[:30]
    list_data = list(queryset_data)
    for i in range(len(list_data)):
        date = str(list_data[i].date)
        split_date = date.split("-")
        #new_date = str(split_date[1]) + "|" + str(split_date[2])
        chart_labels.append(split_date[2])
        chart_values.append(list_data[i].total_shares)
        #print(split_date[2], list_data[i].total_shares)
        #print(list_data[i].date, list_data[i].broker, list_data[i].stock, list_data[i].total_shares)
    
    chart_values.reverse()
    #print(values)
    chart_labels.reverse()
    #print(labels)

    # stock to watch
    yesterday_data = YesterdayTransaction.objects.all().order_by("-percentage")[:10]

    context = {
        "labels": labels,
        "values": values,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "data": list(yesterday_data),
    }

    return render(request, "chart.html", context)


def line_chart(request):
    labels = []
    values = []
    queryset_data = HoldingsPerMonth.objects.filter(broker = 5).order_by("-date")[:30]
    list_data = list(queryset_data)
    for i in range(len(list_data)):
        date = str(list_data[i].date)
        split_date = date.split("-")
        labels.append(split_date[2])
        values.append(list_data[i].total_shares)
        #print(list_data[i].date, list_data[i].broker, list_data[i].stock, list_data[i].total_shares)
    
    values.reverse()
    #print(values)
    labels.reverse()
    #print(labels)
    context = {
        "labels": labels,
        "values": values,
    }
    return render(request, "line.html", context)


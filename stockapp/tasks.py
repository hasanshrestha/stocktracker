from celery import shared_task
from celery import group
from django.shortcuts import render
from django.http import HttpResponse, response 
from django.http import JsonResponse
import pandas as pd
import time
import os
from django.conf import settings
from .models import Broker, Stock, Holdings, HoldingsPerMonth, DailyTransaction, YesterdayTransaction
from django.db import transaction
from datetime import datetime

@shared_task(bind=True)
def extract_csv(request):
    file_path = (
        os.path.join(settings.BASE_DIR, "media") + "/" + "UNL.csv"
    )
    filename = os.path.basename(file_path)[:-4]
    print("Filename: ", filename)

    dataset = pd.read_csv(file_path)
    #print(dataset)

    get_stock = Stock.objects.get(symbol=filename)
    print("Symbol: ", get_stock.symbol)

    st = time.time()

    #with transaction.atomic(): 1=date  3=buyer, 4=seller, 5=quantity
    for row in reversed(dataset.values.tolist()):
        # print(row)
        # print(row[1], row[3], row[4], row[5])
        broker_object = Broker.objects.get(broker_number = row[3])
        # d = datetime.strptime(row[1], '%Y/%m/%d')
        # new_date = d.strftime('%Y-%m-%d')
        # print("New Date: ", d.strftime('%Y-%m-%d'))
        
        if Holdings.objects.filter(broker = row[3], stock = get_stock.symbol).exists(): 
            print("********")
            check_buyer_stock = Holdings.objects.get(broker = row[3], stock = get_stock.symbol)
            updated_share_qty = int(check_buyer_stock.total_shares) + int(row[5])
            Holdings.objects.filter(broker = row[3], stock = get_stock.symbol).update(total_shares=str(updated_share_qty))
        else:
            Holdings.objects.create(broker= broker_object, stock= get_stock, total_shares= row[5])
            print("########")
        
        if Holdings.objects.filter(broker = row[4], stock = get_stock.symbol).exists() :
            print("@@@@@@@@")
            check_seller_stock = Holdings.objects.get(broker = row[4], stock = get_stock.symbol)
            if row[3] != row[4]:
                updated_share_qty = int(check_seller_stock.total_shares) - int(row[5])
                Holdings.objects.filter(broker = row[4], stock = get_stock.symbol).update(total_shares=str(updated_share_qty))
                # if updated_share_qty < 0:
                #     updated_share_qty = 0
                #     HoldingsPerMonth.objects.filter(broker = row[4], stock = get_stock.symbol, date= new_date).update(total_shares=str(updated_share_qty))
                # else:
                #     HoldingsPerMonth.objects.filter(broker = row[4], stock = get_stock.symbol, date= new_date).update(total_shares=str(updated_share_qty))

    end = time.time()
    print("Time1: ", end-st)
    response = {
        "msg":"Successfull!!"
    }
    return response



@shared_task(bind=True)
def extract_csv_per_month(request):
    file_path = (
        os.path.join(settings.BASE_DIR, "media") + "/" + "UNL.csv"
    )
    filename = os.path.basename(file_path)[:-4]
    print("Filename: ", filename)

    dataset = pd.read_csv(file_path)
    #print(dataset)
    get_stock = Stock.objects.get(symbol=filename)
    print("Symbol: ", get_stock.symbol)
    st = time.time()

    #with transaction.atomic(): 1=date  3=buyer, 4=seller, 5=quantity
    for row in reversed(dataset.values.tolist()):
        # print(row)
        # print(row[1], row[3], row[4], row[5])
        broker_object = Broker.objects.get(broker_number = row[3])
        d = datetime.strptime(row[1], '%Y/%m/%d')
        new_date = d.strftime('%Y-%m-%d')
        # print("New Date: ", d.strftime('%Y-%m-%d'))
        
        if HoldingsPerMonth.objects.filter(broker = row[3], stock = get_stock.symbol, date= new_date).exists(): 
            print("********")
            check_buyer_stock = HoldingsPerMonth.objects.get(broker = row[3], stock = get_stock.symbol, date= new_date)
            updated_share_qty = int(check_buyer_stock.total_shares) + int(row[5])
            HoldingsPerMonth.objects.filter(broker = row[3], stock = get_stock.symbol, date= new_date).update(total_shares=str(updated_share_qty))
        
        elif HoldingsPerMonth.objects.filter(broker = row[3], stock = get_stock.symbol).exists():
            print("$$$$$$$")
            check_buyer_stock = HoldingsPerMonth.objects.filter(broker = row[3], stock = get_stock.symbol).order_by("-date").first()
            updated_share_qty = int(check_buyer_stock.total_shares) + int(row[5])
            #HoldingsPerMonth.objects.filter(broker = row[3], stock = get_stock.symbol, date= new_date).update(total_shares=str(updated_share_qty))
            HoldingsPerMonth.objects.create(broker = broker_object, stock = get_stock, date= new_date, total_shares= updated_share_qty)
        else:
            HoldingsPerMonth.objects.create(broker= broker_object, stock= get_stock, date= new_date, total_shares= row[5])
            print("########")
        
        if HoldingsPerMonth.objects.filter(broker = row[4], stock = get_stock.symbol, date= new_date).exists() :
            print("@@@@@@@@")
            check_seller_stock = HoldingsPerMonth.objects.get(broker = row[4], stock = get_stock.symbol, date= new_date)
            if row[3] != row[4]:
                updated_share_qty = int(check_seller_stock.total_shares) - int(row[5])
                HoldingsPerMonth.objects.filter(broker = row[4], stock = get_stock.symbol, date= new_date).update(total_shares=str(updated_share_qty))
                # if updated_share_qty < 0:
                #     updated_share_qty = 0
                #     HoldingsPerMonth.objects.filter(broker = row[4], stock = get_stock.symbol, date= new_date).update(total_shares=str(updated_share_qty))
                # else:
                #     HoldingsPerMonth.objects.filter(broker = row[4], stock = get_stock.symbol, date= new_date).update(total_shares=str(updated_share_qty))

    end = time.time()
    print("Time1: ", end-st)
    print("Symbol: ", get_stock.symbol)
    response = {
        "msg":"Successfull!!"
    }
    return response



@shared_task(bind=True)
def save_daily_transactions(request):
    stocks = Stock.objects.all()
    brokers = Broker.objects.all()
    st = time.time()
    for stock in stocks:
        for broker in brokers:
            if HoldingsPerMonth.objects.filter(stock = stock, broker = broker).exists():
                print("!!!!!!!!!!")
                data = HoldingsPerMonth.objects.filter(stock = stock, broker = broker).order_by("-date")[:2]
            
                if DailyTransaction.objects.filter(stock = stock, broker = broker, date=data[0].date).exists():
                    None
                else:
                    DailyTransaction.objects.bulk_create(list(data))

                    percentage = ((int(data[0].total_shares) - int(data[1].total_shares))*100) / int(data[1].total_shares)
                    YesterdayTransaction.objects.create(broker = data[0].broker, stock = data[0].stock, date = data[0].date, total_shares = data[0].total_shares, percentage=percentage)

    end = time.time()
    print("Time1: ", end-st)
    response = {
        "msg":"Saved!!"
    }
    return response



from django.http.response import JsonResponse, HttpResponse
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
import datetime
from datetime import timedelta
import calendar


class ProductList(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def delete(self, request, format=None):
            products = Product.objects.filter(CustomerId=request.data['CustomerId'], ProductName=request.data['ProductName'],Domain=request.data['Domain'])
            if products:
                products.delete()
                return JsonResponse(request.data, status=status.HTTP_200_OK)
            return JsonResponse(request.data, status=status.HTTP_400_BAD_REQUEST)

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def build_item(product, mail_date):
    return {'CustomerId':product.CustomerId, 'ProductName':product.ProductName, 'Domain':product.Domain, 'mail_date':str(mail_date)}

def emails_list(request):
    items=[]
    product_listfinal_list=''
    products = list(Product.objects.all())
    product_list = 'CustomerID   ProductName   Domain   EmailDate  \n';
    if products:
        for product in products:
            mail_date = add_months(product.StartDate, product.Duration)
            if product.ProductName == 'domain':
                calculated_mail_date = mail_date - timedelta(2)
                items.append(build_item(product, calculated_mail_date))
            if product.ProductName == 'hosting':
                activated_mail_date = product.StartDate + timedelta(1)
                items.append(build_item(product, activated_mail_date))
                expiration_mail_date = mail_date - timedelta(3)
                items.append(build_item(product, expiration_mail_date))
            if product.ProductName == 'pdomain':
                expiration_mail_date_1 = mail_date - timedelta(9)
                items.append(build_item(product, expiration_mail_date_1))
                expiration_mail_date_2 = mail_date - timedelta(2)
                items.append(build_item(product, expiration_mail_date_2))
        ordered_list = sorted(items, key=lambda i: i['mail_date'])
        for item in ordered_list:
            product_list += item['CustomerId'] + ' | ' +  item['ProductName'] + ' | ' + item['Domain'] + ' | ' + item['mail_date'] + '\n'
    else:
        print('no products')
        
    return HttpResponse(product_list)



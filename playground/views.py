from itertools import product
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from store.models import Product, OrderItem


# Create your views here.


def say_hello(request):
    # queryset=Product.objects.filter(unit_price__gt=60)
    # queryset=Product.objects.filter(unit_price__range=(20,40))

    #find all the products in the collection no 1
    # queryset=Product.objects.filter(collection__id__range=(1,2,3))

    #find string on the title
    #queryset=Product.objects.filter(title__icontains='coffee')

    #find certain date
    # queryset=Product.objects.filter(last_update__year=2021)

    #to find all the products with no description
    # queryset=Product.objects.filter(description__isnull=True)

    #find products inventory<10 AND unit_price<20
    # queryset=Product.objects.filter(inventory__lt=10,unit_price__lt=20)
    # queryset=Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    #logical OR operator
    # queryset=Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

    # SORTING
    # queryset=Product.objects.order_by('-title')

    # LIMITING results return only 5 results
    # queryset=Product.objects.all()[:5]

    #SELECTING FIELDS TO QUERY
    # queryset=Product.objects.values('id','title')

    #access related fields
    # queryset=Product.objects.values('id','title','collection__title')

    #select product that have been ordered and sort them by title
    # queryset=Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')

    # to load all the products with their collection
    # queryset=Product.objects.all()
    queryset=Product.objects.select_related('collection').all()

    # queryset=OrderItem.objects.values('product__id').distinct()

    # product=Product.objects.filter(pk=0).first()
    #product=Product.objects.filter(pk=0).exists()
    # try:
    #     product=Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass
    return render(request,'hello.html',{'name':'Bishnu','products':list(queryset)})

    

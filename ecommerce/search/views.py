from django.shortcuts import render
from django.views import View
from shop.models import Product
from django.db.models import Q
class SearchView(View):
    def get(self,request):
        query=request.GET['q'] #read the keyword
        print(query)
        #ORM query to filter records from table(two or more)
        p =Product.objects.filter(Q(name__icontains=query)
                              |Q(description__icontains=query)
                              |Q(price__icontains=query))
        context={'products':p,'query':query}

        return render(request,'search.html',context)

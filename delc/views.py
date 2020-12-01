from django.shortcuts import render
from reci.models import recipes,comments,category
from django.contrib.auth.models import User


def index(request):
    sum=0
    avglist=[]
    recipe=recipes.objects.all()
    for i in recipe:
            comment=comments.objects.filter(recipe=i.id)
            if len(comment)!=0:
                
                for avg in comment:
                    sum=sum+avg.rating


                average=round(sum/len(comment))
            else:
                average=0

            avglist.append(average)
            sum=0

    cat = category.objects.all() 
    return render(request, 'index.html',{'data': zip(recipe,avglist),'cat':cat } )

def contact(request):
    return render(request, 'contact.html')
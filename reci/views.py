from django.views.generic import CreateView 
from django.db.models import Q        
from django.shortcuts import get_object_or_404, redirect, render
from .models import recipes,steps,integredients,comments,whishlist,category,reciepe_category
from accounts.models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf 
from django.contrib import messages
from django.db.models.aggregates import Sum
from datetime import date, timedelta
from django.utils import timezone
from django.shortcuts import redirect

def pdf(request,id):
    template = get_template('pdfff.html')
    reci= recipes.objects.get(id=id)
    step=steps.objects.filter(recepe=id)
    incr=integredients.objects.filter(recipe=id)
    context = {
            "Name": reci.title,
            "descr": reci.descr,
            "total": reci.total_time,
            "active": reci.active_time,
            "serves":reci.serves,
            "step":step,"incr":incr,
            
        }
    html = template.render(context)
    pdf = render_to_pdf('pdfff.html',context)
    return HttpResponse(pdf, content_type='application/pdf')



def recipe(request,id):
    reci = recipes.objects.get(id=id)
    # stp=steps.objects.get(recepe=reci.id)
    stp=steps.objects.filter(recepe=id).order_by('order_no')
    inc=integredients.objects.filter(recipe=id)
    com=comments.objects.filter(recipe=id)
    if  request.user.is_anonymous:
        return redirect('/accounts/sign-in')
    wish=whishlist.objects.filter(recepe=reci).filter(author=request.user).first()
    return render(request,'recipe.html',{'recipe': reci,'stp':stp,'inc':inc,'com':com,'wish':wish})
def sigup(request):
    return render(request,'sign-up.html')

def signin(request):
    return render(request,'sign-in.html')

def wishlist(request,id):
    wish=whishlist.objects.filter(author=id).distinct()
    
    print("whiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiish",wish)
    sum=0
    avglist=[]

    for i in wish:
            comment=comments.objects.filter(recipe=i.recepe.id)
            if len(comment)!=0:
                
                for avg in comment:
                    sum=sum+avg.rating


                average=round(sum/len(comment))
            else:
                average=0

            avglist.append(average)
            sum=0
   
    return render(request,'wishlist.html',{'data': zip(wish,avglist)})

def profile(request,id):
    current=request.user
    num=[]
    z=0
    reci=recipes.objects.filter(author=id)
    for i in reci:
        num.append(len(comments.objects.filter(recipe=i.id)))
    for n in num:
        z=z+n
    
    x=len(reci)
    use=User.objects.filter(id=id)

    sum=0
    avglist=[]

    for i in reci:
            comment=comments.objects.filter(recipe=i.id)
            if len(comment)!=0:
                
                for avg in comment:
                    sum=sum+avg.rating


                average=round(sum/len(comment))
            else:
                average=0

            avglist.append(average)
            sum=0
    if z==0:
        z="No"
    return render(request,'profile.html',{'data': zip(reci,avglist),'use':use,'x':x,'z':z,'current':current})

def update(request,id):
    if request.method=='POST':
        post = Profile.objects.get(user=id)
        post.image=request.FILES.get('pic')
        print(post.image)
        post.save()
        messages.success(request,"Profile updated successfully!")
        return redirect('/reci/profile/'+str(id))
def delrecipe(request,recid,usrid):
    obj = get_object_or_404(recipes, id = recid) 
    print(obj)
    obj.delete() 
    messages.success(request,"Recipe deleted successfully!")
    return redirect('http://127.0.0.1:8000/reci/profile/'+str(usrid))

def comment(request,id):
    usr=request.user.id
    print("dddddddddd",usr)
    exist=comments.objects.filter(author=usr).filter(recipe=id)
    
    
    if exist.exists():
          messages.error(request,"You have already rated this recipe!!")
          return redirect('http://127.0.0.1:8000/reci/recipe/'+str(id))
    
    else:
        obj=comments()
        obj.comment=request.POST.get('post')   
        obj.author= request.user
        reci = recipes.objects.get(id=id)
        obj.recipe=reci
        if(request.POST.get('rate') ) is None:
            messages.error(request,"Please rate recipe!!")
            return redirect('http://127.0.0.1:8000/reci/recipe/'+str(id))
        obj.rating=request.POST.get('rate') 
        
        obj.save()
        sam=[]
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        rate=comments.objects.filter(created_at__gte=monday_of_this_week).filter(recipe=id)
        length=len(comments.objects.filter(created_at__gte=monday_of_this_week).filter(recipe=id))
        for ratings in rate:
            sam.append(ratings.rating)
        print('cccccccccccccccccccccccccccccccccccoooooooooooont',sam.count(5))
            
        post = recipes.objects.get(id=id)
        post.fivestarcount= sam.count(5)
        post.save()
    return redirect('http://127.0.0.1:8000/reci/recipe/'+str(id))
def delcomment(request,id,recid):
    obj = get_object_or_404(comments, id = id) 
    
    obj.delete() 
    messages.success(request,"Comment deleted successfully!")
    return redirect('http://127.0.0.1:8000/reci/recipe/'+str(recid))
def warning(request,id,recid):
    messages.warning(request,"Do you really want to delete this review?")
    return redirect('http://127.0.0.1:8000/reci/recipe/'+str(recid))
def recwarning(request,recid,usrid):
    messages.warning(request,"Do you really want to delete this recipe?")
    return redirect('http://127.0.0.1:8000/reci/profile/'+str(usrid))
    
def delwish(request,id,usrid):
   
    obj=whishlist.objects.filter(recepe=id)
     
    obj.delete() 
    if request.POST.get('page') == 'recipe':
            messages.error(request,"Recipe deleted from wishlist")
            return redirect('http://127.0.0.1:8000/reci/recipe/'+str(id))
    else:
            print("happening")
            messages.error(request,"Recipe deleted from wishlist")
            return redirect('http://127.0.0.1:8000/reci/wishlist/'+str(usrid))

def search(request):
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

            
    if request.method == 'GET':
        submitbutton= request.GET.get('submit')
        query= request.GET.get('ser')
        if query is not None:
            lookups= Q(title__icontains=query) | Q(descr__icontains=query)

            results= recipes.objects.filter(lookups).distinct()
            sum=0
            avglist=[]
            for i in results:
                        comment=comments.objects.filter(recipe=i.id)
                        if len(comment)!=0:
                            
                            for avg in comment:
                                sum=sum+avg.rating


                            average=round(sum/len(comment))
                        else:
                            average=0

                        avglist.append(average)
                        sum=0
            print(results)
            cat = category.objects.all()
            context={
                     'submitbutton': submitbutton,'data': zip(results,avglist),'cat':cat } 
           
            return render(request, 'index.html', context)

def edit(request,id):
    reci = recipes.objects.get(id=id)
    step=steps.objects.filter(recepe=id)
    cat=category.objects.all()
    incr=integredients.objects.filter(recipe=id)
    rec_cat=reciepe_category.objects.filter(recipe=id)
    cat_id=[]
    for i in rec_cat:
        cat_id.append(i.category.id)

    return render(request, 'edit.html',{'reci':reci,'step':step,'cat':cat,'incr':incr,'rec_cat':cat_id})
def updaterec(request,id):
     if request.method=='POST':
        post = recipes.objects.get(id=id)
        post.title= request.POST.get('title')
        post.descr= request.POST.get('descr')
        post.active_time= request.POST.get('active_time')
        post.total_time= request.POST.get('total_time')
        post.serves= request.POST.get('serves')
        post.save()
        usrid=request.user.id
        messages.success(request,"Recipe updated")
        return redirect('/reci/profile/'+str(usrid))



def cat_filter(request,id): 
    recip=reciepe_category.objects.filter(category=id)
    cat = category.objects.all()
    sum=0
    avglist=[]
    
    for i in recip:
            comment=comments.objects.filter(recipe=i.recipe.id)
            if len(comment)!=0:
                
                for avg in comment:
                    sum=sum+avg.rating


                average=round(sum/len(comment))
            else:
                average=0

            avglist.append(average)
            sum=0
    return render(request,'index.html',{'datas': zip(recip,avglist),'cat':cat})


def wish(request,id,recid):
    obj=whishlist()
    reci = recipes.objects.get(id=recid)
    obj.recepe=reci
    obj.author= request.user
    obj.save()
    messages.success(request,"Recipe added to wishlist")
    return redirect('http://127.0.0.1:8000/reci/recipe/'+str(recid))

def addrec(request):
    cat = category.objects.all()
    return render(request,'addrec.html',{'cat':cat})


def addrecinsert(request):
        if recipes.objects.filter(title=request.POST.get('title')).exists():
            messages.error(request,"Recipe title already exists,try with another!")
            return redirect('addrec')
        else:
            if request.POST.get('title') and request.POST.get('descr')and request.POST.get('active_time')and request.POST.get('total_time')and request.POST.get('serves'):
                post=recipes()
                img=request.FILES
                post.title= request.POST.get('title')
                post.descr= request.POST.get('descr')
                post.active_time= request.POST.get('active_time')
                post.total_time= request.POST.get('total_time')
                post.serves= request.POST.get('serves')
                post.image=request.FILES.get('image')
                post.author= request.user
                post.save()
                stpno=request.POST.getlist('steps[stepno]')
                stps=request.POST.getlist('steps[addstep]')
            
                for i in range(0,len(stpno)):
                    # print(stpno[i])
                    # print(stps[i])
                    post.steps_set.create(
                    step=stps[i],
                    order_no=stpno[i],
                    )
                ingr=request.POST.getlist('ingredients[no]')
                for i in ingr:
                    post.integredients_set.create(
                    ingredient=i,
                    )

                categoriesList=request.POST.getlist('categories')
                sam=recipes.objects.get(id=post.id)
                for i in categoriesList:
                    cate=reciepe_category()
                    cate.recipe=sam
                    cate.category=category.objects.get(id=i)
                    cate.save()
                
                messages.success(request,"Recipe added successfully!")
                return redirect('/')
            else: 
                messages.error(request,"Input Error!")
                return redirect('addrec')

    
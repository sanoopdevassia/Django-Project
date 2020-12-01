from django.db import models
from django.db import connections
from django.contrib.auth.models import User
from PIL import Image


class recipes(models.Model):
    
    title=models.CharField(max_length=200,unique=True)
    descr=models.TextField(default='SOME STRING',verbose_name="Recipes Description")
    active_time=models.TextField()
    total_time=models.TextField()
    serves=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    image=models.ImageField(upload_to='pics',default='SOME STRING')
    created_at=models.DateTimeField( auto_now_add=True)
    star=models.BooleanField(default=False)
    fivestarcount=models.IntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta: 
        verbose_name = "Recipe"
    
    
    # steps=models.ForeignKey(steps,on_delete=models.CASCADE)


class steps(models.Model):
    step=models.TextField()
    order_no=models.IntegerField()
    recepe=models.ForeignKey(recipes,on_delete=models.CASCADE)
  

class integredients(models.Model):
     ingredient=models.TextField()
     recipe=models.ForeignKey(recipes,on_delete=models.CASCADE)
    
class comments(models.Model):
    comment=models.TextField()
    rating=models.IntegerField(default=0)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    recipe=models.ForeignKey(recipes,on_delete=models.CASCADE)
    created_at=models.DateTimeField( auto_now_add=True)
    class Meta:
        verbose_name = "Comment"
  
class whishlist(models.Model):
    recepe=models.ForeignKey(recipes,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
class category(models.Model):
    category_name=models.TextField()
    class Meta:
        verbose_name = "Categorie"
    

class reciepe_category(models.Model):
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    recipe=models.ForeignKey(recipes,on_delete=models.CASCADE)
    
    
    


    



    



    

    
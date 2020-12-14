from django.urls import path
from .import views

urlpatterns = [
    
     path('recipe/<int:id>',views.recipe,name='recipe'),
     path('sign-up',views.sigup,name='sign-up'),
     path('wishlist/<int:id>',views.wishlist,name='wishlist'),
     path('addrec',views.addrec,name='addrec'),
     path('addrecinsert',views.addrecinsert,name='addrecinsert'),
     path('sign-in',views.signin,name='sign-in'),
     path('comment/<int:id>',views.comment,name='comment'),
     path('delcomment/<int:id>/<int:recid>',views.delcomment,name='delcomment'),
     path('wish/<int:id>/<int:recid>',views.wish,name='wish'),
     path('delwish/<int:id>/<int:usrid>',views.delwish,name='delwish'),
     path('search',views.search,name='search'),
     path('profile/<int:id>',views.profile,name='profile'),
     path('update/<int:id>',views.update,name='update'),
     path('edit/<int:id>',views.edit,name='edit'),
     path('delrecipe/<int:recid>/<int:usrid>',views.delrecipe,name='delrecipe'),
     path('updaterec/<int:id>',views.updaterec,name='updaterec'),
     path('pdf/<int:id>',views.pdf,name='pdf'),
     path('cat_filter/<int:id>',views.cat_filter,name='cat_filter'),
     path('warning/<int:id>/<int:recid>',views.warning,name='warning'),
     path('recwarning/<int:recid>/<int:usrid>',views.recwarning,name='recwarning'),

      
      
     

]

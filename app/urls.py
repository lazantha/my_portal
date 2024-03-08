from django.urls import path
from . import views

urlpatterns = [
	path('test/', views.testing,name='test'),
    path('', views.home,name='homePage'),
	path('aboutUs/', views.aboutUs,name='aboutUs'),
	path('contactUs/', views.contactUs,name='contactUs'),
	path('userLogin/', views.userLogin,name='userLogin'),
	path('userSignUp/', views.userSignUp,name='userSignUp'),
	path('userHome/', views.userHome,name='userHome'),
	path('delete/<int:post_id>/', views.delete,name='delete'),
	path('update/<int:post_id>/', views.update,name='update'),
	path('adminPost/', views.adminPost,name='adminPost'),
    path('upload/', views.upload,name='upload'),
    path('signOut/', views.signOut,name='signOut'),
    
    
    
]

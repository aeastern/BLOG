from django.urls import path
from . import views
#from userprofile.views import uploadImg # 添加
app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    # 用户退出
    path('logout/', views.user_logout, name='logout'),
    # 用户注册
    path('register/', views.user_register, name='register'),
    # 用户信息
    path('edit/<int:id>/', views.profile_edit, name='edit'),
  #  path('edit/<int:id>/', views.showImg, name='showImg'),
    path('edit/<int:id>/', views.showImg, name='showImg'),
    path('uploadImg/', views.uploadImg, name='uploadImg'),
   path('showImg/', views.showImg, name='showImg'),
    # 用户删除
    path('delete/<int:id>/', views.user_delete, name='delete'),


]
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Trang chủ
    path('', views.home, name='home'),
    
    # Nhóm chức năng đăng nhập, đăng ký, quên mật khẩu
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),

    # Xác thực email và đặt lại mật khẩu
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    # Nhóm chức năng quản lý
    path('quanlituyendung/', views.quanlituyendung, name='quanlituyendung'),
    path('lichphongvan/', views.lichphongvan, name='lichphongvan'),
    path('chuongtrinhdaotao/', views.chuongtrinhdaotao, name='chuongtrinhdaotao'),
    path('theodoihieusuat/', views.theodoihieusuat, name='theodoihieusuat'),
    path('giaotiepvaphanhoi/', views.giaotiepvaphanhoi, name='giaotiepvaphanhoi'),
    path('quanlyhoso/', views.quanlyhoso, name='quanlyhoso'),
    path('baocaovaphantich/', views.baocaovaphantich, name='baocaovaphantich'),
    path('cauhinhhethong/', views.cauhinhhethong, name='cauhinhhethong'),
    path('baomatvaquyenhan/', views.baomatvaquyenhan, name='baomatvaquyenhan'),

    # Nhóm chức năng cá nhân
    path('myprofile/', views.myprofile, name='myprofile'),
    path('reports/', views.reports, name='reports'),
    path('helpvasupport/', views.helpvasupport, name='helpvasupport'),
]

# Phục vụ file media trong môi trường DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
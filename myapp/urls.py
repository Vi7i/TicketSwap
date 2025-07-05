
from django.urls import path
from myapp import views
from django.urls import re_path
from django.conf.urls.static import static
from django.conf import settings
from .views import approve_user


urlpatterns = [
    path("",views.startpage,name='startpage'),
    path("login/",views.login1,name="login"),
    path("verify_email",views.verify_email,name="verify_email"),
    re_path(r'^register1/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<token>\w+)/$', views.confirmedemail, name='confirmedemail'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
    path("home",views.home,name='home'),
    path("home/profile",views.profile,name="profile"),
    path("home/profile/view/<int:id>",views.profile_view,name="profile_view"),
    path("home/alltickets",views.all_tickets,name="alltickets"),
    path("book/<int:ticket_id>",views.book,name="book"),
    path("home/uploads",views.view_uploads,name="myuploads"),
    path("mybooks",views.my_books,name="mybooks"),
    path("complaint/<int:ticket_id>",views.complaint,name="complaint"),
    path("payment/<int:bookedid>",views.payment,name="payment"),
    path("thankyou/<int:bookedid>",views.thankyou,name="thankyou"),
    path("download_ticket/<int:bookedid>", views.download_ticket, name="download_ticket"),
    path("admin_user/delete_user/<int:id>",views.delete_user,name="delete_user"),
    path('admin_user/<int:user_id>/', approve_user, name='approve_user'),
    path("admin_user/delete_complaint/<int:id>",views.delete_complaint,name="delete_complaint"),
    path("admin_user/delete_ticket/<int:id>",views.delete_ticket,name="delete_ticket"),
    # path('upload/', views.upload_ticket, name='upload_ticket'),
    path("logout/",views.logoutuser,name="logout")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
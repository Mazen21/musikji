from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users import views as user_views
from archive import views as archive_views

urlpatterns = [
    path('',archive_views.home, name="musikji_home"),
    path('admin/', admin.site.urls),
    path('archive/', include('archive.urls')),
    path('backoffice/', include('backoffice.urls')),
    path('register/', user_views.register, name="register"),
    path('activate/<uidb64>/<token>/',user_views.activate, name='activate'),  
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('profile/', user_views.profile, name="profile"),
    path('profile/<int:user_id>', user_views.profile_detail, name="profile_detail"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html"), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),
    path('message/<int:receiver_id>', user_views.send_message, name="send_message"),
    path('message_detail/<int:msg_id>', user_views.message_detail, name="message_detail"),
    path('summernote/', include('django_summernote.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

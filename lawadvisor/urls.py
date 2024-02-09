from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from Account.views import (
    registration_view,
    logout_view,
    login_view,
)

from home.views import (
    home_view,
    project_view,
)

from chatbot.views import(
    chatbot_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Account.urls', namespace='account')),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', registration_view, name="register"),
    path('', home_view , name="home"),
    path('project/', project_view, name="project"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_changedone.html'),
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_resetdone.html'),
        name='password_reset_done'),
 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_resetform.html'),
        name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_resetcomplete.html'),
        name='password_reset_complete'),
    path('chatbot/', chatbot_view, name='chatbot_view'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
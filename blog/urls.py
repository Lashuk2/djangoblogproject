from blog import views
from django.urls import path
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.post_list, name='home'),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='reset/password_reset.html',
        email_template_name='reset/password_reset_email.html',
        subject_template_name='reset/password_reset_subject.txt'), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset/password_reset_complete.html'), name='password_reset_complete'),
    path('settings/account/', accounts_views.UserUpdateView.as_view(), name='my_account'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='change/password_change.html'), name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='change/password_change_done.html'), name='password_change_done'),
    path('tag/<tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('like/<slug:slug>/', views.post_like, name='like'),
    path('dislike/<slug:slug>/', views.post_dislike, name='dislike'),
]

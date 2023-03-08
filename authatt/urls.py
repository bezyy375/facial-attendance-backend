from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views

from users_auth.attendance_api import AttendanceViewSet
from users_auth.members_api import MemberViewSet
from users_auth.users_apis import RegistrationView, LoginView, LogoutView

router = DefaultRouter()
router.register(r'member', MemberViewSet, basename='members')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='register'),
    path('token-refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    *router.urls,
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, include
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import handler404, handler500

from core.views import custom_404_view, custom_500_view

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

handler404 = custom_404_view
handler500 = custom_500_view

urlpatterns = [
    path('auth/locate/user/admin/', admin.site.urls),
    path('', include('core.urls')),
    path('chat/ai/', include('bot.urls')),
    path('auth/user/', include('user.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # path('rest', include('rest_framework.urls')),
    # path('settings/api/secret/', include('base.urls')),

 
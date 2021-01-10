from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import  get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include('blog_api.urls', namespace='blog_api')),
    path('api/user/', include('users.urls', namespace='users')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('blog.urls', namespace='blog')),
    path('docs/', include_docs_urls(title='BlogAPI')),
    path('schema', get_schema_view(
        title="BlogAPI",
        description="API for the BlogAPI",
        # version="1.0.0"
    ), name='openapi-schema'),
    path('auth/', obtain_auth_token),
url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
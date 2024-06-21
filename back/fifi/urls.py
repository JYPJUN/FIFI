"""
URL configuration for fifi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts 관련 url
    path('api/v1/accounts/', include('accounts.urls')), # 일반 accounts 사용 시
    path('accounts/', include('dj_rest_auth.urls')), # allauth 라이브러리 사용
    path('accounts/signup/', include('dj_rest_auth.registration.urls')), # allauth 회원가입
    path('accounts/logout/', include('dj_rest_auth.registration.urls')), # allauth 로그아웃
    
    # article 관련 url   
    path('api/v1/articles/', include('articles.urls')),
    
    # exchange 관련 url
    path('api/v1/exchange/', include('exchange.urls')),
    
    # product 관련 url
    path('api/v1/products/', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # static 및 media 경로 설정

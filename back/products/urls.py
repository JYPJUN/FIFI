
from django.urls import path
from . import views

urlpatterns = [
    # 금융 회사 DB
    path('', views.getcompany), 
    path('getAPIcompany/', views.getAPIcompany), # 금융 회사 데이터 얻기
    
    # 금융회사 좋아요
    path('<int:company_pk>/likes/', views.likes),
    path('company/likes/', views.userlike),

    
    # 금융 예금 확인
    path('getTimeDepogit/', views.getTimeDepogit), # 정기 예금 DB
    path('getAPITimeDepogit/', views.getAPITimeDepogit), # 정기 예금 데이터 & 옵션 얻기
    path('getTimeDepogitOption/', views.getTimeDepogitOption), # 정기 예금 옵션 DB
    path('getTimeDepogitOption/<str:fin_prdt_cd>/', views.getTimeDepogitOptionDetail), # 정기 예금 옵션 세부데이터 얻기
    
    # 금융 적금 확인
    path('getAPISaving/', views.getAPISaving), # 적금 데이터 & 옵션 얻기
    path('getSaving/', views.getSaving), # 적금 DB 데이터
    path('getSavingOption/', views.getSavingOption), # 적금 옵션 DB 데이터
    path('getSavingOption/<str:fin_prdt_cd>/', views.getSavingOptionDetail), # 적금 옵션 세부데이터 얻기
    
    # 상품 가입
    path('deposit/<int:deposit_pk>/join/', views.depositjoin), # 정기예금 가입
    path('deposit/signup/', views.depositsignup), # 유저가 가입한 상품 다 찾기
    
    path('saving/<int:saving_pk>/join/', views.savingjoin), # 정기적금 가입
    path('saving/signup/', views.savingsignup), # 유저가 가입한 상품 다 찾기
    
    # 금융 상품 추천
    path('deposit/getrecommendproduct/', views.getRdeposit),
    path('saving/getrecommendproduct/', views.getRsaving),
    
]

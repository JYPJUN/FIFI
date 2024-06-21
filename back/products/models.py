from django.db import models
from django.conf import settings

# Create your models here.
# 회사 정보
class FinancialCompany(models.Model):
    fin_co_no = models.IntegerField() # 금융회사코드 ex) 0010001
    kor_co_nm = models.CharField(max_length=100) # 금융회사 명 ex) 우리은행
    homp_url = models.URLField() # 금융회사 홈페이지 주소 URL ex) https://spot.wooribank.com/pot/Dream?withyou=po
    cal_tel = models.CharField(max_length=100) # 금융회사 콜센터번호 ex) 15885000
    
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_company')

# 예금
class TimeDeposit(models.Model):
    kor_co_nm = models.CharField(max_length=100) # 금융회사 명
    fin_prdt_cd = models.CharField(max_length=100) # 금융상품 코드
    fin_prdt_nm = models.CharField(max_length=100) # 금융상품 명
    join_way = models.CharField(max_length=500) # 가입방법
    mtrt_int = models.CharField(max_length=500) # 만기 후 이자율
    spcl_cnd = models.CharField(max_length=500) # 우대조건
    join_deny = models.CharField(max_length=5) # 가입 제한
    join_member = models.CharField(max_length=100) # 가입 대상
    etc_note = models.CharField(max_length=500) # 기타 유의사항
    max_limit = models.IntegerField(null=True) #최고한도
    
    joinDeposit = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joinD')
    
class TimeDepositOption(models.Model):
    deposit = models.ForeignKey(TimeDeposit, on_delete=models.CASCADE) # 금융상품 코드
    intr_rate_type_nm = models.CharField(max_length=2) # 저축 금리 유형
    save_trm = models.CharField(max_length=5) # 저축기간 [단위: 개월]
    intr_rate = models.FloatField() # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField() #최고 우대금리 [소수점 2자리]
    

# 적금
class Saving(models.Model):
    kor_co_nm = models.CharField(max_length=100) # 금융회사 명
    fin_prdt_cd = models.CharField(max_length=100) # 금융상품 코드
    fin_prdt_nm = models.CharField(max_length=100) # 금융상품 명
    join_way = models.CharField(max_length=500) # 가입방법
    mtrt_int = models.CharField(max_length=500) # 만기 후 이자율
    spcl_cnd = models.CharField(max_length=500) # 우대조건
    join_deny = models.CharField(max_length=5) # 가입 제한
    join_member = models.CharField(max_length=100) # 가입 대상
    etc_note = models.CharField(max_length=500) # 기타 유의사항
    max_limit = models.IntegerField(null=True) #최고한도
    
    joinSaving = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joinS')
    
class SavingOption(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE) # 금융상품 코드
    intr_rate_type_nm = models.CharField(max_length=2) # 저축 금리 유형
    save_trm = models.CharField(max_length=5) # 저축기간 [단위: 개월]
    intr_rate = models.FloatField() # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField() #최고 우대금리 [소수점 2자리]
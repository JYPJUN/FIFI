from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.
class Exchange(models.Model):
  date = models.DateField() # 환율 일자
  cur_unit = models.CharField(max_length=100) # 통화코드 ex) AED
  cur_nm = models.CharField(max_length=100) # 국가/통화명 ex) 아랍에미리트 디르함
  ttb = models.FloatField() # 전신환(송금) 받을 때 ex) 342.04
  tts = models.FloatField() # 전신환(송금) 보낼 때 ex) 348.95
  deal_bas_r = models.FloatField() # 매매 기준율 ex) 345.5
  
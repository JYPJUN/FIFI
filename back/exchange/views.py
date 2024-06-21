from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Exchange
from .serializers import ExchangeSerializer
from datetime import datetime, timedelta
import requests
from django.conf import settings


# Create your views here.

# Exchange 정보 API로 호출
@api_view(['GET'])
@permission_classes([AllowAny])
def getAPIExchange(request):
  s_date = '20230101' # 시작 날짜
  e_date = '20231231' # 끝 날짜
  start_date_formatted = datetime.strptime(s_date, '%Y%m%d').date()
  end_date_formatted = datetime.strptime(e_date, '%Y%m%d').date()
  while start_date_formatted <= end_date_formatted:
    # settings.EXCHANGE_API_KEY
    EXCHANGE = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&searchdate={start_date_formatted}&data=AP01'

    if len(EXCHANGE) >= 1:
      existing_date = Exchange.objects.filter(date=start_date_formatted)
    else:
      start_date_formatted += timedelta(days=1)
      continue
    
    if existing_date.exists():
      start_date_formatted += timedelta(days=1)
      continue
    else:
      response = requests.get(EXCHANGE).json()
      for item in response:
        item['ttb'] = float(item['ttb'].replace(',', ''))
        item['tts'] = float(item['tts'].replace(',', ''))
        item['deal_bas_r'] = float(item['deal_bas_r'].replace(',', ''))
        serializer = ExchangeSerializer(data=item)
        if serializer.is_valid(raise_exception=True):
            serializer.save(date=start_date_formatted)
    start_date_formatted += timedelta(days=1)
    
  real_data = Exchange.objects.all()
  serializer = ExchangeSerializer(real_data, many=True)
  
  return Response(serializer.data, status=status.HTTP_200_OK)


# Exchange 환율 정보 얻기
@api_view(['GET'])
@permission_classes([AllowAny])
def getExchange(request):
  data = Exchange.objects.all()
  serializer = ExchangeSerializer(data, many=True)
  
  return Response(serializer.data, status=status.HTTP_200_OK)


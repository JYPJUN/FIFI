from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import FinancialCompany, TimeDeposit, TimeDepositOption, Saving, SavingOption
from .serializers import CompanySerializer, TimeDeopositSerializer, OptionSerializer, SavingSerializer, SavingOptionSerializer
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import date
from django.db.models import Count, Sum
import pandas as pd

User = get_user_model()

# Create your views here.
# 은행 회사 정보
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAPIcompany(request): # 은행 정보 API로 받아오기
    COMPANY = f'http://finlife.fss.or.kr/finlifeapi/companySearch.json?auth={settings.PRODUCT_API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(COMPANY).json()
    for data in response['result']['baseList']:
        existing_company = FinancialCompany.objects.filter(fin_co_no = data['fin_co_no'])
        if existing_company.exists():
            continue
        else:
            serializer = CompanySerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    
    real_data = FinancialCompany.objects.all()
    real_serializer = CompanySerializer(real_data, many=True)
    
    return Response(real_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def getcompany(request): # 은행 정보 DB에서 가져오기
    data = FinancialCompany.objects.all()
    serializer = CompanySerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likes(request,company_pk): # 금융회사 좋아요 기능 
    company = FinancialCompany.objects.get(pk=company_pk)
    if request.user in company.like_users.all():
        company.like_users.remove(request.user)
        return Response({ "detail": "좋아요를 삭제 하셨습니다."}, status=status.HTTP_200_OK)
    else:
        company.like_users.add(request.user)
        return Response({ "detail": "좋아요를 추가 하셨습니다."}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def userlike(request):
    user = request.user
    companylist = user.like_company.all()  # 가입한 적금 상품 다 가져오기
    serializer = CompanySerializer(companylist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 정기 예금 데이터
@api_view(['GET'])
@permission_classes([AllowAny])
def getAPITimeDepogit(request):
    TimeDepogitOption = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={settings.PRODUCT_API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(TimeDepogitOption).json()
    # 정기 예금 데이터 저장
    for data in response['result']['baseList']:
        if TimeDeposit.objects.filter(fin_prdt_cd=data['fin_prdt_cd']).exists():
            continue
        serializer = TimeDeopositSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    # 정기 예금 옵션 데이터 저장
    for data in response['result']['optionList']:
        deposit = TimeDeposit.objects.get(fin_prdt_cd=data['fin_prdt_cd'])
        serializer = OptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(deposit=deposit)
    real_data = TimeDeposit.objects.all()
    real_serializer = TimeDeopositSerializer(real_data, many=True)
    
    return Response(real_serializer.data, status=status.HTTP_200_OK)

# 정기 예금 정보 DB 얻기
@api_view(['GET'])
@permission_classes([AllowAny])
def getTimeDepogit(request):
    data = TimeDeposit.objects.all()
    serializer = TimeDeopositSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 정기 예금 옵션 DB 얻기
@api_view(['GET'])
@permission_classes([AllowAny])
def getTimeDepogitOption(request):
    data = TimeDepositOption.objects.all()
    serializer = OptionSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def getTimeDepogitOptionDetail(request, fin_prdt_cd):
    deposit = get_object_or_404(TimeDeposit, fin_prdt_cd=fin_prdt_cd)
    data = TimeDepositOption.objects.filter(deposit=deposit)
    serializer = OptionSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 적금 데이터 얻기
@api_view(['GET'])
@permission_classes([AllowAny])
def getAPISaving(request):
    SavingOption = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={settings.PRODUCT_API_KEY}&topFinGrpNo=020000&pageNo=1'
    
    response = requests.get(SavingOption).json()
    # 정기 적금 데이터 저장
    for data in response['result']['baseList']:
        if Saving.objects.filter(fin_prdt_cd=data['fin_prdt_cd']).exists():
            continue
        serializer = SavingSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    # 정기 적금 옵션 데이터 저장
    for data in response['result']['optionList']:
        saving = Saving.objects.get(fin_prdt_cd=data['fin_prdt_cd'])
        serializer = SavingOptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(saving=saving)
    real_data = Saving.objects.all()
    real_serializer = SavingSerializer(real_data, many=True)
    
    return Response(real_serializer.data, status=status.HTTP_200_OK)

# 적금 DB 데이터 얻기
@api_view(['GET'])
@permission_classes([AllowAny])
def getSaving(request):
    data = Saving.objects.all()
    serializer = SavingSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def getSavingOption(request):
    data = SavingOption.objects.all()
    serializer = SavingOptionSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def getSavingOptionDetail(request, fin_prdt_cd) :
    saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
    data = SavingOption.objects.filter(saving=saving)
    serializer = SavingOptionSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny])
def depositjoin(request, deposit_pk):
    deposit = TimeDeposit.objects.get(pk=deposit_pk)
    if request.user in deposit.joinDeposit.all():
        deposit.joinDeposit.remove(request.user)
        return Response({ "detail": "상품 가입을 해지하셨습니다."}, status=status.HTTP_200_OK)
    else:
        deposit.joinDeposit.add(request.user)
        return Response({ "detail": "상품을 가입하셨습니다."}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def depositsignup(request):
    user = request.user
    joinD = user.joinD.all()  # 가입한 예금 상품 다 가져오기
    serializer = TimeDeopositSerializer(joinD, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def savingjoin(request, saving_pk):
    saving = Saving.objects.get(pk=saving_pk)
    if request.user in saving.joinSaving.all():
        saving.joinSaving.remove(request.user)
        return Response({"join":False, "detail": "상품 가입을 해지하셨습니다."}, status=status.HTTP_200_OK)
    else:
        saving.joinSaving.add(request.user)
        return Response({"join":True, "detail": "상품을 가입하셨습니다."}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def savingsignup(request):
    user = request.user
    joinS = user.joinS.all()  # 가입한 적금 상품 다 가져오기
    serializer = SavingSerializer(joinS, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

############################################################

# 상품 추천 알고리즘에 필요한 함수 구현
# 나이는 25% 의 가산점
# 연봉은 35% 의 가산점
# 선호도는 20% 의 가산점
# 상품가입유저수는 20% 의 가산점

## 나이가중치구하기
def age_point(user_age, other_user_age):
    percentage = other_user_age / user_age * 100 if other_user_age != 0 else 0
    if percentage < 20:
        return 1
    elif percentage < 50:
        return 0.75
    elif percentage < 75:
        return 0.5
    elif percentage < 100:
        return 0.25
    else:
        return 0

## 연봉가중치구하기
def income_point(user_income, other_user_income):
    percentage = abs(user_income - other_user_income) / user_income * 100
    if percentage < 20:
        return 1
    elif percentage < 50:
        return 0.75
    elif percentage < 75:
        return 0.5
    elif percentage < 100:
        return 0.25
    else:
        return 0

## 회사선호도가중치구하기
def company_point(total_likes, s_likes):
    percentage = s_likes / total_likes * 100 if s_likes != 0 else 0
    if percentage < 20:
        return 0.25
    elif percentage < 50:
        return 0.5
    elif percentage < 75:
        return 0.75
    elif percentage < 100:
        return 1
    else:
        return 0
    
## 가입유저가중치구하기
def deposit_point(total_user, other_sign_user):
    percentage = other_sign_user / total_user * 100 if other_sign_user != 0 else 0
    if percentage < 20:
        return 0.25
    elif percentage < 50:
        return 0.5
    elif percentage < 75:
        return 0.75
    elif percentage < 100:
        return 1
    else:
        return 0


## 나이 계산하기    
def find_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

## 가입한 유저들의 평균 나이 계산하기
def get_average_age_income(value, num):
    if num == 1:
        users = value.joinDeposit.all()
    else:
        users = value.joinSaving.all()
        
    users_with_income = users.exclude(income__isnull=True)
    if not users_with_income.exists():
        return None, None
    # 나이 계산
    total_age = sum(find_age(user.birth_date) for user in users)
    average_age = total_age / users.count()
    # 소득 계산
    total_income = sum(user.income for user in users if user.income is not None)
    average_income = total_income / users.count()
    return average_age, average_income

@api_view(['GET'])
@permission_classes([AllowAny])
def getRdeposit(request):
    request_user_age = find_age(request.user.birth_date)
    request_user_income = request.user.income
    deposits = TimeDeposit.objects.all()
    
    records = []
    
    total_company_likes = FinancialCompany.objects.annotate(like_count=Count('like_users')).aggregate(total_likes=Sum('like_count'))['total_likes']
    total_user = User.objects.count()
    
    for deposit in deposits:
        average_age, average_income = get_average_age_income(deposit, 1)
        if average_age is None or average_income is None:
            continue
        
        company = FinancialCompany.objects.get(kor_co_nm=deposit.kor_co_nm)
        company_recommend = company.like_users.count()
        deposit_sign_user = deposit.joinDeposit.count()
        
        point_age = age_point(request_user_age, average_age) * 0.25
        point_income = income_point(request_user_income, average_income) * 0.35
        point_company = company_point(total_company_likes, company_recommend) * 0.2
        point_deposit_sign = deposit_point(total_user, deposit_sign_user) * 0.2
        
        
        records.append({
            'deposit_company': deposit.kor_co_nm,
            'deposit_name': deposit.fin_prdt_nm,
            'id': deposit.id,
            'age': point_age,
            'income': point_income,
            'preference': point_company,
            'user_count': point_deposit_sign,
            'total_score': point_age + point_income + point_company + point_deposit_sign
        })
    return Response(records, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def getRsaving(request):
    request_user_age = find_age(request.user.birth_date)
    request_user_income = request.user.income
    savings = Saving.objects.all()
    
    records = []
    
    total_company_likes = FinancialCompany.objects.annotate(like_count=Count('like_users')).aggregate(total_likes=Sum('like_count'))['total_likes']
    total_user = User.objects.count()
    
    for saving in savings:
        average_age, average_income = get_average_age_income(saving, 2)
        if average_age is None or average_income is None:
            continue
        
        company = FinancialCompany.objects.get(kor_co_nm=saving.kor_co_nm)
        company_recommend = company.like_users.count()
        saving_sign_user = saving.joinSaving.count()
        
        point_age = age_point(request_user_age, average_age) * 0.25
        point_income = income_point(request_user_income, average_income) * 0.35
        point_company = company_point(total_company_likes, company_recommend) * 0.2
        point_saving_sign = deposit_point(total_user, saving_sign_user) * 0.2
        
        
        records.append({
            'saving_company': saving.kor_co_nm,
            'saving_name': saving.fin_prdt_nm,
            'id': saving.id,
            'age': point_age,
            'income': point_income,
            'preference': point_company,
            'user_count': point_saving_sign,
            'total_score': point_age + point_income + point_company + point_saving_sign
        })
    return Response(records, status=status.HTTP_200_OK)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import ArticleListSerializer,ArticleSerializer,CommentSerializer
from .models import Article,Comment
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count
import logging
logger = logging.getLogger(__name__)

# 게시글 조회, 생성
@api_view(['GET','POST'])
@permission_classes([AllowAny])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by('-pk')
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = ArticleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        
# 좋아요 많은 순으로 게시글 조회
@api_view(['GET'])
@permission_classes([AllowAny])
def article_list_by_likes(request):
    try:
        articles = Article.objects.annotate(
            like_count=Count('like_users')
        ).order_by('-like_count', '-pk')  # 좋아요 수와 작성 날짜에 따라 내림차순으로 정렬
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error retrieving articles by likes: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# 내가 작성한 게시글 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_article_list(request):
    articles = Article.objects.filter(user=request.user).order_by('-pk')
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 게시글 Detail
@api_view(['GET','DELETE','PUT'])
@permission_classes([AllowAny])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE' or request.method == 'PUT':
        if request.user.is_authenticated:
            if request.method == 'DELETE':
                article.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif request.method == 'PUT':
                serializer = ArticleSerializer(article, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comment_list(request, article_pk):
    if request.method == "GET":
        comments = Comment.objects.filter(article_id=article_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        if request.user.is_authenticated:
            article = get_object_or_404(Article, pk=article_pk)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(article=article, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET','DELETE','PUT'])
@permission_classes([AllowAny])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if comment.user == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        if comment.user == request.user:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

# like
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likes(request,article_pk):
    article= Article.objects.get(pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    article.save()
    return Response({'like_users': [user.username for user in article.like_users.all()]}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_articles(request):
    user = request.user
    liked_articles = user.like_articles.all()  # 좋아요를 누른 게시글 가져오기
    serializer = ArticleListSerializer(liked_articles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
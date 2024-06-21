from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import CustomUserDetailsSerializer

class ArticleListSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    image = serializers.ImageField(read_only=True)
    
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content',)
    
    comment_set = CommentDetailSerializer(read_only=True, many=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', )

class ArticleSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)  # 선택 사항으로 설정

    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content',)
    
    comment_set = CommentDetailSerializer(read_only=True, many=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', )
        extra_kwargs = {
            'like_users': {'required': False, 'allow_empty': True}
        }

class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)

    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title',)

    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

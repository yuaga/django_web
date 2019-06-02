from rest_framework import serializers
from apps.blog.serializers import UserSerializers
from apps.news.models import Category, News, Comment


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    comment_author = UserSerializers()

    class Meta:
        model = Comment
        fields = ('id', 'pub_time', 'comment_content', 'comment_author', 'origin_comment')


class NewsListSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializers()

    class Meta:
        model = News
        fields = ('id', 'title', 'intro', 'category', 'author', 'pub_time','up_num','views')



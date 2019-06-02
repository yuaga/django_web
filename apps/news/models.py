from django.db import models
from apps.blog.models import User


# 文章分类模型
class Category(models.Model):
    name = models.CharField(max_length=10)


# 文章模型
class News(models.Model):
    title = models.CharField(max_length=100)  # 标题
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 作者
    intro = models.CharField(max_length=250)  # 文章简述
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default='个人博客')
    pub_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    content = models.TextField()  # 文章内容
    up_num = models.IntegerField(default=0, blank=True, null=True)  # 文章点赞数
    views = models.PositiveIntegerField(default=0)  # 文章浏览数

    class Meta:
        ordering = ['-pub_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


# 评论模型
class Comment(models.Model):
    comment_content = models.TextField(max_length=150)  # 评论内容
    pub_time = models.DateTimeField(auto_now_add=True)  # 评论创建时间
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)  # 评论作者
    comment_news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')  # 给哪个文章写的评论
    origin_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)  # 2级评论，可以为空

    class Meta:
        ordering = ['-pub_time']


# 点赞记录模型
class UpAndDown(models.Model):

    up_user = models.ForeignKey(User, related_name='up_user', on_delete=models.CASCADE)  # 点赞人
    up_news = models.ForeignKey(News, related_name='up_news', on_delete=models.CASCADE)  # 点赞的文章
    up = models.BooleanField(default=0)  # 记录是否对这个文章有过点赞

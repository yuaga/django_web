from django import forms
from apps.forms import FormMixin


class CommentForm(forms.Form, FormMixin):
    comment_content = forms.CharField(max_length=150, error_messages={'max_length': '评论最多150个字哦！'})
    news_id = forms.IntegerField()
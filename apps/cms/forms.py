from django import forms
from apps.forms import FormMixin


class WriteNewsForms(forms.Form, FormMixin):
    title = forms.CharField(max_length=100, error_messages={
        'max_length': '标题太长了！',
        'required': '标题不要忘了写！'
    })
    category = forms.IntegerField(error_messages={
        'required': '分类不要忘了写！'
    })
    intro = forms.CharField(max_length=250, error_messages={
        'max_length': '摘要太长了！',
        'required': '不要忘了写摘要！'
    })
    content = forms.CharField(error_messages={
        'required': '不要忘了写文章内容！'
    })


class EditNewsForm(forms.Form, FormMixin):
    id = forms.IntegerField()
    title = forms.CharField(max_length=100, error_messages={
        'max_length': '标题太长了！',
        'required': '标题不要忘了写！'
    })
    category = forms.IntegerField(error_messages={
        'required': '分类不要忘了写！'
    })
    intro = forms.CharField(max_length=200, error_messages={
        'max_length': '摘要太长了！',
        'required': '不要忘了写摘要！'
    })
    content = forms.CharField(error_messages={
        'required': '不要忘了写文章内容！'
    })

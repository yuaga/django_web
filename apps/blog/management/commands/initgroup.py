from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType
from apps.news.models import News, Category, Comment


class Command(BaseCommand):

    def handle(self, *args, **options):
        # 编辑组
        # 先通过模型找到对应的content_type
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(Category),
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        edit_group = Group.objects.create(name='编辑组')
        edit_group.permissions.set(edit_permissions)
        edit_group.save()
        self.stdout.write(self.style.SUCCESS('编辑组创建成功'))

        # 管理组
        manage_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(Category),
            ContentType.objects.get_for_model(Comment),
        ]
        manage_permissions = Permission.objects.filter(content_type__in=manage_content_types)
        manage_group = Group.objects.create(name='管理组')
        manage_group.permissions.set(manage_permissions)
        manage_group.save()
        self.stdout.write(self.style.SUCCESS('管理创建好了'))
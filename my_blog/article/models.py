from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse
#栏目类
class ArticleColumn(models.Model):
    #名字
    title = models.CharField(max_length=100, blank=True)
    #日期
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    #参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。
    author = models.ForeignKey(User, on_delete=models.CASCADE)#ForeignKey是用来解决“一对多”问题的，用于关联查询。
    title = models.CharField(max_length=100)#字段（field）表示数据库表的一个抽象类
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    # 头像
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    #浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    #处理图片函数,先保存再处理
    def save(self,*args,**kwargs):
        article = super(ArticlePost, self).save(*args, **kwargs)
        #缩放，保持纵横比
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    # 模型元数据是“任何不是字段的东西”，例如排序选项ordering、
    # 数据库表名db_table、单数和复数名称verbose_name和
    # verbose_name_plural。要不要写内部类是完全可选的，
    # 当然有了它可以帮助理解并规范类的行为。
    class Meta:
        ordering = ('-created',)#时间倒序
    #返回文章标题
    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
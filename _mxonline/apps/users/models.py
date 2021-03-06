from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    nick_name=models.CharField(max_length=50,verbose_name=u'昵称',default="");
    birday=models.DateField(verbose_name=u"生日",default=datetime.now);#null=True, blank=True
    gender=models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")),default="male");
    address=models.CharField(max_length=100,default="");
    mobile=models.CharField(max_length=11,null=True,blank=True);
    image=models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png",max_length=100);

    class Meta:
        verbose_name=u"用户信息";
        verbose_name_plural=verbose_name;

    def __str__(self):
        return self.username;

    def get_unread(self):
        """获取用户未读的消息
        """
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count();


#邮箱验证
class EmailVerifyRecord(models.Model):
    code=models.CharField(max_length=20,verbose_name=u"验证码");
    email=models.EmailField(max_length=50,verbose_name=u"邮箱");
    send_type=models.CharField(verbose_name=u'发送类型',max_length=30,choices=(("register",u"注册"),("forget",u"密码"),("update_email",u"修改邮箱")))
    send_time=models.DateTimeField(default=datetime.now,verbose_name=u"发送时间");

    class Meta:
        verbose_name=u"邮箱验证码";
        verbose_name_plural=verbose_name;
#轮播图
class Banner(models.Model):
    title=models.CharField(max_length=100,verbose_name=u"标题");
    image=models.ImageField(upload_to="banner/%Y/%m",verbose_name=u"轮播图",max_length=100);
    url=models.URLField(max_length=200,verbose_name=u"访问地址");
    index=models.IntegerField(default=100,verbose_name=u"顺序");
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间");

    class Meta:
        verbose_name=u"轮播图";
        verbose_name_plural=verbose_name;

    def __str__(self):
        return self.title;



from django.db import models
from django.contrib.auth.models import AbstractUser
from sorl.thumbnail import ImageField, get_thumbnail
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField


class NSuser(AbstractUser):
    USERNAME_FIELD = 'username'
    phone_number = PhoneNumberField(null=True, unique=True)
    photo = models.OneToOneField('Photo', blank=True, null=True)
    news_read = models.IntegerField(null=True, blank=True, default=0)
    news_added = models.IntegerField(null=True, blank=True, default=0)
    news_rejected = models.IntegerField(null=True, blank=True, default=0)
    news_views = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.username)

    def number(self):
        return str("{} {} {}".format(self.phone_number[0:4],
                                     self.phone_number[4:6],
                                     self.phone_number[6:]))


class NewsPost(models.Model):
    author = models.ForeignKey('NSuser', null=True, blank=True)
    post_header = models.TextField(null=True, blank=True, default="There must be header")
    post_category = models.ForeignKey('Category', null=True)
    post_content = RichTextField(null=True)
    post_photo = models.URLField(null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    post_source = models.URLField(blank=True, null=True, unique=True)
    is_approved = models.BooleanField(default=True)
    what_to_correct = models.TextField(null=True, blank=True)
    read = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.post_header


class Category(models.Model):
    category_name = models.CharField(max_length=60)
    category_icon = models.ImageField(upload_to='media',
                                      blank=True, null=True,
                                      default='media/notebook.png')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

    @property
    def slug(self):
        return self.category_name.replace(" ", "_")


class Comment(models.Model):
    user = models.ForeignKey('NSuser', null=True)
    answer_to = models.ForeignKey('Comment', null=True, blank=True)
    post = models.ForeignKey('NewsPost', null=True)
    text = models.TextField(max_length=300, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Photo(models.Model):
    photo_name = models.CharField(max_length=120, blank=True, null=True)
    image = ImageField(upload_to='media', default='')
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.photo_name)

    def thumb(self):
        return u'<img src=%s/>' % (get_thumbnail(self.image, "100x100", crop='center', quality=95).url,)
    thumb.short_description = 'Photos'
    thumb.allow_tags = True


class IsReadByUserStatus(models.Model):
    user = models.ForeignKey("NSuser")
    post = models.ForeignKey("NewsPost")
    status = models.BooleanField(default=False)

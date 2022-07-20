from django.db import models
from django.utils import timezone
from extensions.utils import jalali_convertor
#My-Manager

class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status="p")

    # def get_queryset(self):
    #     return super().get_queryset().filter(status='p')

class CategoryManager(models.Manager):
    def published(self):
        return self.filter(status=True)

#Mt-Models
class Article(models.Model):
    objects = ArticleManager()


    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-published',)

    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده '),
    )

    title = models.CharField(max_length=100, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='توضیحات')
    category = models.ManyToManyField('Category', related_name='article', verbose_name= 'دسته بندی')
    descriptions = models.TextField(verbose_name='آدرس مقاله')
    thumbnail = models.ImageField(upload_to="images", verbose_name='تصویر')
    published = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان وآخرین ویرایش')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='وضعیت انتشار')


    def __str__(self):
        return self.title

    def jalali_published(self):
        return jalali_convertor(self.published)

    jalali_published.short_description = "زمان انتشار"

    def category_published(self):
        return self.category.filter(status=True)



    def image_tag(self):
        from django.utils.html import format_html
        return format_html('<img style="border-radius :3px" src="%s" width="100" height="75" />' % (self.thumbnail.url))
    image_tag.short_description = 'عکس'



class Category(models.Model):
    parent = models.ForeignKey('self',default=None , related_name='children', null=True, blank=True,
                                on_delete=models.SET_NULL, verbose_name='زیردسته')
    title = models.CharField(max_length=100, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='توضیحات')
    status = models.BooleanField(default=True, verbose_name='آیا نشان داده شود ؟')
    position = models.IntegerField(verbose_name='پوزیشن')

    objects = CategoryManager()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ('position',)

    def __str__(self):
        return self.title





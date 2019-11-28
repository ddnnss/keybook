from django.db import models
from pytils.translit import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from customuser.models import User



class Town(models.Model):
    name = models.CharField('Город', max_length=255, blank=True, null=True)

    def __str__(self):
        return 'Город : {} '.format(self.name)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

class NewsTag(models.Model):
    name = models.CharField('Тег к новости', max_length=255, blank=True, null=True)

    def __str__(self):
        return 'Тег к новости : {} '.format(self.name)

    class Meta:
        verbose_name = "Тег к новости"
        verbose_name_plural = "Теги к новости"

class News(models.Model):
    name = models.CharField('Заголовок', max_length=255, blank=True, null=True)
    tags = models.ManyToManyField(NewsTag, verbose_name='Теги', related_name='tags')
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение превью', upload_to='blog_img/', blank=True)
    imageBig = models.ImageField('Изображение на страницу', upload_to='blog_img/', blank=True)
    short_description = models.CharField('Краткое описание (100 символов)', max_length=100, blank=False)
    description = RichTextUploadingField('Статья', blank=False, null=True)
    isShowAtIndex = models.BooleanField('Отображать на главной?', default=True)
    created_at = models.CharField('Дата', max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        self.name_lower = self.name.lower()
        super(News, self).save(*args, **kwargs)
    def __str__(self):

        return 'Новость : {} '.format(self.name)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class HouseCategory(models.Model):
    name = models.CharField('Категория помещения', max_length=255, blank=True, null=True)

    def __str__(self):
        return 'Категория помещения : {} '.format(self.name)

    class Meta:
        verbose_name = "Категория помещения"
        verbose_name_plural = "Категории помещений"







class House(models.Model):
    category = models.ForeignKey(HouseCategory, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Категория')
    client = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Клиент')
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    town = models.ForeignKey(Town, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Город')
    address = models.TextField('Адрес', blank=True)
    short_description = models.CharField('Краткое описание (100 символов)', max_length=100, blank=False, null=True)
    image = models.ImageField('Изображение превью )', upload_to='house_img/', blank=True)
    price = models.IntegerField('Цена', blank=True,null=True,default=0)
    info = models.TextField('Описание помещения', blank=True, null=True)
    isActive = models.BooleanField('Активно?', default=True)
    # filters = models.ForeignKey(HouseFilter,blank=True,null=True, on_delete=models.CASCADE,verbose_name='Фильтры')

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        self.name_lower = self.name.lower()
        super(House, self).save(*args, **kwargs)

    def __str__(self):
        return 'Помещение категории: {} , клиента {}'.format(self.category.name, self.client.email)

    class Meta:
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"


class CategoryFilter(models.Model):
    name = models.CharField('Фильтр помещения', max_length=255, blank=True, null=True)
    category = models.ForeignKey(HouseCategory, blank=True, null=True,on_delete=models.CASCADE, verbose_name='Для категории помещения')

    def __str__(self):
        return 'Фильтр категории помещения {} : {} '.format(self.category.name,self.name)

    class Meta:
        verbose_name = "Фильтр помещения"
        verbose_name_plural = "Фильтры помещений"

class HousePhotos(models.Model):
    house = models.ForeignKey(House, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Помещение')
    image = models.ImageField('Изображение)', upload_to='house_img/', blank=True)

    def __str__(self):
        return 'Изображение помещения : {} '.format(self.house.name)

    class Meta:
        verbose_name = "Изображение помещения"
        verbose_name_plural = "Изображения помещений"


class Favorite(models.Model):
    client = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Клиент')
    house = models.ForeignKey(House, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Помещение')



class Rent(models.Model):
    clientWhoRent = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Клиент',related_name='rentbyme')
    clientWhoHaveHouse = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Клиент',
                                      related_name='whohavehouse')
    house = models.ForeignKey(House, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Помещение')
    month = models.CharField('Месяц',max_length=255, blank=False, null=True)
    day = models.CharField('День',max_length=255, blank=False, null=True)

    def __str__(self):
        return 'аренда {}'.format(self.house.name)

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
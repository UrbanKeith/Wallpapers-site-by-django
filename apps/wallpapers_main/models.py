from django.db import models

class Category(models.Model):
    category_name = models.CharField('Категория', max_length = 30, unique=True)
    category_link_name = models.CharField('Название для ссылки', max_length=30, unique=True)

    def __str__(self):
        return self.category_name

class Images(models.Model):
    name = models.CharField('Имя картинки', max_length = 256, unique=True)
    categories = models.ManyToManyField(Category, blank=True)
    date = models.DateField('Дата загрузки', auto_now=True)

    # def get_last_added(amount_images):
    #     '''Возвращает последние добавленые картинки в количестве
    #      равном amount_images'''
    #     if not isinstance(amount_images, int):
    #         raise AttributeError('wrong type of amount_images')
    #     return Images.objects.order_by('-date')[:amount_images]

    def __str__(self):
        return self.name

class Source(models.Model):
    SIZES = [
    ('1280x720', 'HD'),
    ('1600x900', 'WXGA++'),
    ('1920x1080', 'Full HD'),
    ('2560×1440', 'Quad HD'),
    ]
    name = models.ForeignKey(Images, on_delete = models.CASCADE)
    size = models.CharField('Разрешение', choices=SIZES, max_length=30)
    source = models.URLField('Ссылка на источник')

    def __str__(self):
        return self.source

    # def get_last_added(size='1920x1080'):
    #     '''Возвращает последние добавленые картинки в количестве
    #      равном amount_images'''
    #     images = Images.objects.order_by('-date')
    #     return Source.objects.filter(name__in = images).filter(size=size)

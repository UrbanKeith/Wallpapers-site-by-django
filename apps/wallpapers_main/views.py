from .models import Images, Source, Category
from utils.parser import Parser

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, OperationalError
from django.core.paginator import Paginator


def load(request): #Загружает страницу для выбора способа загрузки картинок
    sizes = tuple(named_size[0] for named_size in Source.SIZES)
    return render(request, "wallpapers_main\load.html", context = {'sizes':sizes} )

def load_result(request):  #Загружает страницу вывода результатов загрузки картинок( ) и вызывает функции для загрузки картинок
    load_select = request.POST.get('load_select')
    print(load_select)
    if load_select == 'parse_site':
        result = parse_site_and_download(url = request.POST.get('url'),
                                        duration = int(request.POST.get('duration')))
    elif load_select == 'upload_file':
        result = download_file()
    else:
        result = {'Error':'Неправильный запрос на загрузку'}
    return render(request, 'wallpapers_main\\result.html', context = {'result':result})


def view_image_page(request, image_name):
    try:
        image_sources = Source.objects.filter(name__name=image_name)
    except OperationalError:
        context = {'error_message':'Картинка не найдены'}
        return render(request, 'wallpapers_main\\viewIndexImage.html', context=context)
    preview_image = image_sources.filter(size='1280x720').get()
    context = {'preview_image':preview_image, 'image_sources':image_sources, 'image_name':image_name}
    return render(request, 'wallpapers_main\\viewIndexImage.html', context=context)

def view_image(request, category='all', page=1):
    if category=='all':
        context = get_all_images(page=page)
    else:
        context = get_image_by_category(category=category, page=page)
    return render(request, 'wallpapers_main\\viewImage.html', context=context)

def sort(request):
    try:
        image = Images.objects.filter(categories=None)[:1].get()
    except DoesNotExist:
        error_message = 'Все изображения отсортированы'
        error_redirect = 'images:recommend'
        return render(request, 'wallpapers_main:error',
                     context = {'error_message':error_message,
                                'error_redirect':error_redirect})
    else:
        image = Source.objects.filter(name = image).filter(size='1280x720').get()
    categories = Category.objects.all()
    return render(request, 'wallpapers_main\sort.html',
                  context = {'image':image,
                             'categories':categories})

def category_take(request):

    source = Source.objects.filter(source = request.POST.get('source')).get()
    image = source.name
    category = Category.objects.filter(category_link_name = request.POST.get('category'))
    image.categories.set(category)
    image.save()
    return HttpResponseRedirect(reverse('wallpapers_main:sort'))

def error_redirect(request):
    return HttpResponseRedirect(reverse(request.POST.get('error_redirect')))

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_all_images(page=1):
    '''return context with all category is exist and instace of Paginator, when contains all image is exist'''
    context={}
    IMAGES_ON_PAGE = 24
    all_category = Category.objects.all()
    images = Source.objects.filter(size='1280x720')
    paginator = Paginator(images, IMAGES_ON_PAGE)
    page_obj = paginator.get_page(page)
    context.update({'all_category':all_category, 'images':page_obj, 'page_name':'Все картинки', 'current_category':'all'})
    return context


def get_image_by_category(category, page=1):
    '''return context with all category is exist and instace of Paginator, when contains all image by category'''
    context = {}
    IMAGES_ON_PAGE = 24
    all_category = Category.objects.all()
    images = Source.objects.filter(name__categories__category_link_name=category).filter(size='1280x720')
    category_name = Category.objects.filter(category_link_name=category).get()
    page_name = category_name.category_name
    paginator = Paginator(images, IMAGES_ON_PAGE)
    page_obj = paginator.get_page(page)
    context.update({'all_category':all_category, 'images':page_obj, 'page_name':page_name, 'current_category':category})
    return context


def parse_site_and_download(url, duration = 10): #Парсит сайт по url и загружает картинки со страниц от 0 до duration
    parser = Parser(url = url)
    print('Parsing...')
    images_dict = parser.parse(duration = duration)
    result = tuple()
    for image_name in images_dict:
        try:
            image = Images.objects.create(name = image_name)
        except IntegrityError:
            continue
        for image_source, image_size in images_dict[image_name].items():
            source = Source(name = image, size = image_size, source = image_source)
            source.save()
            result = result + ((image.name, source.size, source.source),)
    return result

from django.shortcuts import render
from django.http import HttpResponse
import os
from models import Picture
from django.views.decorators.csrf import csrf_exempt


def get_cover(request, catagory):
    album_cover_path_list_1_column = []
    album_cover_path_list_2_column = []
    album_cover_path_list_3_column = []
    album_cover_path_list_4_column = []

    album_object_tuple = Picture.objects.filter(image_catagory = catagory)
    for i, obj in enumerate(album_object_tuple):
        image_path_list = obj.image_path.split('/')
        relatively_image_path = '/'
        relatively_image_path = relatively_image_path.join(image_path_list[3:])
        if i % 4 == 0:
            album_cover_path_list_1_column.append((relatively_image_path, obj.image_praise, obj.image_step))
            print i,len(album_object_tuple) 
        if i % 4 == 1:
            album_cover_path_list_2_column.append((relatively_image_path, obj.image_praise, obj.image_step))
        if i % 4 == 2:
            album_cover_path_list_3_column.append((relatively_image_path, obj.image_praise, obj.image_step))
        if i % 4 == 3:
            album_cover_path_list_4_column.append((relatively_image_path, obj.image_praise, obj.image_step))

    return render(request, 'kind_template.html', {'1_column':album_cover_path_list_1_column,'2_column':album_cover_path_list_2_column,
                                                '3_column':album_cover_path_list_3_column,'4_column':album_cover_path_list_4_column,})

def error(request):
    return HttpResponse("<h1>a error</h1>")

@csrf_exempt
def praise(request):
    if request.method == 'POST':
        path = './mm_image/images/' + dict(request.POST.iterlists())['path'][0]
        print path
        praise_item = Picture.objects.filter(image_path = path)
        print praise_item
        print praise_item[0].image_praise
        tmp = praise_item[0].image_praise + 1
        praise_item.update(image_praise = tmp)
        
    return HttpResponse(tmp)

@csrf_exempt
def step(request):
    if request.method == 'POST':
        path = './mm_image/images/' + dict(request.POST.iterlists())['path'][0]
        print path
        step_item = Picture.objects.filter(image_path = path)
        print step_item
        print step_item[0].image_step
        tmp = step_item[0].image_step + 1
        step_item.update(image_step = tmp)
        
    return HttpResponse(tmp)
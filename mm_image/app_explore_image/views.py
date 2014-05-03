from django.shortcuts import render
from django.http import HttpResponse
import os
from models import Picture
from django.views.decorators.csrf import csrf_exempt


def get_cover(request, catagory):
    """
        get web page's Pictures

        args:
            request: http request
            catagory: a url argument
        return:
            a response to browser
    """
    album_cover_path_list_1_column = []
    album_cover_path_list_2_column = []
    album_cover_path_list_3_column = []
    album_cover_path_list_4_column = []

    album_object_tuple = Picture.objects.filter(image_catagory = catagory).order_by('-image_praise','image_step')
    # if catagory = 'cars':
    #     print len
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
    """
        when get a error url ,return 
    """
    return HttpResponse("<h1>a error</h1>")

@csrf_exempt
def praise(request):
    """
        when clicked the praise button, image_praise add 1
        return :
            current image_praise number
    """
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
    """
       when clicked the step button, image_step add 1
        return :
            current image_step number
    """
    if request.method == 'POST':
        path = './mm_image/images/' + dict(request.POST.iterlists())['path'][0]
        print path
        step_item = Picture.objects.filter(image_path = path)
        print step_item
        print step_item[0].image_step
        tmp = step_item[0].image_step + 1
        step_item.update(image_step = tmp)
        
    return HttpResponse(tmp)


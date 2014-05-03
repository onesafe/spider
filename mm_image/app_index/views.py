from django.shortcuts import render
from django.http import HttpResponse
from app_explore_image.models import Picture


def test(request):
    path = []
    recommend_pics = Picture.objects.all().order_by('image_praise')[:7]
    for i, pic in enumerate(recommend_pics):
        path.append((i+1,pic.image_path[11:]))
    print path
    return render(request, "index.html",{"pics_path" : path})

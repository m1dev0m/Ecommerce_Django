from django.shortcuts import render
from django.http import JsonResponse
def home(request):
    return render(request, 'main/home.html')


def some_view(request):
    data = {"message": "Hello, world!"}
    return JsonResponse(data)

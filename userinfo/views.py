import json

from django.contrib.auth.models import AbstractUser
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        password = data.get('password')
        if not name or not password:
            return JsonResponse({'error': 'Name and password are required', 'code': 500}, status=200)
        user = AbstractUser.objects.filter(username=name).first()
        if user is None:
            return JsonResponse({'error': 'User not found', 'code': 500}, status=200)
        if not user.pass_field == password:
            return JsonResponse({'error': 'Incorrect password', 'code': 500}, status=200)
        return JsonResponse(
            {'message': 'Login successful', 'data': {"id": user.id, "name": user.name, "logo": user.logo}, 'code': 200},
            status=200)
    else:
        return JsonResponse({'error': 'Only POST method allowed', 'code': 500}, status=200)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        password = data.get('password')
        print(name, password)
        if not name or not password:
            return JsonResponse({'error': 'Name and password are required', 'code': 500}, status=200)
        if AbstractUser.objects.filter(username=name).exists():
            print("User already exists")
            return JsonResponse({'error': '用户已存在', 'code': 500}, status=200)
        try:
            AbstractUser.objects.create_user(username=name, password=password)
            print("success")
            return JsonResponse({'message': 'User created successfully', 'code': 200}, status=200)
        except Exception as e:
            print("error" + str(e))
            return JsonResponse({'error': str(e), 'code': 500}, status=200)
    else:
        print("error")
        return JsonResponse({'error': 'Only POST method allowed', 'code': 500}, status=200)

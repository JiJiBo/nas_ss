import json

from django.contrib.auth.models import AbstractUser
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from utils.utils.Result import getErrorResult, getOkResult


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        password = data.get('password')
        if not name or not password:
            return getErrorResult('Name and password are required')
        user = AbstractUser.objects.filter(username=name).first()
        if user is None:
            return getErrorResult('User not found')
        if not user.pass_field == password:
            return getErrorResult('Incorrect password')
        return getOkResult({"name": user.username})
    else:
        return getErrorResult('Only POST method allowed')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        password = data.get('password')
        print(name, password)
        if not name or not password:
            return getErrorResult('Name and password are required')
        if AbstractUser.objects.filter(username=name).exists():
            print("User already exists")
            return getErrorResult('用户已存在')
        try:
            AbstractUser.objects.create_user(username=name, password=password)
            print("success")
            return getOkResult('User created successfully')
        except Exception as e:
            print("error" + str(e))
            return getErrorResult(str(e))
    else:
        print("error")
        return getErrorResult('Only POST method allowed')

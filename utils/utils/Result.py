from django.http import JsonResponse


def getErrorResult(error, code=500):
    return JsonResponse({'error': error, 'code': code, 'msg': 'error'}, status=200)


def getOkResult(data):
    return JsonResponse({"data": data, 'code': 200, 'msg': 'success'}, status=200)

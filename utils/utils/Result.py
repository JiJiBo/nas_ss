from django.http import JsonResponse


def getErrorResult(error):
    return JsonResponse({'error': error, 'code': 500, 'msg': 'error'}, status=200)


def getOkResult(data):
    return JsonResponse({"data": data, 'code': 200, 'msg': 'success'}, status=200)

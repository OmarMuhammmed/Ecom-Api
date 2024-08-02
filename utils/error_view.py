from django.http import JsonResponse

def handler404(request,exception): # error from user
    message = ('Path not found ')
    response = JsonResponse(data={'erorr':message})
    response.status_code = 404 
    return response



def handler500(request): # error from server
    message = ('Internal server Error ')
    response = JsonResponse(data={'erorr':message})
    response.status_code = 500 
    return response
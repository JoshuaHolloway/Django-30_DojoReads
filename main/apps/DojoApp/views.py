from django.shortcuts import render, HttpResponse
def index(request):
    context = {
        "name": "Noelle",
        "favorite_color": "turquoise",
        "pets": ["Bruce", "Fitz", "Georgie"]
    }
    return render(request, "DojoApp/index.html", context)
    #return HttpResponse('Hello')

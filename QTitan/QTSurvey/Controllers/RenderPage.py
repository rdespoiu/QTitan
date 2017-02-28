from django.http import HttpResponse

def renderPage(template, context, request):
    return HttpResponse(template.render(context, request))

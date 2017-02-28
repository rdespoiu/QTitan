from django.template import loader

def setTemplate(templateName):
    return loader.get_template(templateName)

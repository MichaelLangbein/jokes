from django.shortcuts import render


def startPage(req):
    return render(req, 'baseLayout/startPage.html')

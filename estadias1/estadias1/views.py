from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def registro_ventas(request):
    return render(request,'registro_venta.html')
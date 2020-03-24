from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')
def dosearch(request):
    keyword=request.GET.get('q','')
    print(keyword)
    return render(request,'result.html')
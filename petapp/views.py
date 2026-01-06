from django.shortcuts import render

# Create your views here.
def home(request): 
    return render(request, 'index.html')

def adoption_process(request): 
    return render(request, 'adoption_process.html')


from django.shortcuts import render, get_object_or_404
from .models import Category, Pet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# Create your views here.
def home(request ):
    all_categories = Category.objects.all().order_by('name')
    paginator = Paginator(all_categories, 6) 
    initial_categories = paginator.page(1)
    context = {
        'categories': initial_categories, 
    }
    return render(request, 'index.html', context)

def load_more_categories(request):
    page_number = request.GET.get('page')
    all_categories = Category.objects.all().order_by('name')
    paginator = Paginator(all_categories, 6)
    
    try:
        categories_page = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        return JsonResponse({'categories': [], 'has_next': False})

    categories_json = []
    for category in categories_page:
        categories_json.append({
            'name': category.name,
            'description': category.description,
            'image_url': category.image.url,
            'url': f'/category/{category.name}/', # Manually construct the URL
        })

    has_next = categories_page.has_next()

    return JsonResponse({
        'categories': categories_json,
        'has_next': has_next,
    })

def adoption_process(request): 
    return render(request, 'adoption_process.html')

def pet_list_view(request, category_name):

    category = get_object_or_404(Category, name__iexact=category_name)

    all_pets = Pet.objects.filter(category=category).order_by('name')

    paginator = Paginator(all_pets, 9) # 9 pets per page

    page_number = request.GET.get('page')

    try:

        page_obj = paginator.page(page_number)
    except PageNotAnInteger:

        page_obj = paginator.page(1)
    except EmptyPage:

        page_obj = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'page_obj': page_obj, # This contains the pets for the current page and pagination info
    }

    return render(request, 'pet_list.html', context)
def pet_detail_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    context = {
        'pet': pet,
    }
   
    return render(request, 'pet_detail.html', context)
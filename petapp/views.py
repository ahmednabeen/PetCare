from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Pet, AdoptionApplication, ContactMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    all_categories = list(Category.objects.all().order_by('name'))
    total = len(all_categories)
    page_size_1 = 6
    page_size_rest = 9

    page_number = int(request.GET.get('page', 1))
    if page_number < 1:
        page_number = 1

    if total <= page_size_1:
        total_pages = 1
    else:
        from math import ceil
        total_pages = 1 + ceil((total - page_size_1) / page_size_rest)

    if page_number > total_pages:
        page_number = total_pages

    if page_number == 1:
        items = all_categories[:page_size_1]
    else:
        offset = page_size_1 + (page_number - 2) * page_size_rest
        items = all_categories[offset:offset + page_size_rest]

    context = {
        'categories': items,
        'page_number': page_number,
        'total_pages': total_pages,
        'has_previous': page_number > 1,
        'has_next': page_number < total_pages,
        'prev_page': page_number - 1 if page_number > 1 else None,
        'next_page': page_number + 1 if page_number < total_pages else None,
    }
    return render(request, 'index.html', context)

def pet_list_view(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    all_pets = Pet.objects.filter(category=category)
    species_filter = request.GET.get('species')
    if species_filter:
        all_pets = all_pets.filter(species__iexact=species_filter)
    all_pets = all_pets.order_by('name')
    paginator = Paginator(all_pets, 9) 
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {
        'category': category,
        'page_obj': page_obj, 
        'current_species': species_filter,
    }
    return render(request, 'pet_list.html', context)

def pet_detail_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    context = {
        'pet': pet,
    }
    return render(request, 'pet_detail.html', context)

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def adoption_process(request):
    if request.method == "POST":
        AdoptionApplication.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            pet_name=request.POST.get("pet_name"),
            message=request.POST.get("message"),
        )
        return redirect("adoption_process") 

    pet_name = request.GET.get("pet", "")
    return render(request, "adoption_process.html", {"preset_pet": pet_name})

def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )
        return redirect("contact")

    return render(request, "contact.html")

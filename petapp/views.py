from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
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
    submitted = False
    if request.method == "POST":
        app = AdoptionApplication.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            pet_name=request.POST.get("pet_name"),
            message=request.POST.get("message"),
        )
        send_mail(
            subject=f"New Adoption Application from {app.name}",
            message=(
                f"Name: {app.name}\n"
                f"Email: {app.email}\n"
                f"Phone: {app.phone}\n"
                f"Address: {app.address}\n"
                f"Pet: {app.pet_name}\n"
                f"Message: {app.message}\n\n"
                f"Login to admin panel to respond: {request.build_absolute_uri('/admin/')}"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )
        submitted = True

    pet_name = request.GET.get("pet", "")
    return render(request, "adoption_process.html", {
        "preset_pet": pet_name,
        "submitted": submitted,
    })

def contact(request):
    if request.method == "POST":
        msg = ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )
        send_mail(
            subject=f"New Contact Message from {msg.name}: {msg.subject}",
            message=(
                f"Name: {msg.name}\n"
                f"Email: {msg.email}\n"
                f"Subject: {msg.subject}\n"
                f"Message: {msg.message}\n\n"
                f"Login to admin panel to respond: {request.build_absolute_uri('/admin/')}"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )
        return redirect("contact")

    return render(request, "contact.html")

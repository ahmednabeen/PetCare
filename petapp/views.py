from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Category, Pet, AdoptionApplication, ContactMessage, BlogPost, Testimonial
from .forms import ContactForm, AdoptionForm, SearchForm

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

    testimonials = Testimonial.objects.filter(featured=True)[:3]
    blog_posts = BlogPost.objects.filter(published=True)[:3]

    context = {
        'categories': items,
        'page_number': page_number,
        'total_pages': total_pages,
        'has_previous': page_number > 1,
        'has_next': page_number < total_pages,
        'prev_page': page_number - 1 if page_number > 1 else None,
        'next_page': page_number + 1 if page_number < total_pages else None,
        'home_testimonials': testimonials,
        'home_blog_posts': blog_posts,
    }
    return render(request, 'index.html', context)

def pet_list_view(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    all_pets = Pet.objects.filter(category=category).select_related('category')
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
    species_list = Pet.objects.filter(category=category).values_list('species', flat=True).distinct().order_by('species')
    context = {
        'category': category,
        'page_obj': page_obj,
        'current_species': species_filter,
        'species_list': species_list,
    }
    return render(request, 'pet_list.html', context)

def pet_detail_view(request, pet_id):
    pet = get_object_or_404(Pet.objects.select_related('category'), id=pet_id)
    additional_images = pet.additional_images.all()
    context = {
        'pet': pet,
        'additional_images': additional_images,
    }
    return render(request, 'pet_detail.html', context)

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def adoption_process(request):
    form = AdoptionForm(request.POST or None)
    submitted = False

    if request.method == "POST" and form.is_valid():
        cd = form.cleaned_data
        app = AdoptionApplication.objects.create(
            name=cd["name"],
            email=cd["email"],
            phone=cd["phone"],
            address=cd["address"],
            pet_name=cd["pet_name"],
            message=cd["message"],
            user=request.user if request.user.is_authenticated else None,
        )
        try:
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
            send_mail(
                subject="We received your adoption application – PetCare",
                message=(
                    f"Dear {app.name},\n\n"
                    f"Thank you for your interest in adopting a pet. We have received your application "
                    f"and our team will review it shortly.\n\n"
                    f"Here is a summary of your application:\n"
                    f"Pet interested in: {app.pet_name or 'Not specified'}\n\n"
                    f"We typically respond within 2-3 business days.\n\n"
                    f"Best regards,\nThe PetCare Team"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[app.email],
                fail_silently=True,
            )
        except Exception:
            pass
        submitted = True

    pet_name = request.GET.get("pet", "")
    return render(request, "adoption_process.html", {
        "preset_pet": pet_name,
        "submitted": submitted,
        "form": form,
    })

def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        cd = form.cleaned_data
        ContactMessage.objects.create(
            name=cd["name"],
            email=cd["email"],
            subject=cd["subject"],
            message=cd["message"],
        )
        try:
            send_mail(
                subject=f"New Contact Message from {cd['name']}: {cd['subject']}",
                message=(
                    f"Name: {cd['name']}\n"
                    f"Email: {cd['email']}\n"
                    f"Subject: {cd['subject']}\n"
                    f"Message: {cd['message']}\n\n"
                    f"Login to admin panel to respond: {request.build_absolute_uri('/admin/')}"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        messages.success(request, "Your message has been sent. We'll get back to you soon!")
        return redirect("contact")

    return render(request, "contact.html", {"form": form})

def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'blog_list.html', {'page_obj': page_obj})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    recent = BlogPost.objects.filter(published=True).exclude(id=post.id)[:3]
    return render(request, 'blog_detail.html', {'post': post, 'recent_posts': recent})

def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'testimonial_list.html', {'testimonials': testimonials})

def search(request):
    form = SearchForm(request.GET)
    query = ""
    results = []
    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        if query:
            results = Pet.objects.filter(
                Q(name__icontains=query) |
                Q(species__icontains=query) |
                Q(origin__icontains=query)
            ).select_related('category')
    return render(request, 'search_results.html', {
        'form': form,
        'query': query,
        'results': results,
    })

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

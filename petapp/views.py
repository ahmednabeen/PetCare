from django.shortcuts import render

# Create your views here.
def home(request): 
    return render(request, 'index.html')

def adoption_process(request): 
    return render(request, 'adoption_process.html')

def pet_list_view(request, category_name):
    """
    This view handles displaying all pets for a specific category with pagination.
    """
    # 1. Get the Category object based on the name from the URL.
    #    get_object_or_404 is a shortcut: it gets the object or returns a 404 error
    #    if the category doesn't exist. This prevents errors.
    category = get_object_or_404(Category, name__iexact=category_name)
    
    # 2. Filter the pets.
    #    This is the power of the ForeignKey! We get all 'Pet' objects
    #    where the 'category' field is the category we just found.
    all_pets = Pet.objects.filter(category=category).order_by('name')

    # 3. Set up Pagination.
    #    We create a Paginator object with our list of pets and specify
    #    that we want 9 pets per page.
    paginator = Paginator(all_pets, 9) # 9 pets per page
    
    # Get the page number from the URL's query parameters (e.g., ?page=2)
    page_number = request.GET.get('page')
    
    try:
        # Get the specific page object from the paginator
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If the page parameter is not a number, show the first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., page 99), show the last page.
        page_obj = paginator.page(paginator.num_pages)

    # 4. Prepare the context and render the template.
    #    We pass the category and the page object to the template.
    context = {
        'category': category,
        'page_obj': page_obj, # This contains the pets for the current page and pagination info
    }
    
    return render(request, 'pet_list.html', context)
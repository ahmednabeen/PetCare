from django.db import migrations


DEFAULT_SETTINGS = {
    # Home page
    'hero_title': 'Find Your Perfect Pet Companion',
    'hero_subtitle': 'Adopt loving pets and give them a forever home',
    'home_categories_heading': 'Pet Categories',
    'home_testimonials_heading': 'What Our Adopters Say',
    'home_testimonials_btn_text': 'View All Testimonials',
    'home_working_steps_heading': 'Working Procedure',
    'home_blog_heading': 'Latest from Our Blog',
    'home_blog_btn_text': 'View All Posts',
    'home_adoption_btn_text': 'Click Here',
    # About
    'about_heading': 'About PetCare',
    'about_intro': 'PetCare is a trusted pet adoption platform connecting loving pets with forever homes.',
    # Services
    'services_heading': 'Our Services',
    'services_intro': 'We offer a range of services for your pets.',
    # Contact
    'contact_heading': 'Contact Us',
    'contact_get_in_touch': 'Get in Touch',
    'contact_form_heading': 'Send Us a Message',
    'contact_send_btn': 'Send Message',
    'contact_address': 'Dhaka, Bangladesh',
    'contact_email': 'support@petcare.com',
    'contact_phone': '+880 1234 567890',
    # Adoption
    'adoption_process_heading': 'Adoption Process',
    'adoption_process_subheading': 'Adopt Your Perfect Pet',
    'adoption_process_text': 'Follow the steps below to give a pet a loving forever home.',
    'adoption_process_how_it_works': 'How It Works',
    'adoption_contact_admin_heading': 'Contact the Admin',
    'adoption_form_heading': 'Adoption Application Form',
    'adoption_submit_btn': 'Submit Application',
    'admin_email': 'admin@petcare.com',
    'admin_phone': '+880 1234 567890',
    # Blog
    'blog_heading': 'PetCare Blog',
    'blog_tagline': 'Tips, stories, and guides for pet lovers',
    # Testimonials
    'testimonials_heading': 'What Our Adopters Say',
    'testimonials_tagline': 'Real stories from real families who found their perfect pet',
    # Search
    'search_heading': 'Search Results',
    'search_btn_text': 'Search',
    # Pet list / detail
    'filter_by_species_text': 'Filter by species:',
    'filter_all_text': 'All',
    'details_btn_text': 'Details',
    'read_more_text': 'Read More',
    'pagination_prev_text': 'Previous',
    'pagination_next_text': 'Next',
    'available_text': 'Available for Adoption',
    'adopted_text': 'Already Adopted',
    # Pet detail table labels
    'label_category': 'Category',
    'label_species': 'Species',
    'label_lifespan': 'Average lifespan',
    'label_origin': 'Origin',
    'label_height': 'Height',
    'label_weight': 'Weight',
    'label_habits': 'Habits',
    'label_diet': 'Diet',
    'label_vaccination': 'Vaccination',
    'label_availability': 'Availability',
    'adopt_btn_text': 'Adopt',
    # Footer
    'footer_about': 'Your trusted platform for pet adoption. Giving pets a loving forever home.',
    'footer_heading_quick_links': 'Quick Links',
    'footer_heading_contact': 'Contact',
    'footer_heading_follow_us': 'Follow Us',
    'footer_text': '© 2026 PetCare. All rights reserved.',
    # Errors
    'error_404_heading': 'Page Not Found',
    'error_404_text': 'Sorry, the page you\'re looking for doesn\'t exist or has been moved.',
    'error_500_heading': 'Server Error',
    'error_500_text': 'Something went wrong on our end. Please try again later.',
    'error_back_btn': 'Back to Home',
    # Misc
    'skip_to_main': 'Skip to main content',
    'toggle_menu': 'Toggle menu',
    'search_placeholder': 'Search pets by name, species, or origin...',
    'back_to_top': 'Back to top',
    'breadcrumb_home': 'Home',
    # Step titles for adoption process
    'step_1_title': 'Browse our available pets and find your match',
    'step_2_title': 'Fill out the adoption application form below',
    'step_3_title': 'Our team reviews your application and contacts you',
    'step_4_title': 'Meet the pet and complete the adoption',
}

DEFAULT_NAV_LINKS = [
    {'placement': 'navbar', 'title': 'About Us', 'url_name': 'about', 'order': 10},
    {'placement': 'navbar', 'title': 'Contact Us', 'url_name': 'contact', 'order': 20},
    {'placement': 'navbar', 'title': 'Services', 'url_name': 'services', 'order': 30},
    {'placement': 'navbar', 'title': 'Blog', 'url_name': 'blog_list', 'order': 40},
    {'placement': 'footer', 'title': 'About Us', 'url_name': 'about', 'order': 10},
    {'placement': 'footer', 'title': 'Services', 'url_name': 'services', 'order': 20},
    {'placement': 'footer', 'title': 'Contact', 'url_name': 'contact', 'order': 30},
    {'placement': 'footer', 'title': 'Adoption', 'url_name': 'adoption_process', 'order': 40},
    {'placement': 'footer', 'title': 'Blog', 'url_name': 'blog_list', 'order': 50},
]

DEFAULT_SOCIAL_LINKS = [
    {'platform': 'Facebook', 'url': '#', 'order': 10},
    {'platform': 'Twitter', 'url': '#', 'order': 20},
    {'platform': 'Instagram', 'url': '#', 'order': 30},
]


def add_default_data(apps, schema_editor):
    SiteSetting = apps.get_model('petapp', 'SiteSetting')
    NavigationLink = apps.get_model('petapp', 'NavigationLink')
    SocialLink = apps.get_model('petapp', 'SocialLink')

    for key, value in DEFAULT_SETTINGS.items():
        SiteSetting.objects.get_or_create(key=key, defaults={'value': value})

    for link in DEFAULT_NAV_LINKS:
        NavigationLink.objects.get_or_create(
            placement=link['placement'],
            title=link['title'],
            defaults=link,
        )

    for link in DEFAULT_SOCIAL_LINKS:
        SocialLink.objects.get_or_create(
            platform=link['platform'],
            defaults=link,
        )


def remove_default_data(apps, schema_editor):
    SiteSetting = apps.get_model('petapp', 'SiteSetting')
    NavigationLink = apps.get_model('petapp', 'NavigationLink')
    SocialLink = apps.get_model('petapp', 'SocialLink')

    SiteSetting.objects.filter(key__in=DEFAULT_SETTINGS.keys()).delete()

    for link in DEFAULT_NAV_LINKS:
        NavigationLink.objects.filter(
            placement=link['placement'],
            title=link['title'],
        ).delete()

    for link in DEFAULT_SOCIAL_LINKS:
        SocialLink.objects.filter(platform=link['platform']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('petapp', '0010_sociallink_navigationlink'),
    ]
    operations = [
        migrations.RunPython(add_default_data, remove_default_data),
    ]

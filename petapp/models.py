from django.db import models
from django.contrib.auth.models import User

class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.key

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Emoji or icon text", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class WorkingStep(models.Model):
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.number}. {self.title}"

class AboutFeature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Emoji or icon text", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "About Feature"
        verbose_name_plural = "About Features"

    def __str__(self):
        return self.title

class WhyChooseUsItem(models.Model):
    text = models.CharField(max_length=300)
    icon = models.CharField(max_length=50, help_text="Emoji or icon text", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Why Choose Us Item"

    def __str__(self):
        return self.text

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', help_text="Image for the category card")
    description = models.TextField(help_text="A short article about this category.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Pet(models.Model):
    pet_id = models.CharField(max_length=20, editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pet_images/', help_text="Image of the pet")
    is_available = models.BooleanField(default=True, help_text="Is this pet available for adoption?")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="pets")
    species = models.CharField(max_length=100, help_text="e.g., Golden Retriever, Siamese", db_index=True)
    average_lifespan = models.PositiveIntegerField(help_text="Age in years")
    origin = models.CharField(max_length=100, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm", blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg", blank=True, null=True)
    habitual_status = models.TextField(blank=True, help_text="Describe the pet's habits")
    foods = models.TextField(blank=True, help_text="Describe the pet's diet")
    vaccination = models.TextField(blank=True, help_text="Vaccination status and history")
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['is_available']),
            models.Index(fields=['category', 'is_available']),
        ]

    def save(self, *args, **kwargs):
        if not self.pet_id:
            last = Pet.objects.all().order_by('id').last()
            if last and last.pet_id:
                num = int(last.pet_id.split('-')[1]) + 1
            else:
                num = 1
            self.pet_id = f"PET-{num:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.species})"

class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='pet_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Pet Image"
        verbose_name_plural = "Pet Additional Images"

    def __str__(self):
        return f"{self.pet.name} image {self.order}"

class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    pet_name = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_reply = models.TextField(blank=True)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.name} - {self.pet_name or 'General'}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    admin_reply = models.TextField(blank=True)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.name}: {self.subject or 'No subject'}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="Short summary for cards")
    image = models.ImageField(upload_to='blog/', blank=True)
    author = models.CharField(max_length=100, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    pet_name = models.CharField(max_length=100, blank=True, help_text="Adopted pet name")
    content = models.TextField(help_text="Testimonial text")
    image = models.ImageField(upload_to='testimonials/', blank=True, help_text="Photo of the person or pet")
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.pet_name or 'General'}"



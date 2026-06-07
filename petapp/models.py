from django.db import models

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
    """Represents a category of pets, e.g., Dogs, Cats."""
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', help_text="Image for the category card")
    description = models.TextField(help_text="A short article about this category.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Pet(models.Model):
    """Represents an individual pet available for adoption."""
    # --- Core Information ---
    pet_id = models.CharField(max_length=20, editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pet_images/', help_text="Image of the pet")
    is_available = models.BooleanField(default=True, help_text="Is this pet available for adoption?")
    # --- Relationship to Category ---
    # This is the crucial link. Each pet belongs to one category.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="pets")
    # --- Details for the list page ---
    species = models.CharField(max_length=100, help_text="e.g., Golden Retriever, Siamese")
    average_lifespan = models.PositiveIntegerField(help_text="Age in years")
    # --- Details for the single pet page ---
    origin = models.CharField(max_length=100, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm", blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg", blank=True, null=True)
    habitual_status = models.TextField(blank=True, help_text="Describe the pet's habits")
    foods = models.TextField(blank=True, help_text="Describe the pet's diet")
    vaccination = models.TextField(blank=True, help_text="Vaccination status and history")

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



class AdoptionApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    pet_name = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    admin_reply = models.TextField(blank=True)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    admin_reply = models.TextField(blank=True)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


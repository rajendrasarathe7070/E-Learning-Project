from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse 

class Branch(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code}"

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('super_student', 'Super Student'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.PositiveSmallIntegerField(null=True, blank=True)
    college = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True)

    def __str__(self):
        return self.username

class Note(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)

    subject = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_index=True)
    semester = models.PositiveSmallIntegerField(db_index=True)
    unit = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='notes/', null=True, blank=True)
    pdf_link = models.URLField(blank=True)
    cover_link = models.URLField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    uploaded_at = models.DateField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
     
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) # Title ko URL-friendly banata hai
        super().save(*args, **kwargs)

    def clean(self):
        if not self.pdf_file and not self.pdf_link:
            raise ValidationError("Either PDF file or PDF link is required.")

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_index=True)
    semester = models.PositiveSmallIntegerField(db_index=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    cover_gradient = models.CharField(max_length=100, default='linear-gradient(135deg,#6c63ff,#00d4ff)')
    description = models.TextField()
    pdf_file = models.FileField(upload_to='books/', null=True, blank=True)
    pdf_link = models.URLField(blank=True)
    cover_link = models.URLField(blank=True)

 # स्लग बनाने के लिए ज़रूरी है

class PYQ(models.Model):
    EXAM_TYPES = [
        ('F', 'F-Series'),
        ('mid', 'Mid-Sem'),
        ('end', 'End-Sem'),
        ('S', 'S-Series'),
    ]
    
    subject = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_index=True)
    semester = models.PositiveSmallIntegerField(db_index=True)
    year = models.PositiveSmallIntegerField()
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES)
    pdf_file = models.FileField(upload_to='pyqs/', null=True, blank=True)
    pdf_link = models.URLField(blank=True)
    
    # 1. max_length को बढ़ाकर 250 कर दिया है
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    def __str__(self):
        # self.subject_name को बदलकर self.subject किया गया है
        return f"{self.subject} ({self.year})"

    def save(self, *args, **kwargs):
        if not self.slug:
            # यहाँ भी self.subject का उपयोग किया गया है
            title_string = f"{self.subject} {self.exam_type} {self.year}"
            original_slug = slugify(title_string)
            
            # डुप्लिकेट स्लग से बचने का लॉजिक
            queryset = PYQ.objects.all().filter(slug__iexact=original_slug).count()
            count = 1
            slug = original_slug
            while(queryset):
                slug = f"{original_slug}-{count}"
                count += 1
                queryset = PYQ.objects.all().filter(slug__iexact=slug).count()
            
            self.slug = slug
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pyq_detail', kwargs={'slug': self.slug})


class Syllabus(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_index=True)
    semester = models.PositiveSmallIntegerField(db_index=True)
    units = models.JSONField(default=list)   # e.g. [{"n":1,"topic":"..."}, ...]
    pdf_file = models.FileField(upload_to='syllabi/', null=True, blank=True)
    pdf_link = models.URLField(blank=True)

class Doubt(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doubts')
    asked_at = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def delete_if_expired(self):
        """Auto-delete: 7 days unsolved, 2 days solved"""
        now = timezone.now()
        if self.is_solved:
            expiry = self.asked_at + timezone.timedelta(days=2)
        else:
            expiry = self.asked_at + timezone.timedelta(days=7)
        if now >= expiry:
            self.delete()
            return True
        return False

class Reply(models.Model):
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    is_best = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'note')
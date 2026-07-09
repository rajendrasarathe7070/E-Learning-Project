from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Note, User , Branch, Book, PYQ, Syllabus, Doubt, Reply, Bookmark
from core.models import User, Branch, Note, Book, PYQ, Syllabus, Doubt, Reply, Bookmark
# Try to unregister first if already registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'branch', 'semester', 'role', 'is_staff')
    list_filter = ('branch', 'semester', 'role', 'is_staff')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('branch', 'semester', 'college', 'role', 'bio', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Fields', {'fields': ('branch', 'semester', 'college', 'role')}),
    )

admin.site.register(User, CustomUserAdmin)

admin.site.register(Branch)
admin.site.register(Note)
admin.site.register(Book)
admin.site.register(PYQ)
admin.site.register(Syllabus)
admin.site.register(Doubt)
admin.site.register(Reply)
admin.site.register(Bookmark)
admin.site.site_header = " E-leran Admin - Rajendra sarathe"
admin.site.site_title = " E-leran Admin - Rajendra sarathe" 


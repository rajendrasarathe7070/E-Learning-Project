from django.urls import path
# urls.py
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page  # Cache के लिए
from minor.sitemaps import StaticSitemap, DynamicFilterSitemap, DetailSitemap

from .views import (
    health_check,
    notes_list,
    upload_note,
    download_note,
    toggle_bookmark,
    delete_note,
    books_list,
    upload_book,
    pyqs_list,
    upload_pyq,
    syllabus_list,
    syllabus_detail_by_slug,
    upload_syllabus,
    doubts_list,
    ask_doubt,
    reply_to_doubt,
    mark_best_reply,
    profile_data,
    update_profile,
    my_uploads,
    saved_notes,
    
)

app_name = 'api'




urlpatterns = [
    # NOTE: Frontend expects these exact routes:
    #   /api/notes/      -> notes_list
    #   /api/doubts/     -> doubts_list
    #   /api/profile/    -> profile_data
    # These are kept explicitly to avoid accidental prefix/mount issues.
    path('health/', health_check, name='health_check'),
   
    


    # Notes
    path('notes/', notes_list, name='notes_list'),
    path('notes/upload/', upload_note, name='upload_note'),
    path('notes/<int:note_id>/download/', download_note, name='download_note'),
    path('notes/<int:note_id>/bookmark/', toggle_bookmark, name='toggle_bookmark'),
    path('notes/<int:note_id>/delete/', delete_note, name='delete_note'),

    # Books
    path('books/', books_list, name='books_list'),
    path('books/upload/', upload_book, name='upload_book'),

    # PYQ
    path('pyqs/', pyqs_list, name='pyqs_list'),
    path('pyqs/upload/', upload_pyq, name='upload_pyq'),

    # Syllabus
    path('syllabus/', syllabus_list, name='syllabus_list'),
    path('syllabus/<slug:slug>/', syllabus_detail_by_slug, name='syllabus_detail'),
    path('syllabus/upload/', upload_syllabus, name='upload_syllabus'),

    # Doubts + Replies
    path('doubts/', doubts_list, name='doubts_list'),
    path('doubts/ask/', ask_doubt, name='ask_doubt'),
    path('doubts/<int:doubt_id>/reply/', reply_to_doubt, name='reply_to_doubt'),
    path('replies/<int:reply_id>/mark_best/', mark_best_reply, name='mark_best_reply'),

    # Profile
    path('profile/', profile_data, name='profile_data'),
    path('profile/update/', update_profile, name='update_profile'),
    path('user/uploads/', my_uploads, name='my_uploads'),
    path('user/saved/', saved_notes, name='saved_notes'),
]



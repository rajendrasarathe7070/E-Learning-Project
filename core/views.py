from django.shortcuts import render


def search_page(request):
    # Search page uses JS to fetch results using ?q= from the URL.
    # This view only serves the template.
    return render(request, 'search.html')


def note_detail(request, slug):
    note = get_object_or_404(Note, slug=slug)
    return render(request, 'note_detail.html', {'note': note})

def pyq_detail(request, slug):
    # Your view logic goes here
    pass

from django.shortcuts import render


def search_page(request):
    # Search page uses JS to fetch results using ?q= from the URL.
    # This view only serves the template.
    return render(request, 'search.html')



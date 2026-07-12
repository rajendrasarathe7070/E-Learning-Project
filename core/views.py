from django.shortcuts import render
from django.db.models import Q
from core.models import PYQ  # अपने PYQ मॉडल को इम्पोर्ट करें

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


def pyq_page(request):
    # सर्च बार से आने वाले शब्द को पकड़ें
    query = request.GET.get('q', '').strip()
    
    # शुरुआत में सभी पेपर्स लोड करें
    pyqs = PYQ.objects.all()
    
    # अगर यूज़र ने कुछ सर्च किया है, तो फ़िल्टर करें
    if query:
        pyqs = pyqs.filter(
            Q(subject__icontains=query) | 
            Q(exam_type__icontains=query) |
            Q(year__icontains=query)
        ).distinct()
        
    context = {
        'pyqs': pyqs,
        'query': query,  # इसे वापस भेज रहे हैं ताकि सर्च बार में टाइप किया हुआ शब्द गायब न हो
    }
    return render(request, 'pyq.html', context)

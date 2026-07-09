from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from core.forms import UserCreationForm


@csrf_protect
def register_view(request):
    """Register using core.forms.UserCreationForm."""
    if request.method == 'POST':
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.role = 'student'
                user.branch = form.cleaned_data.get('branch')
                user.semester = form.cleaned_data.get('semester')
                user.college = form.cleaned_data.get('college', '')
                user.save()

                messages.success(request, '✅ Registration successful! Logging you in...')
                login(request, user)
                return redirect('/')
            else:
                # Form has validation errors, re-render with errors
                return render(request, 'registration/register.html', {'form': form})
        except Exception as e:
            messages.error(request, f'❌ Registration failed: {str(e)}')
            form = UserCreationForm()
            return render(request, 'registration/register.html', {'form': form, 'error': str(e)})
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User, Branch

class UserCreationForm(BaseUserCreationForm):
    branch = forms.CharField(max_length=10, required=False)
    semester = forms.IntegerField(min_value=1, max_value=8, required=False)
    college = forms.CharField(max_length=100, required=False)

    class Meta(BaseUserCreationForm.Meta):
        model = User   # important – custom User model
        fields = ('username', 'email', 'password1', 'password2', 'branch', 'semester', 'college')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make branch and semester optional in form
        self.fields['branch'].required = False
        self.fields['semester'].required = False
        self.fields['college'].required = False

    def clean_branch(self):
        branch_code = self.cleaned_data.get('branch')
        if branch_code and branch_code.strip():
            try:
                branch_obj = Branch.objects.get(code=branch_code)
                return branch_obj
            except Branch.DoesNotExist:
                raise forms.ValidationError(f"Branch '{branch_code}' not found. Available branches: CSE, ME, CE, EE")
        return None

    def clean_semester(self):
        semester = self.cleaned_data.get('semester')
        if semester and (semester < 1 or semester > 8):
            raise forms.ValidationError("Semester must be between 1 and 8")
        return semester
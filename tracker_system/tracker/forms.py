from django import forms
from django.core.validators import FileExtensionValidator
from .models import Car, Tracker, InstallationHistory, OrderDocument

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'board_number',  # Бортовой номер
            'state_number',  # Державний номер
            'model',
            'location',
            'comment',
            'is_active',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If Location model exists, use it as queryset
        try:
            from .models import Location
            self.fields['location'].queryset = Location.objects.all()
        except Exception:
            pass

class TrackerForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = [
            'imei', 'serial_number', 'inventory_number_tracker',
            'inventory_number_antenna', 'model', 'protocol',
            'holder_number', 'sim_old', 'n_card', 'sim_new',
            'comment', 'is_active'
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class InstallationForm(forms.ModelForm):
    class Meta:
        model = InstallationHistory
        fields = [
            'car', 'tracker', 'installation_date',
            'removal_date', 'is_active', 'comment'
        ]
        widgets = {
            # Date inputs must be rendered in ISO format (YYYY-MM-DD) for HTML5 date inputs
            'installation_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'removal_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        installation_date = cleaned_data.get('installation_date')
        removal_date = cleaned_data.get('removal_date')
        is_active = cleaned_data.get('is_active')
        
        if removal_date and installation_date and removal_date < installation_date:
            raise forms.ValidationError(
                "Дата снятия не может быть раньше даты установки"
            )
        
        if is_active and removal_date:
            raise forms.ValidationError(
                "Активная установка не может иметь дату снятия"
            )
        
        return cleaned_data

class OrderDocumentForm(forms.ModelForm):
    class Meta:
        model = OrderDocument
        fields = [
            'car', 'document', 'document_type',
            'document_number', 'issue_date', 'comment'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
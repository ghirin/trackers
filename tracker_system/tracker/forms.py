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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If Location model exists, use it as queryset
        try:
            from .models import Location
            self.fields['location'].queryset = Location.objects.all()
        except Exception:
            pass

        # Add an optional current_car field to allow assigning current installation from tracker form
        try:
            from .models import Car
            self.fields['current_car'] = forms.ModelChoiceField(
                queryset=Car.objects.all(),
                required=False,
                label='Автомобиль',
                help_text='Выберите автомобиль, на который назначить этот трекер (создаст запись установки)'
            )
            if self.instance and getattr(self.instance, 'pk', None):
                active = self.instance.installations.filter(is_active=True).select_related('car').first()
                if active:
                    self.fields['current_car'].initial = active.car

            # Place current_car after 'holder_number' in the field order for nicer layout
            try:
                from collections import OrderedDict
                current = self.fields.pop('current_car')
                new_fields = OrderedDict()
                inserted = False
                for name, field in list(self.fields.items()):
                    new_fields[name] = field
                    if name == 'holder_number':
                        new_fields['current_car'] = current
                        inserted = True
                if not inserted:
                    new_fields['current_car'] = current
                self.fields = new_fields
            except Exception:
                # if for some reason ordering fails, keep the field where it was
                self.fields['current_car'] = current
        except Exception:
            pass

class InstallationForm(forms.ModelForm):
    class Meta:
        model = InstallationHistory
        fields = [
            'car', 'tracker', 'installation_date',
            'removal_date', 'is_active', 'order_document', 'comment'
        ]
        widgets = {
            # Date inputs must be rendered in ISO format (YYYY-MM-DD) for HTML5 date inputs
            'installation_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'removal_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure order_document is required at form level (DB allows null for migration safety)
        if 'order_document' in self.fields:
            self.fields['order_document'].required = True
            self.fields['order_document'].help_text = 'Выберите приказ (создайте его в админке, если ещё нет)'

    def clean(self):
        cleaned_data = super().clean()
        installation_date = cleaned_data.get('installation_date')
        removal_date = cleaned_data.get('removal_date')
        is_active = cleaned_data.get('is_active')
        order_document = cleaned_data.get('order_document')
        
        if removal_date and installation_date and removal_date < installation_date:
            raise forms.ValidationError(
                "Дата снятия не может быть раньше даты установки"
            )
        
        if is_active and removal_date:
            raise forms.ValidationError(
                "Активная установка не может иметь дату снятия"
            )

        if not order_document:
            raise forms.ValidationError('Поле "Приказ" обязательно.')
        
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
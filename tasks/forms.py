
#- Para crear un formulario a partir de un modelo.
from django import forms
from .models import Task



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Escribe el titulo de la tarea'}),

            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Describe la tarea'}),

            'important': forms.CheckboxInput(attrs={'class': 'form-check-input mb-3 text-primary'}),
        }

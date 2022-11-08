from django import forms
from .models import AcceptanceDocs
import datetime

class SupplierForm(forms.ModelForm):
    #date_time = forms.DateTimeField(initial=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doc_date'].required = True
        self.fields['supplier'].required = True
    
    class Meta:
        model = AcceptanceDocs
        fields = [ 'doc_date', 'supplier' ]
        widgets = {
            'doc_date': forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'type': 'datetime-local'})
        }
        labels = { 'doc_date': 'Дата', 'supplier': 'Контрагент' }
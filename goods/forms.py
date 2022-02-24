from django import forms
from .models import Good, Barcode


class GoodForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = True
    
    class Meta:
        model = Good
        fields = ['name', 'price', 'Group', 'Author', 'Genre', 'published_house']
        
        labels = {
            "name": "Наименование товара",
            "price": "Цена розничная",
            "Group": "Группа",
            "Author": "Автор",
            "Genre": "Жанр",
            "published_house": "Издательство",
        }

class BarcodeForm(forms.ModelForm):
    
    class Meta:
        model = Barcode
        fields = '__all__'
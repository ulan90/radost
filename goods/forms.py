from django import forms
from .models import Good


class GoodForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = True
    
    class Meta:
        model = Good
        fields = '__all__'
        
        labels = {
            "name": "Наименование товара",
            "price": "Цена розничная",
            "Group": "Группа",
            "Author": "Автор",
            "published_house": "Издательство",
            "Genre": "Жанр",
        }
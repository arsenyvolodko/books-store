from django import forms
from .models import CategoryHierarchy, Category


class CategoryHierarchyForm(forms.ModelForm):
    class Meta:
        model = CategoryHierarchy
        fields = '__all__'

    def check_cycle(self, parent, child):

        if parent == child:
            raise forms.ValidationError(
                f"Cannot add subcategory due to circular dependency!")

        children = Category.objects.filter(children__parent=child).all()
        for ch in children:
            self.check_cycle(parent, ch)

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get("parent")
        child = cleaned_data.get("child")

        if parent == child:
            raise forms.ValidationError(f'Same category cannot be parent and child at the same time')

        if CategoryHierarchy.objects.filter(child__exact=child):
            raise forms.ValidationError(
                f"Category '{parent}' can't be a parent of '{child}' category because '{child}' is already a subcategory for another category.")

        self.check_cycle(parent, child)
        return cleaned_data

from django import forms

from ehms.articles.models import Article


class ArticleCountryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '1', 'data-validation': 'required', })
        self.fields['published'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '2', })
        self.fields['excerpt'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '3', 'data-validation': 'required', })
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '4', 'data-validation': 'required', })
        self.fields['type'].widget.attrs.update(
            {'class': 'form-select', 'autocomplete': 'off', 'tabindex': '5',
             'data-validation': 'required|within:Article Sticky Big:Article Sticky Aside:Article Other', })
        self.fields['category'].widget.attrs.update(
            {'class': 'form-select', 'autocomplete': 'off', 'tabindex': '6', 'data-validation': 'required', })
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '7',
             'data-validation': 'file:jpg,jpeg:2:MB', })
        self.fields['region'].widget.attrs.update(
            {'class': 'form-select', 'autocomplete': 'off', 'tabindex': '8', 'data-validation': 'required', })

    class Meta:
        model = Article
        fields = ['title', 'published', 'excerpt', 'content', 'type', 'image', 'category', 'region', ]


class ArticleRegionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '1', 'data-validation': 'required', })
        self.fields['published'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '2', })
        self.fields['excerpt'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '3', 'data-validation': 'required', })
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '4', 'data-validation': 'required', })
        self.fields['type'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '5',
             'data-validation': 'required|within:Article Sticky Big:Article Sticky Aside:Article Other', })
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '6', 'data-validation': 'required', })
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '7',
             'data-validation': 'file:jpg,jpeg:2:MB', })
        self.fields['region'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '8', 'data-validation': 'required', })

    class Meta:
        model = Article
        fields = ['title', 'published', 'excerpt', 'content', 'type', 'image', 'category', 'district', ]


class ArticleDistrictForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '1', 'data-validation': 'required', })
        self.fields['published'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '2', })
        self.fields['excerpt'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '3', 'data-validation': 'required', })
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '4', 'data-validation': 'required', })
        self.fields['type'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '5',
             'data-validation': 'required|within:Article Sticky Big:Article Sticky Aside:Article Other', })
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '6', 'data-validation': 'required', })
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '7',
             'data-validation': 'file:jpg,jpeg:2:MB', })
        self.fields['hospital'].widget.attrs.update(
            {'class': 'form-control', 'autocomplete': 'off', 'tabindex': '8', 'data-validation': 'required', })

    class Meta:
        model = Article
        fields = ['title', 'published', 'excerpt', 'content', 'type', 'image', 'category', 'hospital', ]

from django.forms import widgets
from django.shortcuts import render, redirect
from . import util
import markdown2
from django.utils.safestring import mark_safe
from django import forms
import secrets

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    
    query = request.POST.get('q')
    subEntries = []


    if util.get_entry(query) is not None:
        return redirect('entry', query )

    else:

        for querys in util.list_entries():
            if query.lower() in querys.lower():
                subEntries.append(querys)
                
            
        return render(request, 'encyclopedia/search.html', {
            "entries": subEntries,
            "title": query,
        })

def entry(request, title):

    entry = util.get_entry(title)
    
    if entry is None:

        title_entry = title
        error = 'The page you request does not exist'
        return render(request, "encyclopedia/entry.html", {
            'error': error, 'title_entry': title_entry
        })

    else:

        title_entry = title


        return render(request, "encyclopedia/entry.html", {
            'entry': mark_safe(markdown2.markdown(entry)), 'title_entry': title_entry
        })


class NewEntryForm(forms.Form):

    title = forms.CharField(label='Entry title', widget=forms.TextInput(attrs={'class': 'form-control col-md-10 col-lg-8'}), required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-10 col-lg-8', 'placeholder': 'Enter markdown content'}))

def new_page(request):

    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title) is None:
               util.save_entry(title, content)
               return redirect('entry', title)

            else: 

                error = 'The page you want to create already exists'
                return render(request, 'encyclopedia/new.html', {
                    'error': error
                })

    else:
        form = NewEntryForm()


    return render(request, 'encyclopedia/new.html', {
        'form': form
    })

def edit_entry(request, title):
    
    if request.method == "GET":
        instance = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": NewEntryForm(initial={'content':instance})
        })

    if request.method == "POST":
    
        form = NewEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('entry', title)

    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })

def random(request):

    list_entries = util.list_entries()
    entry = secrets.choice(list_entries)
    return redirect('entry', entry)



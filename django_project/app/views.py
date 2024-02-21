from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .forms import AppNoteUpdateForm
from django.utils.html import escape
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Note
from bs4 import BeautifulSoup
import re
from nltk import word_tokenize, pos_tag, sent_tokenize
from .utils import generate_summary


def index(request):
    return render(request, 'app/register.html')


def validate(request):
    username = request.POST['username']
    data = {
        'taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def get_text(request):
    username = request.POST['username']
    data = {
        'username': username
    }
    return JsonResponse(data)


class UserPostListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'app/user_notes.html'
    context_object_name = 'notes'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        notes = Note.objects.filter(author=user).order_by('-last_updated')
        # for note in notes:
        #     # print(note.content)
        #     if len(note.content) >= 100:
        #         note.content = note.content[:97]
        #         index = note.content.rindex('<') if '<' in note.content else len(note.content)
        #         note.content = note.content[:index] + '...'
        return notes


class NoteDetailView(DetailView):
    model = Note


@login_required()
def note_create(request):
    data = {'title': 'Untitled Note'}
    form = AppNoteUpdateForm(data)
    note = form.save(commit=False)
    note.author = request.user
    if form.is_valid():
        note.save()
        return redirect('note-update', pk=note.pk)
    else:
        return redirect('user-notes')


@login_required()
def note_update(request, pk):
    data = get_object_or_404(Note, pk=pk)
    form = AppNoteUpdateForm(instance=data)

    if hasattr(data, 'author') and request.user != data.author:
        raise PermissionDenied

    if request.method == "POST":
        form = AppNoteUpdateForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, f'Note updated')
            return redirect('note-update', pk)

    sources = []
    for note in [note for note in Note.objects.filter(author=request.user).order_by('-last_updated') if note.pk != pk]:
        content = note.content
        # print(content)
        soup = BeautifulSoup(content, "html.parser")
        for element in soup.find_all(['p']):
            if len(element.text) > 5:
                element_text = str(element).removeprefix('<p>').removesuffix('</p>')
                section_list = sent_tokenize(element_text)
                element.string = ''
                for text in section_list:
                    new_span = soup.new_tag("span")
                    new_span['class'] = 'source-section'
                    new_span.insert(1, BeautifulSoup(text + ' ', "html.parser"))
                    # new_span.append(BeautifulSoup(text, "html.parser"))
                    element.append(new_span)
        for element in soup.find_all(['li']):
            element_text = str(element).removeprefix('<li>').removesuffix('</li>')
            next_index = element_text.index("<ul>") if "<ul>" in element_text else len(element_text)
            text = element_text[:next_index]
            new_span = soup.new_tag("span")
            new_span['class'] = 'source-section'
            new_span.insert(0, BeautifulSoup(text, "html.parser"))
            # print(element.contents)
            while len(element.contents):
                current_element = str(element.contents[0])
                print(current_element)
                if '<ul>' not in current_element:
                    element.contents.pop(0)
                else:
                    break
            element.insert(0, new_span)

        sources.append({'pk': note.pk,
                        'title': note.title,
                        'split_content': content,
                        'content': str(soup)})

    context = {
        "form": form,
        "sources": sources,
        "pk": pk,
    }
    return render(request, 'app/note_form.html', context)


@login_required()
def note_save(request, pk):
    data = get_object_or_404(Note, pk=pk)
    form = AppNoteUpdateForm(request.POST, instance=data)

    if hasattr(data, 'author') and request.user != data.author:
        raise PermissionDenied

    if form.is_valid():
        form.cleaned_data['last_updated'] = timezone.now()
        form.save()
        data = {
            'message': 'Note saved successfully'
        }
        return JsonResponse(data)
    data = {
        'message': 'Error saving note'
    }
    return JsonResponse(data)


def note_autosuggest(request, pk):
    content = request.POST['content']
    # data = {
    #     'suggestion': ' and that\'s what it is',
    # }
    return JsonResponse(data)


def note_suggest(request, pk):
    section = request.POST['section'].strip()
    if section:
        # data = {
        #     'suggestion': section,
        # }
        data = {
            'suggestion': generate_summary(section)
        }
        return JsonResponse(data)


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

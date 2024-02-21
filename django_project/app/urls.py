from django.urls import path
from django.conf.urls import url
from .views import (
    UserPostListView,
    NoteDetailView,
    # NoteCreateView,
    # NoteUpdateView,
    NoteDeleteView,
    note_create, note_update, note_save, note_autosuggest, note_suggest,
    index, validate, get_text
)

urlpatterns = [
    path('ajax/', index, name="index"),
    path('ajax/validate', validate, name="validate"),
    path('ajax/get-text', get_text, name="get-text"),
    path('', UserPostListView.as_view(), name='user-notes'),
    # path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    # path('new/', NoteCreateView.as_view(), name='note-create'),
    path('new/', note_create, name='note-create'),
    # path('<int:pk>/update/', NoteUpdateView.as_view(), name='note-update'),
    path('<int:pk>/', note_update, name='note-update'),
    path('<int:pk>/save/', note_save, name='note-save'),
    path('<int:pk>/autosuggest/', note_autosuggest, name='note-autosuggest'),
    path('<int:pk>/suggest/', note_suggest, name='note-suggest'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
]

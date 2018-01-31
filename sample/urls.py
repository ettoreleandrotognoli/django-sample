from django.urls.conf import path, include

from sample import api_views as api
from sample.web_views import MovementCreateView
from sample.web_views import MovementDeleteView
from sample.web_views import MovementDetailView
from sample.web_views import MovementListView
from sample.web_views import MovementUpdateView
from sample.web_views import summary_view

web_patterns = [
    path('', summary_view, name='movement-summary'),
    path('movement/', MovementListView.as_view(), name='movement-list'),
    path('movement/create/', MovementCreateView.as_view(), name='movement-create'),
    path('movement/<int:pk>/detail/', MovementDetailView.as_view(), name='movement-detail'),
    path('movement/<int:pk>/edit/', MovementUpdateView.as_view(), name='movement-update'),
    path('movement/<int:pk>/delete/', MovementDeleteView.as_view(), name='movement-delete'),
]

api_patterns = [
    path('movement/', api.MovementListView.as_view(), name='movement-list'),
    path('movement/<int:pk>/', api.MovementDetailView.as_view(), name='movement-detail'),
    path('tag/', api.TagListView.as_view(), name='movement-list'),
    path('tag/<int:pk>/', api.TagDetailView.as_view(), name='movement-detail'),
]

urlpatterns = [
    path('', include((web_patterns, 'web'), namespace='web')),
    path('api/', include((api_patterns, 'api'), namespace='api')),
]

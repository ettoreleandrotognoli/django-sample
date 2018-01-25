from django.contrib import admin
from django.urls import path

from sample.views import MovementCreateView
from sample.views import MovementDeleteView
from sample.views import MovementDetailView
from sample.views import MovementListView
from sample.views import MovementUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movement/', MovementListView.as_view(), name='movement-list'),
    path('movement/create/', MovementCreateView.as_view(), name='movement-create'),
    path('movement/<int:pk>/detail/', MovementDetailView.as_view(), name='movement-detail'),
    path('movement/<int:pk>/edit/', MovementUpdateView.as_view(), name='movement-update'),
    path('movement/<int:pk>/delete/', MovementDeleteView.as_view(), name='movement-delete'),
]

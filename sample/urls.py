from django.urls.conf import path, include

from sample.views import MovementCreateView
from sample.views import MovementDeleteView
from sample.views import MovementDetailView
from sample.views import MovementListView
from sample.views import MovementUpdateView

web_patterns = [
    path('movement/', MovementListView.as_view(), name='movement-list'),
    path('movement/create/', MovementCreateView.as_view(), name='movement-create'),
    path('movement/<int:pk>/detail/', MovementDetailView.as_view(), name='movement-detail'),
    path('movement/<int:pk>/edit/', MovementUpdateView.as_view(), name='movement-update'),
    path('movement/<int:pk>/delete/', MovementDeleteView.as_view(), name='movement-delete'),
]

api_patterns = [

]

urlpatterns = [
    path('', include((web_patterns, 'web'), namespace='web')),
    path('api/', include((api_patterns, 'api'), namespace='api')),
]

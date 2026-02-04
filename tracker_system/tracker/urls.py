from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # Автомобили
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
    
    # Трекеры
    path('trackers/', views.TrackerListView.as_view(), name='tracker_list'),
    path('trackers/create/', views.TrackerCreateView.as_view(), name='tracker_create'),
    path('trackers/<int:pk>/', views.TrackerDetailView.as_view(), name='tracker_detail'),
    path('trackers/<int:pk>/update/', views.TrackerUpdateView.as_view(), name='tracker_update'),
    path('trackers/<int:pk>/delete/', views.TrackerDeleteView.as_view(), name='tracker_delete'),
    
    # История установок
    path('installations/', views.InstallationListView.as_view(), name='installation_list'),
    path('installations/create/', views.InstallationCreateView.as_view(), name='installation_create'),
    path('installations/<int:pk>/update/', views.InstallationUpdateView.as_view(), name='installation_update'),
    
    # API
    path('api/installations/', views.installation_history_api, name='installation_api'),
    path('api/installations/car/<int:car_id>/', views.installation_history_api, name='installation_api_car'),
    path('api/installations/tracker/<int:tracker_id>/', views.installation_history_api, name='installation_api_tracker'),
    
    # Отчеты
    path('reports/', views.ReportView.as_view(), name='reports'),
    path('reports/export/', views.export_installations_xlsx, name='export_installations'),
    
    # Главная страница
    path('', views.DashboardView.as_view(), name='dashboard'),
]
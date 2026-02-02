from django.urls import path
from .views import FileUploadView, DashboardStatsView, HistoryView, GeneratePDFView
from .auth_views import RegisterView, LoginView, LogoutView, UserProfileView

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # Data endpoints
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('history/', HistoryView.as_view(), name='history'),
    path('summary/<int:batch_id>/', DashboardStatsView.as_view(), name='summary'),
    path('report/<int:batch_id>/', GeneratePDFView.as_view(), name='report'),
]
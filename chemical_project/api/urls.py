from .views import GeneratePDFView # Import the new view

urlpatterns = [
    # ... existing urls ...
    path('report/<int:batch_id>/', GeneratePDFView.as_view(), name='report'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.save_csv_data),
    # path('test', views.save_csv_per_month),
    # path('testCelery', views.testCelery),
    # path('test', views.daily_transactions),
    path('testing', views.testing),
    path('getAllBrokers', views.getAllBrokers, name="getAllBrokers"),
    path('chart', views.bar_graph, name="chart"),
    path('line', views.line_chart, name="line"),
]
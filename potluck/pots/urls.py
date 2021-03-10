from django.urls import path


from potluck.pots.views import PotListView, PotCreateView

app_name = "pots"

urlpatterns = [
    path("", PotListView.as_view(), name="list"),
    path("create/", PotCreateView.as_view(), name="create"),
]

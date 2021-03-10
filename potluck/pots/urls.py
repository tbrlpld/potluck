from django.urls import path


from potluck.pots.views import PotListView

app_name = "pots"

urlpatterns = [path("", PotListView.as_view(), name="list")]

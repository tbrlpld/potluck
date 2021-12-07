from django import urls
from django.views import generic

from potluck.pots import models as pots_models


class PotList(generic.ListView):
    model = pots_models.Pot
    context_object_name = "pots"
    ordering = "-id"


class PotDetail(generic.DetailView):
    model = pots_models.Pot
    context_object_name = "pot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        picks_url = urls.reverse_lazy(
            "submit_pick_sheet", kwargs={"pot_id": self.object.id}
        )
        context["picks_url"] = self.request.build_absolute_uri(picks_url)

        return context


class PotCreate(generic.CreateView):
    model = pots_models.Pot
    template_name = "pots/pot_create.html"
    fields = ("name", "tiebreaker_description")

    def get_success_url(self):
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.object.id})


class PotDelete(generic.DeleteView):
    model = pots_models.Pot
    template_name = "pots/pot_delete.html"
    success_url = urls.reverse_lazy("pots_list")


class UpdatePotStatus(generic.UpdateView):
    model = pots_models.Pot
    fields = ("status",)
    http_method_names = ["post"]

    def get_success_url(self):
        return urls.reverse_lazy("pot_detail", kwargs={"pk": self.kwargs["pk"]})

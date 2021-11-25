from django import forms, shortcuts
from django.views import generic

from potluck.picks import forms as picks_forms
from potluck.picks import models as picks_models
from potluck.pots import models as pots_models


class Tally(generic.ListView):
    template_name = "picks/tally.html"
    model = picks_models.PickSheet
    context_object_name = "pick_sheets"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pot_id = kwargs.get("pot_id")
        self.pot = shortcuts.get_object_or_404(pots_models.Pot, pk=self.pot_id)

    def get_queryset(self):
        return self.pot.get_tally()

    def get_context_data(self):
        context = super().get_context_data()
        context["pot"] = self.pot
        return context


def submit_pick_sheet(request, pot_id):
    pot = shortcuts.get_object_or_404(pots_models.Pot, pk=pot_id)
    CreatePickFormset = forms.formset_factory(
        picks_forms.CreatePick,
        formset=picks_forms.BaseCreatePickFormset,
        min_num=pot.games.count(),
        max_num=pot.games.count(),
        validate_min=True,
        validate_max=True,
        extra=0,
    )

    if request.method == "POST":
        create_pick_sheet_form = picks_forms.CreatePickSheet(request.POST, pot=pot)
        create_pick_formset = CreatePickFormset(
            request.POST,
            games=pot.games.all(),
        )

        if all((create_pick_sheet_form.is_valid(), create_pick_formset.is_valid())):
            pick_sheet = create_pick_sheet_form.save()

            for pick_form in create_pick_formset:
                pick = pick_form.save(commit=False)
                pick.add_pick_sheet(pick_sheet)

            return shortcuts.render(
                request,
                template_name="picks/thank_you.html",
                context={"pot": pot},
            )
    else:
        create_pick_sheet_form = picks_forms.CreatePickSheet(pot=pot)
        create_pick_formset = CreatePickFormset(games=pot.games.all())

    return shortcuts.render(
        request,
        template_name="picks/submit-pick-sheet.html",
        context={
            "pot": pot,
            "create_pick_sheet_form": create_pick_sheet_form,
            "create_pick_formset": create_pick_formset,
        },
    )

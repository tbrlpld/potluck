from django import forms, shortcuts, urls

from potluck.picks.forms import CreatePickForm, CreatePickSheetForm
from potluck.picks.models import Pot


def pick_create_view(request, pot_id):
    pot = shortcuts.get_object_or_404(Pot, pk=pot_id)
    CreatePickFormset = forms.formset_factory(
        CreatePickForm,
        min_num=pot.games.count(),
        max_num=pot.games.count(),
        validate_min=True,
        validate_max=True,
        extra=0,
    )
    initial_pick_sheet_form = {"pot": pot}
    initial_pick_formset = []
    for game in pot.games.all():
        initial_pick_formset.append({"game": game})

    if request.method == "POST":
        create_pick_sheet_form = CreatePickSheetForm(
            request.POST,
            initial=initial_pick_sheet_form,
        )
        create_pick_formset = CreatePickFormset(
            request.POST,
            initial=initial_pick_formset,
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
        create_pick_sheet_form = CreatePickSheetForm(initial=initial_pick_sheet_form)
        create_pick_formset = CreatePickFormset(initial=initial_pick_formset)

    return shortcuts.render(
        request,
        template_name="picks/create.html",
        context={
            "pot": pot,
            "create_pick_sheet_form": create_pick_sheet_form,
            "create_pick_formset": create_pick_formset,
        },
    )

from django import forms, shortcuts, urls

from potluck.picks.forms import CreateGamePickForm, CreatePickForm
from potluck.picks.models import Pot


def pick_create_view(request, pot_id):
    pot = shortcuts.get_object_or_404(Pot, pk=pot_id)
    CreateGamePickFormset = forms.formset_factory(
        CreateGamePickForm,
        min_num=pot.games.count(),
        max_num=pot.games.count(),
        validate_min=True,
        validate_max=True,
        extra=0,
    )
    initial_pick_form = {"pot": pot}
    initial_game_pick_formset = []
    for game in pot.games.all():
        initial_game_pick_formset.append({"game": game})

    if request.method == "POST":
        create_pick_form = CreatePickForm(
            request.POST,
            initial=initial_pick_form,
        )
        create_game_pick_formset = CreateGamePickFormset(
            request.POST,
            initial=initial_game_pick_formset,
        )

        if all((create_pick_form.is_valid(),
                create_game_pick_formset.is_valid())):
            pick = create_pick_form.save()

            for game_pick_form in create_game_pick_formset:
                game_pick = game_pick_form.save(commit=False)
                game_pick.save_with_pick(pick)

            return shortcuts.render(
                request,
                template_name="picks/thank_you.html",
                context={"pot": pot},
            )
    else:
        create_pick_form = CreatePickForm(initial=initial_pick_form)
        create_game_pick_formset = CreateGamePickFormset(
            initial=initial_game_pick_formset)

    return shortcuts.render(
        request,
        template_name="picks/create.html",
        context={
            "create_pick_form": create_pick_form,
            "create_game_pick_formset": create_game_pick_formset,
        },
    )

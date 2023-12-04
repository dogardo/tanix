
def create_game_context_5(request):

    all_games_c = classic_room.objects.all()
    all_games_n = non_classic_activity_room.objects.all()
    all_games_p = placer_room.objects.all()

    consumer_in_core = consumer.objects.filter(username_id=request.user.id)

    timenow = timezone.now()
    threelater = timenow + datetime.timedelta(hours=3)
    sixlater = timenow + datetime.timedelta(hours=6)
    sixbefore = timenow + datetime.timedelta(hours=-6)
    threebefore = timenow + datetime.timedelta(hours=-3)

    # Tüm oyunları toplu bir şekilde alın
    all_games = list(all_games_c) + list(all_games_n) + list(all_games_p)

    # Filtrelenmiş oyunları alın (zaman kontrolü yapılacak)

    # Etkinliklerde kullanıcı var mı kontrol edin ve filtreyi uygulayın
    filtered_again_1 = [
        game for game in all_games if not any(request.user.id == consumer.username_id for consumer in game.offers.all())
    ]

    filtered_again_2 = [game for game in filtered_again_1 if game.m_time < threebefore]

    filtered_again_3 = [
        game for game in filtered_again_2 if any(request.user.id == consumer.username_id for consumer in game.ppl_existence.all())
    ]

    # Etkinlikleri tarihe göre sıralayın
    sorted_games = sorted(filtered_again_3, key=lambda game: game.m_time, reverse=True)

    return {
        "all_games_c": all_games_c,
        "all_games_n": all_games_n,
        "all_games_p": all_games_p,
        "consumer_in_core": consumer_in_core,
        "timenow": timenow,
        "threelater": threelater,
        "sixlater": sixlater,
        "sorted_games": sorted_games,
        "sixbefore": sixbefore,
        "threebefore":threebefore,
    }

def games_in_o(request, template='games_c_o.html', extra_context=None):
    game_context = create_game_context_5(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page=6, orphans=1) 
    page = request.GET.get('page', 1)

    try:
        paginated_games = paginator.page(page)
        print("1")
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'has_next': False})
        raise Http404

    data = {
        'games': [vars(game) for game in paginated_games]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("3")
        return JsonResponse(data)

    page_template = template

    if extra_context is not None:
        print("4")
        context.update(extra_context)

    context = {
        'games': paginated_games,
        'page_template': page_template,
    }

    # game_context değerlerini context'e ekleyin

    context.update(game_context)

    return render(request, template, context)


def load_more_data_5(request):
    page = request.GET.get('page', 1)  # Sayfa numarasını isteğe ekle
    per_page = 6  # Her sayfada gösterilecek etkinlik sayısı

    game_context = create_game_context_4(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page)

    try:

        paginated_games = paginator.page(page)
    except EmptyPage:

        return JsonResponse({'has_next': False})

    context = {'xgamesx': paginated_games}

    context.update(game_context)

    # Yeni oyunları içeren HTML içeriğini oluştur
    html_content = render_to_string('game_cards_partial_c_o.html', context)

    return JsonResponse({'html_content': html_content})


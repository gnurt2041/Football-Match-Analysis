from analysis.colors import all

def filters(args):
    colors_home = []
    for color in args.color_home:
        for item in all:
            if color == item['name']:
                colors_home.append(item)
    colors_away = []
    for color in args.color_away:
        for item in all:
            if color == item['name']:
                colors_away.append(item)
    colors_referee = []
    for item in all:
        if args.color_referee == item['name']:
            colors_referee.append(item)

    if len(colors_home) > 1:
        colors_home = list(colors_home)
    else:
        colors_home = colors_home
    if len(colors_away) > 1:
        colors_away = list(colors_away)
    else:
        colors_away = colors_away
    colors_referee = colors_referee

    home_filter = {
        "name": args.teams_name[0],
        "colors": colors_home,
    }

    away_filter = {
        "name": args.teams_name[1],
        "colors": colors_away,
    }

    referee_filter = {
        "name": "Referee",
        "colors": colors_referee,
    }
    filters = [
        home_filter,
        away_filter,
        referee_filter
    ]
    return filters

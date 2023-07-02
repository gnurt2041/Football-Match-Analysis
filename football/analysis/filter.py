from analysis.colors import all

def filters(args):
    colors = []
    if len(args.colors) !=0:
        for color in args.colors:
            for item in all:
                if color == item['name']:
                    colors.append(item)
    else:
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

    if len(args.colors) == 0:
        if len(colors_home) > 1:
            colors_home = list(colors_home)
        else:
            colors_home = colors_home
        if len(colors_away) > 1:
            colors_away = list(colors_away)
        else:
            colors_away = colors_away
        colors_referee = colors_referee
    else:
        colors_home = list(colors[:2])
        colors_away = list(colors[2:4])
        colors_referee = [colors[-1]]

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

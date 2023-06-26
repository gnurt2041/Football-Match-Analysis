from analysis.colors import all

def filters(args):
    colors = []
    if len(args.colors) !=0:
        for color in args.colors:
            for item in all:
                if color == item['name']:
                    colors.append(item)
    else:
        colors_t1 = []
        for color in args.color_t1:
            for item in all:
                if color == item['name']:
                    colors_t1.append(item)
        colors_t2 = []
        for color in args.color_t2:
            for item in all:
                if color == item['name']:
                    colors_t2.append(item)
        colors_rf = []
        for item in all:
            if args.color_rf == item['name']:
                colors_rf.append(item)

    if len(args.colors) == 0:
        if len(colors_t1) > 1:
            colors_t1 = list(colors_t1)
        else:
            colors_t1 = colors_t1
        if len(colors_t2) > 1:
            colors_t2 = list(colors_t2)
        else:
            colors_t2 = colors_t2
        colors_rf = colors_rf
    else:
        colors_t1 = list(colors[:2])
        colors_t2 = list(colors[2:4])
        colors_rf = [colors[-1]]

    team_1_filter = {
        "name": args.teams_name[0],
        "colors": colors_t1,
    }

    team_2_filter = {
        "name": args.teams_name[1],
        "colors": colors_t2,
    }

    referee_filter = {
        "name": "Referee",
        "colors": colors_rf,
    }
    filters = [
        team_1_filter,
        team_2_filter,
        referee_filter
    ]
    return filters
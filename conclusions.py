def generate_conclusion(taste, scale, stdevs):
    highest_scale = 0
    highest_index = 0
    for i in range(0, len(scale)):
        if scale[i] > highest_scale:
            highest_scale = scale[i]
            highest_index = i
    highest_taste = taste[highest_index]

    conc_string = ''

    if scale[taste.index('danceability')] > 0.5:
        conc_string += is_danceable()

    if scale[taste.index('acousticness')] > 0.5:
        conc_string += is_acoustic()

    if scale[taste.index('energy')] > 0.5:
        conc_string += is_energetic()

    if scale[taste.index('instrumentalness')] > 0.5:
        conc_string += is_instrumental()

    if scale[taste.index('speechiness')] > 0.5:
        conc_string += is_speechy()

    if scale[taste.index('valence')] > 0.5:
        conc_string += is_happy()
    else:
        conc_string += is_sad()

    if sum(stdevs)/len(stdevs) > 0.2:
        conc_string += is_broad()

    return conc_string


def is_danceable():
    return 'Your playlist has a relatively high danceability rating, meaning it is probably great to dance to. The ' \
           'danceability rating is based on various musical qualities such as tempo, rhythm stability, beat ' \
           'strength, and overall regularity.\n'


def is_acoustic():
    return 'Your playlist appears to be relatively acoustic. The acousticness rating of a playlist is determined ' \
           'based on how acoustic its tracks are, or the lack of electronic qualities.\n'


def is_energetic():
    return 'Your playlist has a relatively high energy rating. This attribute represents a perceptual measure of ' \
           'intensity and activity. The songs in the playlist generally sound fast, loud, and noisy.\n'


def is_instrumental():
    return 'Your playlist appears to contain little vocal content overall. The instrumentalness rating is predicted ' \
           'based on the lack of vocals throughout all tracks on a playlist.\n'


def is_speechy():
    return 'Your playlist has a relatively high speechiness rating, which means it likely contains pure vocals ' \
           'without instrumentation.\n'


def is_happy():
    return 'Your playlist appears to have relatively high valence based on its valence rating. This means the ' \
           'playlist is more musically happy or uplifting, rather than sad, depressed, or angry.\n'


def is_sad():
    return 'Your playlist appears to have relatively low valence based on its valence rating. This means the ' \
           'playlist is more musically dark or sad, rather than happy, cheerful, or uplifting.\n'


def is_broad():
    return 'Overall, it appears that your playlist contains a wide variety of different qualities.\n'

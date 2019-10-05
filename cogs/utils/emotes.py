emotes = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟', '0⃣',
                 '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']


def get(count):
    return emotes[:count]


def get_index(emote):
    return emotes.index(emote)
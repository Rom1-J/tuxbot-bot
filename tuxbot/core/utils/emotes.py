emotes = [chr(0x1F1E6 + i) for i in range(26)]
check = (chr(0x2705), chr(0x2716))


def get(count):
    return emotes[:count]


def get_index(emote):
    return emotes.index(emote)

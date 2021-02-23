# https://python-forum.io/Thread-read-a-binary-file-to-find-its-type
def find_ext(content: bytes) -> str:
    magic_numbers = {
        'png': bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    }

    if content.startswith(magic_numbers["png"]):
        return "png"

    return "txt"

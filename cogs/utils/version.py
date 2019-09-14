class Version:
    def __init__(self, major: int, minor: int, patch: int, **kwargs):
        self.major: int = major
        self.minor: int = minor
        self.patch: int = patch

        self.pre_release = kwargs.get('pre_release', '')
        self.build = kwargs.get('build', '')

    def __str__(self) -> str:
        build = self.build[:10]
        return f'v{self.major}.{self.minor}.{self.patch}{self.pre_release}+{build}'

import argparse


class AutoBanParser(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)

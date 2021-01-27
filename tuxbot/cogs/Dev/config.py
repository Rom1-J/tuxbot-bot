from structured_config import Structure, StrField

HAS_MODELS = False


class DevConfig(Structure):
    sentryKey: str = StrField("")


extra = {
    "sentryKey": {
        "type": str,
        "description": "Sentry KEY for error logging (https://sentry.io/)",
    },
}

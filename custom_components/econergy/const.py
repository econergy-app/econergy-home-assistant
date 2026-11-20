"""Constants for Econergy Cloud."""

from typing import Any

DOMAIN = "econergy"
NAME = "Econergy Cloud 2.1.15"
CONF_FORCE_STATUS_REFRESH = "force_status_refresh"


def mask_identifier(value: Any) -> str:
    """Mask an Econergy identifier while retaining its last four characters."""
    identifier = str(value or "")
    if len(identifier) <= 4:
        return "*" * len(identifier)
    return "*" * (len(identifier) - 4) + identifier[-4:]
BASE_URL = "https://econergy-app.fr/api/smarthome/v1"

# Econergy Lab public OAuth application. Public clients do not use a secret.
OAUTH_CLIENT_ID = "6af46d41611559f97958913b"
OAUTH_AUTHORIZE_URL = "https://econergy-app.fr/api/oauth/authorize"
OAUTH_TOKEN_URL = "https://econergy-app.fr/api/oauth/token"
OAUTH_SCOPES = "readonly write multihome"

PROGRAM_PANEL_PATH = "econergy-program"
PROGRAM_PANEL_URL = "/econergy-program"

# Read the home inventory and the latest values published by the cloud every ten minutes.
INVENTORY_POLL_INTERVAL_SECONDS = 600
# Optional forced radio refresh: one wave every five minutes.
STATUS_REFRESH_CYCLE_SECONDS = 300
# Space individual status-request POSTs to avoid a burst against the cloud.
STATUS_REQUEST_SPACING_SECONDS = 5
# Verify the command and the newly published state at most twice.
STATUS_REQUEST_CHECK_DELAYS_SECONDS = (2, 10)
# Econergy documents at most one status-request per radiator per minute.
STATUS_REQUEST_MIN_INTERVAL_SECONDS = 60
STATUS_REQUEST_DEFAULT_RETRY_AFTER_SECONDS = 60

DEFAULT_MANUAL_SETPOINT_C = 18.0
REQUEST_TIMEOUT_SECONDS = 20
COMMAND_ACK_TIMEOUT_SECONDS = 15
STATE_CONFIRM_TIMEOUT_SECONDS = 18
PROGRAM_COMMAND_TIMEOUT_SECONDS = 60
PROGRAM_CONFIRM_TIMEOUT_SECONDS = 30
PROGRAM_POLL_INTERVAL_SECONDS = 2

MODE_OFF = "OFF"
MODE_FROST = "FROST"
MODE_MANUAL = "MANUAL"
MODE_PROG = "PROG"
SUPPORTED_MODES = {MODE_OFF, MODE_FROST, MODE_MANUAL, MODE_PROG}

PRESET_MANUAL = "Manuel"
PRESET_FROST = "Hors gel"
PRESET_PROGRAM = "Programmation"
PRESET_TO_MODE = {
    PRESET_MANUAL: MODE_MANUAL,
    PRESET_FROST: MODE_FROST,
    PRESET_PROGRAM: MODE_PROG,
}
MODE_TO_PRESET = {v: k for k, v in PRESET_TO_MODE.items()}

WEEKDAYS = {
    "monday": "Lundi",
    "tuesday": "Mardi",
    "wednesday": "Mercredi",
    "thursday": "Jeudi",
    "friday": "Vendredi",
    "saturday": "Samedi",
    "sunday": "Dimanche",
}

"""Diagnostics for the official Econergy Lab API integration."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, mask_identifier


def _mask_nested_ids(value: Any, known_ids: dict[str, str] | None = None) -> Any:
    """Mask home/device IDs in fields and in arbitrary diagnostic strings."""
    known_ids = known_ids or {}
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if key in {"deviceId", "device_id", "homeId", "home_id"} and item is not None:
                result[key] = mask_identifier(item)
            else:
                result[key] = _mask_nested_ids(item, known_ids)
        return result
    if isinstance(value, list):
        return [_mask_nested_ids(item, known_ids) for item in value]
    if isinstance(value, str):
        for raw_id, masked_id in known_ids.items():
            value = value.replace(raw_id, masked_id)
    return value


def _mask_id_mapping(value: Any) -> dict[str, Any]:
    """Mask device IDs used as dictionary keys."""
    if not isinstance(value, dict):
        return {}
    return {mask_identifier(key): _mask_nested_ids(item) for key, item in value.items()}


def _consumption_summary(value: Any) -> dict[str, Any]:
    """Keep diagnostics compact while retaining the archive extent."""
    if not isinstance(value, dict):
        return {}
    days = value.get("days") or []
    valid_days = [
        day for day in days
        if isinstance(day, dict) and isinstance(day.get("date"), str)
    ]
    return {
        "deviceId": mask_identifier(value.get("deviceId")) if value.get("deviceId") else None,
        "powerW": value.get("powerW"),
        "api_days": _mask_nested_ids(valid_days[-15:]),
        "archived_days_count": len(valid_days),
        "archive_start": valid_days[0].get("date") if valid_days else None,
        "archive_end": valid_days[-1].get("date") if valid_days else None,
    }


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    item = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})
    coordinator = item.get("coordinator")
    api = item.get("api")
    data = coordinator.data if coordinator is not None else None
    devices = (data or {}).get("devices", [])
    known_ids = {}
    home_id = entry.data.get("home_id")
    if home_id:
        known_ids[str(home_id)] = mask_identifier(home_id)
    for device in devices:
        raw_id = device.get("id")
        if raw_id:
            known_ids[str(raw_id)] = mask_identifier(raw_id)
    return {
        "entry": {
            "domain": entry.domain,
            "title": entry.title,
            "home_id": mask_identifier(entry.data.get("home_id")),
            "home_name": entry.data.get("home_name"),
            "has_oauth_authorization": bool(
                (entry.data.get("token") or {}).get("access_token")
            ),
            "oauth_token_expires_at": (data or {}).get("expires_at"),
        },
        "api_version": getattr(api, "api_version", None),
        "program_errors": _mask_nested_ids(_mask_id_mapping((data or {}).get("program_errors", {})), known_ids),
        "programs": _mask_nested_ids(_mask_id_mapping((data or {}).get("programs", {})), known_ids),
        "settings": _mask_nested_ids(_mask_id_mapping((data or {}).get("settings", {})), known_ids),
        "settings_errors": _mask_nested_ids(_mask_id_mapping((data or {}).get("settings_errors", {})), known_ids),
        "consumption_loaded_date": getattr(coordinator, "consumption_loaded_date", None),
        "consumption": {
            mask_identifier(device_id): _consumption_summary(value)
            for device_id, value in (data or {}).get("consumption", {}).items()
        },
        "consumption_errors": _mask_nested_ids(_mask_id_mapping((data or {}).get("consumption_errors", {})), known_ids),
        "last_commands": _mask_nested_ids(_mask_id_mapping((data or {}).get("last_commands", {})), known_ids),
        "firmware_versions": _mask_id_mapping(
            getattr(coordinator, "firmware_versions", {})
        ),
        "forced_temperature_refresh_enabled": (
            coordinator.force_status_refresh_enabled if coordinator is not None else True
        ),
        "devices": [
            {
                "id": mask_identifier(device.get("id")),
                "name": device.get("name"),
                "info": _mask_nested_ids(device.get("info"), known_ids),
                "state": _mask_nested_ids(device.get("state"), known_ids),
                "lastSeenAt": device.get("lastSeenAt"),
                "available_api_fields": sorted(
                    str(key) for key in device if not str(key).startswith("_")
                ),
                "status_request": _mask_nested_ids(device.get("_ha_status_request"), known_ids),
                "settings": _mask_nested_ids(
                    (data or {}).get("settings", {}).get(str(device.get("id")), {})
                ),
                "consumption": _consumption_summary(
                    (data or {}).get("consumption", {}).get(str(device.get("id")), {})
                ),
            }
            for device in devices
        ],
    }

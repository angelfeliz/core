"""Generate bluetooth file."""
from __future__ import annotations

from .model import Config, Integration
from .serializer import format_python_namespace


def generate_and_validate(integrations: dict[str, Integration]) -> str:
    """Validate and generate bluetooth data."""
    match_list = []

    for domain in sorted(integrations):
        integration = integrations[domain]

        if not integration.manifest or not integration.config_flow:
            continue

        match_types = integration.manifest.get("bluetooth", [])

        if not match_types:
            continue

        for entry in match_types:
            match_list.append({"domain": domain, **entry})

    return format_python_namespace(
        {"BLUETOOTH": match_list},
        annotations={"BLUETOOTH": "list[dict[str, bool | str | int | list[int]]]"},
    )


def validate(integrations: dict[str, Integration], config: Config) -> None:
    """Validate bluetooth file."""
    bluetooth_path = config.root / "homeassistant/generated/bluetooth.py"
    config.cache["bluetooth"] = content = generate_and_validate(integrations)

    if config.specific_integrations:
        return

    with open(str(bluetooth_path)) as fp:
        current = fp.read()
        if current != content:
            config.add_error(
                "bluetooth",
                "File bluetooth.py is not up to date. Run python3 -m script.hassfest",
                fixable=True,
            )
        return


def generate(integrations: dict[str, Integration], config: Config) -> None:
    """Generate bluetooth file."""
    bluetooth_path = config.root / "homeassistant/generated/bluetooth.py"
    with open(str(bluetooth_path), "w") as fp:
        fp.write(f"{config.cache['bluetooth']}")

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOW_CELL_VOLTAGE
from .coordinator import UPSECoordinator
from .driver import UPSData


@dataclass(frozen=True, kw_only=True)
class UPSEBinarySensorDescription(BinarySensorEntityDescription):
    value_fn: Callable[[UPSData], bool]


BINARY_SENSORS = (
    UPSEBinarySensorDescription(
        key="charging",
        name="Charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        value_fn=lambda data: data.state in {"charging", "fast_charging"},
    ),
    UPSEBinarySensorDescription(
        key="discharging",
        name="Discharging",
        value_fn=lambda data: data.state == "discharging",
    ),
    UPSEBinarySensorDescription(
        key="low_cell_voltage",
        name="Low Cell Voltage",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data: min(data.cell1, data.cell2, data.cell3, data.cell4)
        < LOW_CELL_VOLTAGE,
    ),
)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        UPSEBinarySensor(coordinator, description)
        for description in BINARY_SENSORS
    )


class UPSEBinarySensor(CoordinatorEntity, BinarySensorEntity):
    entity_description: UPSEBinarySensorDescription

    def __init__(
        self,
        coordinator: UPSECoordinator,
        description: UPSEBinarySensorDescription,
    ):
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"upse_{description.key}"
        self._attr_has_entity_name = True

    @property
    def is_on(self):
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "upse")},
            "name": "UPS-E",
            "manufacturer": "Waveshare",
            "model": "UPS HAT (E)",
        }

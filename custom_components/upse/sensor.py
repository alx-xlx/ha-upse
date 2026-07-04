from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTime,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    PERCENTAGE,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UPSECoordinator


@dataclass(frozen=True, kw_only=True)
class UPSESensorDescription(SensorEntityDescription):
    value: str


SENSORS = (
    UPSESensorDescription(
        key="state",
        name="State",
        value="state",
    ),
    UPSESensorDescription(
        key="battery_voltage",
        name="Battery Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value="battery_voltage",
    ),
    UPSESensorDescription(
        key="battery_current",
        name="Battery Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.MILLIAMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value="battery_current",
    ),
    UPSESensorDescription(
        key="battery_percent",
        name="Battery Percentage",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value="battery_percent",
    ),
    UPSESensorDescription(
        key="battery_power",
        name="Battery Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value="battery_power",
    ),
    UPSESensorDescription(
        key="vbus_voltage",
        name="VBUS Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value="vbus_voltage",
    ),
    UPSESensorDescription(
        key="vbus_current",
        name="VBUS Current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.MILLIAMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value="vbus_current",
    ),
    UPSESensorDescription(
        key="vbus_power",
        name="VBUS Power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        value="vbus_power",
    ),
    UPSESensorDescription(
        key="cell1",
        name="Cell 1",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value="cell1",
    ),
    UPSESensorDescription(
        key="cell2",
        name="Cell 2",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value="cell2",
    ),
    UPSESensorDescription(
        key="cell3",
        name="Cell 3",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value="cell3",
    ),
    UPSESensorDescription(
        key="cell4",
        name="Cell 4",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value="cell4",
    ),
    UPSESensorDescription(
        key="cell_delta",
        name="Cell Delta",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value="cell_delta",
    ),
    UPSESensorDescription(
        key="average_cell_voltage",
        name="Average Cell Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value="average_cell_voltage",
    ),
    UPSESensorDescription(
        key="remaining_capacity",
        name="Remaining Capacity",
        native_unit_of_measurement="mAh",
        state_class=SensorStateClass.MEASUREMENT,
        value="remaining_capacity",
    ),
    UPSESensorDescription(
        key="runtime_to_empty",
        name="Runtime To Empty",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        value="runtime_to_empty",
    ),
    UPSESensorDescription(
        key="time_to_full",
        name="Time To Full",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        value="time_to_full",
    ),
)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        UPSESensor(coordinator, description)
        for description in SENSORS
    )


class UPSESensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: UPSECoordinator, description):
        super().__init__(coordinator)

        self.entity_description = description

        self._attr_unique_id = f"upse_{description.key}"

        self._attr_has_entity_name = True

    @property
    def native_value(self):
        return getattr(
            self.coordinator.data,
            self.entity_description.value,
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "upse")},
            "name": "UPS-E",
            "manufacturer": "Waveshare",
            "model": "UPS HAT (E)",
        }

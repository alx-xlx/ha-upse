from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    CONF_I2C_ADDRESS,
    CONF_I2C_BUS,
    DEFAULT_I2C_ADDRESS,
    DEFAULT_I2C_BUS,
    DOMAIN,
)
from .driver import UPSE

from .const import UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class UPSECoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry):
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

        self.driver = UPSE(
            bus=entry.options.get(
                CONF_I2C_BUS,
                entry.data.get(CONF_I2C_BUS, DEFAULT_I2C_BUS),
            ),
            address=entry.options.get(
                CONF_I2C_ADDRESS,
                entry.data.get(CONF_I2C_ADDRESS, DEFAULT_I2C_ADDRESS),
            ),
        )

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(
                self.driver.read
            )
        except Exception as err:
            raise UpdateFailed(err) from err

    async def async_shutdown(self):
        await self.hass.async_add_executor_job(self.driver.close)

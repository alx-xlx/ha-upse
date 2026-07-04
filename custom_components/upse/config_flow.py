from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_I2C_ADDRESS,
    CONF_I2C_BUS,
    DEFAULT_I2C_ADDRESS,
    DEFAULT_I2C_BUS,
    DEFAULT_NAME,
    DOMAIN,
)


class UPSEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id("upse")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=DEFAULT_NAME,
                data={
                    CONF_I2C_BUS: user_input[CONF_I2C_BUS],
                    CONF_I2C_ADDRESS: user_input[CONF_I2C_ADDRESS],
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_I2C_BUS, default=DEFAULT_I2C_BUS): int,
                    vol.Required(
                        CONF_I2C_ADDRESS,
                        default=DEFAULT_I2C_ADDRESS,
                    ): vol.All(int, vol.Range(min=0x03, max=0x77)),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return UPSEOptionsFlow(config_entry)


class UPSEOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_I2C_BUS,
                        default=self.config_entry.data.get(
                            CONF_I2C_BUS,
                            DEFAULT_I2C_BUS,
                        ),
                    ): int,
                    vol.Required(
                        CONF_I2C_ADDRESS,
                        default=self.config_entry.data.get(
                            CONF_I2C_ADDRESS,
                            DEFAULT_I2C_ADDRESS,
                        ),
                    ): vol.All(int, vol.Range(min=0x03, max=0x77)),
                }
            ),
        )

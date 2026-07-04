# UPS-E for Home Assistant

Home Assistant custom integration for the Waveshare UPS HAT (E). It reads the UPS-E over I2C and exposes battery, VBUS, cell voltage, charging, discharging, and low-cell-voltage entities.

## Installation with HACS

1. Open HACS.
2. Open the three-dot menu and choose **Custom repositories**.
3. Add this repository URL.
4. Select **Integration** as the category.
5. Install **UPS-E**.
6. Restart Home Assistant.
7. Go to **Settings > Devices & services > Add integration** and add **UPS-E**.

## Docker Access To I2C

Home Assistant must be able to access the Raspberry Pi I2C device. For Docker Compose, expose `/dev/i2c-1`:

```yaml
services:
  homeassistant:
    devices:
      - /dev/i2c-1:/dev/i2c-1
```

If your container is not already privileged, you may also need:

```yaml
    privileged: true
```

Make sure I2C is enabled on the host and that the UPS-E is visible:

```bash
ls -l /dev/i2c-1
i2cdetect -y 1
```

The UPS-E normally appears at address `0x2d`.

## Entities

This integration creates sensors for:

- UPS state
- Battery voltage, current, percent, power, and remaining capacity
- Runtime to empty or time to full
- VBUS voltage, current, and power
- Cell 1-4 voltages
- Average cell voltage and cell delta

It also creates binary sensors for:

- Charging
- Discharging
- Low cell voltage

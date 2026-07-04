from __future__ import annotations

from dataclasses import dataclass

from smbus2 import SMBus


@dataclass
class UPSData:
    state: str

    vbus_voltage: int
    vbus_current: int
    vbus_power: int

    battery_voltage: int
    battery_current: int
    battery_percent: int
    remaining_capacity: int

    runtime_to_empty: int | None
    time_to_full: int | None

    cell1: int
    cell2: int
    cell3: int
    cell4: int

    @property
    def cell_delta(self) -> int:
        return max(self.cell1, self.cell2, self.cell3, self.cell4) - min(
            self.cell1, self.cell2, self.cell3, self.cell4
        )

    @property
    def battery_power(self) -> float:
        return round(
            self.battery_voltage * self.battery_current / 1_000_000,
            2,
        )

    @property
    def average_cell_voltage(self) -> float:
        return round(
            (
                self.cell1
                + self.cell2
                + self.cell3
                + self.cell4
            )
            / 4,
            1,
        )

    def as_dict(self):
        return self.__dict__ | {
            "battery_power": self.battery_power,
            "cell_delta": self.cell_delta,
            "average_cell_voltage": self.average_cell_voltage,
        }


class UPSE:
    def __init__(self, bus: int = 1, address: int = 0x2D):
        self.bus = SMBus(bus)
        self.address = address

    @staticmethod
    def _u16(lsb: int, msb: int) -> int:
        return lsb | (msb << 8)

    @staticmethod
    def _s16(lsb: int, msb: int) -> int:
        value = lsb | (msb << 8)
        if value >= 0x8000:
            value -= 0x10000
        return value

    def read(self) -> UPSData:
        status = self.bus.read_i2c_block_data(self.address, 0x02, 1)[0]

        if status & 0x40:
            state = "fast_charging"
        elif status & 0x80:
            state = "charging"
        elif status & 0x20:
            state = "discharging"
        else:
            state = "idle"

        d = self.bus.read_i2c_block_data(self.address, 0x10, 6)

        vbus_voltage = self._u16(d[0], d[1])
        vbus_current = self._u16(d[2], d[3])
        vbus_power = self._u16(d[4], d[5])

        d = self.bus.read_i2c_block_data(self.address, 0x20, 12)

        battery_voltage = self._u16(d[0], d[1])
        battery_current = self._s16(d[2], d[3])
        battery_percent = self._u16(d[4], d[5])
        remaining_capacity = self._u16(d[6], d[7])

        runtime_to_empty = None
        time_to_full = None

        if battery_current < 0:
            runtime_to_empty = self._u16(d[8], d[9])
        else:
            time_to_full = self._u16(d[10], d[11])

        d = self.bus.read_i2c_block_data(self.address, 0x30, 8)

        return UPSData(
            state=state,
            vbus_voltage=vbus_voltage,
            vbus_current=vbus_current,
            vbus_power=vbus_power,
            battery_voltage=battery_voltage,
            battery_current=battery_current,
            battery_percent=battery_percent,
            remaining_capacity=remaining_capacity,
            runtime_to_empty=runtime_to_empty,
            time_to_full=time_to_full,
            cell1=self._u16(d[0], d[1]),
            cell2=self._u16(d[2], d[3]),
            cell3=self._u16(d[4], d[5]),
            cell4=self._u16(d[6], d[7]),
        )

    def shutdown(self):
        self.bus.write_byte_data(self.address, 0x01, 0x55)

    def close(self):
        self.bus.close()
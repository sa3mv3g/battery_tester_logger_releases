import os
import uuid
import json
from batterychargerlogger.app import Application
from batterychargerlogger.mbDeviceConfig import ModbusDeviceConfig
from batterychargerlogger.common import HoldingRegister, Coil
from batterychargerlogger.common import LoggingParameter
from batterychargerlogger.common import REGISTER_TYPE_HOLDING_REGISTER
from batterychargerlogger.common import REGISTER_DATATYPE_F32
from batterychargerlogger.common import MonitorGroup
from batterychargerlogger.common import ControlGroup
from batterychargerlogger.common import appSerialPortInfo

MODBUS_DEVICE_ADDRESS_START = 1
MODBUS_DEVICE_ADDRESS_END = 30

class batteryChargerInstrument(ModbusDeviceConfig):

    def __init__(self, deviceId:int, portInfo):
        super().__init__(deviceId, ModbusDeviceConfig.INTERFACE_TYPE_RTU, portInfo)
        self.device_name = "Battery Tester"
        self.update_holding_registers()
        self.update_input_registers()
        self.update_discrete_inputs()
        self.update_coils()

    def update_holding_registers(self):
        hrlist = [
            HoldingRegister(0x00, 0, label="pwm", description="PWM Value"),
            HoldingRegister(0x01, 0, label="AIN0_RAW", description="Holds uncalibrated value of analog input channel 0, writing to this register has no effect. It will be overwritten with new value before accessing this reigster"),
            HoldingRegister(0x02, 0, label="AIN1_RAW", description="Holds uncalibrated value of analog input channel 1, writing to this register has no effect. It will be overwritten with new value before accessing this reigster"),
            HoldingRegister(0x03, 0, label="AIN2_RAW", description="Holds uncalibrated value of analog input channel 2, writing to this register has no effect. It will be overwritten with new value before accessing this reigster"),
            HoldingRegister(0x04, 0, label="AIN3_RAW", description="Holds uncalibrated value of analog input channel 3, writing to this register has no effect. It will be overwritten with new value before accessing this reigster"),
            HoldingRegister(0x05, 0, label="AIN0", description="holds calibrated value of analog input channel 0, This is read only register", dataType=REGISTER_DATATYPE_F32
                            ,logging_parameters = LoggingParameter("Battery Voltage", "", historyBufferLen=7200, display_format="%.1f")),
            HoldingRegister(0x07, 0, label="AIN1", description="holds calibrated value of analog input channel 1, This is read only register", dataType=REGISTER_DATATYPE_F32
                            ,logging_parameters = LoggingParameter("Battery Temperature", "deg. C", historyBufferLen=7200, display_format="%.1f")),
            HoldingRegister(0x09, 0, label="AIN2", description="holds calibrated value of analog input channel 2, This is read only register", dataType=REGISTER_DATATYPE_F32
                            ,logging_parameters = LoggingParameter("Charging Current", "A", historyBufferLen=7200, display_format="%.1f")),
            HoldingRegister(0x0B, 0, label="AIN3", description="holds calibrated value of analog input channel 3, This is read only register", dataType=REGISTER_DATATYPE_F32
                            ,logging_parameters = LoggingParameter("Discharging Current", "A", historyBufferLen=7200, display_format="%.1f")),
            HoldingRegister(
                address=13,
                value=0,
                label="AIN0_SF",
                description="Analog Input Scale Factor",
                logging_parameters=LoggingParameter("AIN0_SF", "", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=15,
                value=0,
                label="AIN0_OT",
                description="Analog Input Offset term",
                logging_parameters=LoggingParameter("AIN0_OT", "", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=17,
                value=0,
                label="CHARGING_CHARGE",
                description="Charge supplied while charging",
                logging_parameters=LoggingParameter(
                    "Charge at charging", "C", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=19,
                value=0,
                label="AIN1_SF",
                description="Analog Input Scale Factor",
                logging_parameters=LoggingParameter("AIN1_SF", "", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=21,
                value=0,
                label="AIN1_OT",
                description="Analog Input Offset term",
                logging_parameters=LoggingParameter("AIN1_OT", "", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=23,
                value=0,
                label="DISCHARGING_CHARGE",
                description="Charge taken during discharging",
                logging_parameters=LoggingParameter(
                    "Charge at discharging", "C", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=25,
                value=0,
                label="AIN2_SF",
                description="Analog Input Scale Factor",
                logging_parameters=LoggingParameter("AIN2_SF", "", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=27,
                value=0,
                label="AIN2_OT",
                description="Analog Input Offset term",
                logging_parameters=LoggingParameter("AIN2_OT", "", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=29,
                value=0,
                label="NET_CHARGE",
                description="Net charge supplied to battery",
                logging_parameters=LoggingParameter("NET Charge", "C", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=31,
                value=0,
                label="AIN3_SF",
                description="Analog Input Scale Factor",
                logging_parameters=LoggingParameter("AIN3_SF", "", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=33,
                value=0,
                label="AIN3_OT",
                description="Analog Input Offset term",
                logging_parameters=LoggingParameter("AIN3_OT", "", historyBufferLen=1, display_format="%.5f")
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=35,
                value=0,
                label="BAT_CON_TIM_HIGH",
                description="Time at which battry is connected",
            ),
            HoldingRegister(
                address=36,
                value=0,
                label="BAT_CON_TIM_LOW",
                description="Time at which battry is connected",
            ),
            HoldingRegister(
                address=37,
                value=0,
                label="VERSION_MAJOR",
                description="VERSION MAJOR",
            ),
            HoldingRegister(
                address=38,
                value=0,
                label="VERSION_MINOR",
                description="VERSION MINOR",
            ),
            HoldingRegister(
                address=39,
                value=0,
                label="VERSION_PATCH",
                description="VERSION PATCH",
            ),
            HoldingRegister(
                address=40,
                value=0,
                label="RTC_LOCK",
                description="When 0x5555 value is wrriten to this register, then value that is written at RTC_HOUR, \
                    RTC_MINS & RTC_SECS will be written in RTC.",
            ),
            HoldingRegister(
                address=41,
                value=0,
                label="RTC_HOUR",
                description="Value of hour taken from RTC",
            ),
            HoldingRegister(
                address=42,
                value=0,
                label="RTC_MIN",
                description="Value of minute taken from RTC",
            ),
            HoldingRegister(
                address=43,
                value=0,
                label="RTC_SEC",
                description="Value of second taken from RTC",
            ),
            HoldingRegister(
                address=44,
                value=0,
                label="TRIGGER_HOUR",
                description="RTC hour at which charging trigger came",
            ),
            HoldingRegister(
                address=45,
                value=0,
                label="TRIGGER_MINS",
                description="RTC minute at which charging trigger came",
            ),
            HoldingRegister(
                address=46,
                value=0,
                label="TRIGGER_SECS",
                description="RTC second at which charging trigger came",
            ),
            HoldingRegister(
                address=47,
                value=0,
                label="CHARGING_TIMEPERIOD_HOUR",
                description="timeperiod in which battery is supposed to be charged (hours)",
            ),
            HoldingRegister(
                address=48,
                value=0,
                label="CHARGING_TIMEPERIOD_MINS",
                description="timeperiod in which battery is supposed to be charged (mins)",
            ),
            HoldingRegister(
                address=49,
                value=0,
                label="CHARGING_TIMEPERIOD_SECS",
                description="timeperiod in which battery is supposed to be charged (secs)",
            ),
            HoldingRegister(
                address=50,
                value=0,
                label="SET_BV",
                description="Expected battery voltage at trigger time + timeperiod",
                logging_parameters=LoggingParameter(
                    "Expected Battery Voltage",
                    "V", historyBufferLen=1
                    , display_format="%.5f"
                )
                , dataType=REGISTER_DATATYPE_F32
            ),
            HoldingRegister(
                address=52,
                value=0,
                label="TARGET_DISCHARGE_CURR",
                description="target dicharging current at which to discharge the battery during discharging test",
                logging_parameters=LoggingParameter(
                    "Target Discharge Current",
                    "A", historyBufferLen=1
                    , display_format="%.5f"
                )
                , dataType=REGISTER_DATATYPE_F32
            ),
        ]

        for hr in hrlist:
            self.holding_registers[hr.address] = hr

    def update_input_registers(self):
        pass

    def update_discrete_inputs(self):
        pass

    def update_coils(self):
        coilsList = [
            Coil(0, False, label="DOUT0", description="value of digital output 0"),
            Coil(1, False, label="DOUT1", description="value of digital output 1"),
            Coil(2, False, label="DOUT2", description="value of digital output 2"),
            Coil(3, False, label="DOUT3", description="value of digital output 3"),
            Coil(4, False, label="DIN0", description="value of digital input 0"),
            Coil(5, False, label="DIN1", description="value of digital input 1"),
            Coil(6, False, label="DIN2", description="value of digital input 2"),
            Coil(7, False, label="DIN3", description="value of digital input 3"),
        ]
        for coil in coilsList:
            self.coils[coil.address] = coil

class monitorAllBatteryChargerInstruments(MonitorGroup):
    def __init__(self, **kwargs):
        super().__init__("Monitor All Instruments", **kwargs)
        for dev_addr in range(MODBUS_DEVICE_ADDRESS_START, MODBUS_DEVICE_ADDRESS_END + 1):
            self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, dev_addr, 5)
            self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, dev_addr, 7)
            self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, dev_addr, 9)
            self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, dev_addr, 11)

class monitorBatteryChargerInstrument(MonitorGroup):
    def __init__(self, name:str, mbdev:ModbusDeviceConfig):
        super().__init__(name)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 5)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 7)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 9)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 11)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 17)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 23)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 29)

class controlBatteryChargingParam(ControlGroup):
    def __init__(self, name:str, mbdev:ModbusDeviceConfig, **kw):
        super().__init__(name, **kw)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 47)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 48)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 49)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 50)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 52)

class calibrateBatteryChargingInstrument(ControlGroup):
    def __init__(self, name:str, mbdev:ModbusDeviceConfig, **kw):
        super().__init__(name, **kw)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 13)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 15)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 17)

        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 19)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 21)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 23)

        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 25)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 27)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 29)

        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 31)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 33)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 35)


        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 40)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 41)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 42)
        self.add_register_reference(REGISTER_TYPE_HOLDING_REGISTER, mbdev.device_address, 43)


def test_generate_battery_charger_v1_json():
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'test','jsonConfigs', 'battery_charger_v1_2_ind.json')

    if not os.path.exists(os.path.dirname(json_file_path)):
        os.makedirs(os.path.dirname(json_file_path))

    fc = Application.fileContents()
    sp = appSerialPortInfo(str(uuid.uuid4()), "com6", 19200,"None", 1, 1000)
    conta = []
    contb = []
    for dev_addr in range(MODBUS_DEVICE_ADDRESS_START, MODBUS_DEVICE_ADDRESS_END + 1):
        mbdev = batteryChargerInstrument(dev_addr, {})
        mbdev.interface_type = ModbusDeviceConfig.INTERFACE_TYPE_RTU
        mbdev.configure_serial_interface_from_class(sp)
        monA = monitorBatteryChargerInstrument(f"Battery Charger Instrument {dev_addr}", mbdev)
        controlA = controlBatteryChargingParam(f"Control Battery Charging Parameters {dev_addr}", mbdev)
        calibrateA = calibrateBatteryChargingInstrument(f"Calibrate Battery Charging Instrument {dev_addr}", mbdev)
        fc.addModbusDevice(mbdev)
        fc.addMonitorGroup(monA)
        conta.append(controlA)
        contb.append(calibrateA)
    for controlA in conta:
        fc.addControlGroup(controlA)
    for calibrateA in contb:
        fc.addControlGroup(calibrateA)

    fc.addSerialPort(sp)
    with open(json_file_path, 'w') as json_file:
        json.dump(fc.to_dict(), json_file)

if __name__ == "__main__":
    test_generate_battery_charger_v1_json()
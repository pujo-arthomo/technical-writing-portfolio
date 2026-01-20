# ============================================================
# File: sensor-data-processing.py
# Purpose: Explain how raw sensor data is processed and validated
# Context: Reference logic for device documentation
# ============================================================

from typing import List, Dict, Optional


class SensorDataError(Exception):
    """Raised when sensor data processing fails."""
    pass


def normalize_value(
    raw_value: float,
    min_value: float,
    max_value: float
) -> float:
    """
    Normalizes a sensor value to ensure it stays within
    the configured operating range.
    """
    if raw_value < min_value:
        return min_value
    if raw_value > max_value:
        return max_value
    return raw_value


def apply_scaling(
    value: float,
    scale_factor: float,
    offset: float
) -> float:
    """
    Applies scaling and offset to a sensor value.
    """
    return (value * scale_factor) + offset


def process_sensor_reading(
    reading: Dict[str, float],
    config: Dict[str, float]
) -> Dict[str, float]:
    """
    Processes a single sensor reading based on configuration.
    """
    try:
        raw = reading["raw_value"]
        min_v = config["min"]
        max_v = config["max"]
        scale = config["scale"]
        offset = config["offset"]
    except KeyError as exc:
        raise SensorDataError(f"Missing configuration parameter: {exc}")

    normalized = normalize_value(raw, min_v, max_v)
    processed = apply_scaling(normalized, scale, offset)

    return {
        "raw_value": raw,
        "normalized_value": normalized,
        "processed_value": processed
    }


def process_sensor_batch(
    readings: List[Dict[str, float]],
    config: Dict[str, float]
) -> List[Dict[str, float]]:
    """
    Processes a batch of sensor readings.
    """
    processed_batch = []

    for index, reading in enumerate(readings, start=1):
        try:
            result = process_sensor_reading(reading, config)
            processed_batch.append(result)
        except SensorDataError as error:
            processed_batch.append({
                "error": str(error),
                "reading_index": index
            })

    return processed_batch


# ============================================================
# File: device-state-machine.py
# Purpose: Illustrate device operational states and transitions
# ============================================================

class DeviceState:
    POWER_OFF = "power_off"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    FAULT = "fault"
    MAINTENANCE = "maintenance"


class InvalidStateTransition(Exception):
    pass


class DeviceStateMachine:
    def __init__(self):
        self.state = DeviceState.POWER_OFF
        self.history = []

    def _transition(self, new_state: str):
        self.history.append((self.state, new_state))
        self.state = new_state

    def power_on(self):
        if self.state != DeviceState.POWER_OFF:
            raise InvalidStateTransition("Power on allowed only from POWER_OFF")
        self._transition(DeviceState.INITIALIZING)

    def initialization_complete(self):
        if self.state != DeviceState.INITIALIZING:
            raise InvalidStateTransition("Initialization not in progress")
        self._transition(DeviceState.READY)

    def start_operation(self):
        if self.state != DeviceState.READY:
            raise InvalidStateTransition("Device not ready")
        self._transition(DeviceState.RUNNING)

    def enter_maintenance(self):
        if self.state not in [DeviceState.READY, DeviceState.RUNNING]:
            raise InvalidStateTransition("Cannot enter maintenance from current state")
        self._transition(DeviceState.MAINTENANCE)

    def trigger_fault(self, reason: Optional[str] = None):
        self._transition(DeviceState.FAULT)

    def reset_from_fault(self):
        if self.state != DeviceState.FAULT:
            raise InvalidStateTransition("No fault to reset")
        self._transition(DeviceState.INITIALIZING)


# ============================================================
# File: firmware-update-flow.py
# Purpose: Describe firmware update sequence and safeguards
# ============================================================

class FirmwareUpdateError(Exception):
    pass


def verify_firmware_package(package_metadata: Dict[str, str]) -> bool:
    """
    Verifies firmware package metadata.
    """
    required_keys = ["version", "checksum", "compatible_device"]

    for key in required_keys:
        if key not in package_metadata:
            raise FirmwareUpdateError(f"Missing package metadata: {key}")

    return True


def firmware_update_steps() -> List[str]:
    """
    Returns the ordered steps for a firmware update.
    """
    return [
        "verify_package",
        "backup_configuration",
        "stop_services",
        "apply_firmware",
        "restart_system",
        "verify_system_state"
    ]


def execute_firmware_update(package_metadata: Dict[str, str]) -> str:
    """
    Executes a simplified firmware update workflow.
    """
    verify_firmware_package(package_metadata)

    steps = firmware_update_steps()
    completed_steps = []

    for step in steps:
        completed_steps.append(step)

    return f"Firmware update completed. Steps executed: {completed_steps}"


# ============================================================
# File: diagnostic-logic.py
# Purpose: Explain how diagnostic conditions are evaluated
# ============================================================

def evaluate_power_status(voltage_ok: bool, current_ok: bool) -> str:
    if not voltage_ok:
        return "power_voltage_fault"
    if not current_ok:
        return "power_current_fault"
    return "power_ok"


def evaluate_sensor_status(sensor_detected: bool, sensor_value_valid: bool) -> str:
    if not sensor_detected:
        return "sensor_missing"
    if not sensor_value_valid:
        return "sensor_invalid_value"
    return "sensor_ok"


def evaluate_communication_status(link_active: bool, error_rate: float) -> str:
    if not link_active:
        return "communication_lost"
    if error_rate > 0.05:
        return "communication_degraded"
    return "communication_ok"


def evaluate_system_health(status_inputs: Dict[str, str]) -> str:
    """
    Aggregates subsystem diagnostics into overall system status.

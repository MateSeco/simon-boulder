class HardwareError(Exception):
    """Base exception for hardware errors"""
    pass

class ButtonError(HardwareError):
    """Exception for button-related errors"""
    pass

class LEDError(HardwareError):
    """Exception for LED-related errors"""
    pass

class BuzzerError(HardwareError):
    """Exception for buzzer-related errors"""
    pass
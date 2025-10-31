"""Input validation utilities."""

import re
from typing import Optional, Tuple


class Validators:
    """Input validation utilities."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(email)))

    @staticmethod
    def validate_phone_number(phone: str, country_code: str = '+91') -> bool:
        """Validate phone number (India by default)."""
        # Remove spaces and dashes
        phone = str(phone).replace(' ', '').replace('-', '')

        # India: +91 or 0 followed by 10 digits
        pattern = r'^(\+91|0)?[6-9]\d{9}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_field_name(name: str, min_len: int = 2, max_len: int = 100) -> Tuple[bool, Optional[str]]:
        """
        Validate field name.

        Returns:
            (is_valid, error_message)
        """
        if not isinstance(name, str):
            return False, 'Field name must be text'

        name = name.strip()

        if len(name) < min_len:
            return False, f'Field name must be at least {min_len} characters'

        if len(name) > max_len:
            return False, f'Field name must be less than {max_len} characters'

        # Allow alphanumeric, spaces, hyphens, underscores
        if not re.match(r'^[\w\s\-]*$', name):
            return False, 'Field name contains invalid characters'

        return True, None

    @staticmethod
    def validate_crop_name(crop_name: str) -> Tuple[bool, Optional[str]]:
        """Validate crop name."""
        if not isinstance(crop_name, str) or not crop_name.strip():
            return False, 'Crop name is required'

        crop_name = crop_name.strip()

        if len(crop_name) < 2:
            return False, 'Crop name too short'

        if len(crop_name) > 100:
            return False, 'Crop name too long'

        return True, None

    @staticmethod
    def validate_soil_ph(ph: float) -> Tuple[bool, Optional[str]]:
        """Validate soil pH value."""
        try:
            ph_val = float(ph)
            if ph_val < 0 or ph_val > 14:
                return False, 'Soil pH must be between 0 and 14'
            return True, None
        except (TypeError, ValueError):
            return False, 'Soil pH must be a number'

    @staticmethod
    def validate_npk_level(value: float) -> Tuple[bool, Optional[str]]:
        """Validate NPK level (in ppm)."""
        try:
            val = float(value)
            if val < 0 or val > 10000:
                return False, 'NPK level must be between 0 and 10000 ppm'
            return True, None
        except (TypeError, ValueError):
            return False, 'NPK level must be a number'

    @staticmethod
    def validate_moisture_percent(moisture: float) -> Tuple[bool, Optional[str]]:
        """Validate soil moisture percentage."""
        try:
            moisture_val = float(moisture)
            if moisture_val < 0 or moisture_val > 100:
                return False, 'Moisture must be between 0 and 100%'
            return True, None
        except (TypeError, ValueError):
            return False, 'Moisture must be a number'

    @staticmethod
    def validate_field_size(size: float, unit: str) -> Tuple[bool, Optional[str]]:
        """Validate field size."""
        try:
            size_val = float(size)
            if size_val <= 0:
                return False, 'Field size must be greater than 0'

            if unit not in ['acres', 'hectares']:
                return False, 'Unit must be acres or hectares'

            # Max reasonable field size: 1000 hectares (~2500 acres)
            if unit == 'hectares' and size_val > 1000:
                return False, 'Field size too large'

            if unit == 'acres' and size_val > 2500:
                return False, 'Field size too large'

            return True, None
        except (TypeError, ValueError):
            return False, 'Field size must be a number'

    @staticmethod
    def validate_date_range(start_date, end_date) -> Tuple[bool, Optional[str]]:
        """Validate date range."""
        try:
            from datetime import datetime
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date)
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date)

            if start_date >= end_date:
                return False, 'Start date must be before end date'

            return True, None
        except Exception:
            return False, 'Invalid date format'

    @staticmethod
    def validate_image_file(file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate image file."""
        import os
        from pathlib import Path

        if not isinstance(file_path, str):
            return False, 'File path must be text'

        # Check file exists
        if not os.path.exists(file_path):
            return False, 'File does not exist'

        # Check file extension
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        ext = Path(file_path).suffix.lower()

        if ext not in valid_extensions:
            return False, f'File must be image (jpg, png, bmp, gif)'

        # Check file size (max 10 MB)
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:
            return False, 'Image file too large (max 10 MB)'

        return True, None

    @staticmethod
    def validate_language_code(lang_code: str) -> Tuple[bool, Optional[str]]:
        """Validate language code."""
        from config.settings import SUPPORTED_LANGUAGES

        if lang_code not in SUPPORTED_LANGUAGES:
            return False, f'Unsupported language: {lang_code}'

        return True, None


def validate_email(email: str) -> bool:
    """Validate email."""
    return Validators.validate_email(email)


def validate_phone_number(phone: str) -> bool:
    """Validate phone number."""
    return Validators.validate_phone_number(phone)


def validate_soil_ph(ph: float) -> Tuple[bool, Optional[str]]:
    """Validate soil pH."""
    return Validators.validate_soil_ph(ph)


def validate_field_size(size: float, unit: str) -> Tuple[bool, Optional[str]]:
    """Validate field size."""
    return Validators.validate_field_size(size, unit)

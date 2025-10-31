"""Data formatting utilities."""

from datetime import datetime, timedelta
from typing import Union


class Formatters:
    """Data formatting utilities."""

    @staticmethod
    def format_currency(amount: float, currency: str = '₹') -> str:
        """Format amount as currency."""
        try:
            return f'{currency}{amount:,.2f}'
        except (TypeError, ValueError):
            return f'{currency}0.00'

    @staticmethod
    def format_percentage(value: float, decimals: int = 1) -> str:
        """Format value as percentage."""
        try:
            return f'{float(value):.{decimals}f}%'
        except (TypeError, ValueError):
            return '0.0%'

    @staticmethod
    def format_date(date: Union[str, datetime], format_str: str = '%d-%m-%Y') -> str:
        """Format date."""
        try:
            if isinstance(date, str):
                date = datetime.fromisoformat(date)
            elif isinstance(date, datetime):
                pass
            else:
                return 'Invalid date'
            return date.strftime(format_str)
        except Exception:
            return 'Invalid date'

    @staticmethod
    def format_time_ago(timestamp: datetime) -> str:
        """Format timestamp as 'time ago'."""
        try:
            delta = datetime.utcnow() - timestamp
            total_seconds = int(delta.total_seconds())

            if total_seconds < 60:
                return f'{total_seconds}s ago'
            elif total_seconds < 3600:
                minutes = total_seconds // 60
                return f'{minutes}m ago'
            elif total_seconds < 86400:
                hours = total_seconds // 3600
                return f'{hours}h ago'
            else:
                days = total_seconds // 86400
                return f'{days}d ago'
        except Exception:
            return 'Unknown'

    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """Format number with proper separators."""
        try:
            return f'{float(value):,.{decimals}f}'
        except (TypeError, ValueError):
            return '0.00'

    @staticmethod
    def format_temperature(celsius: float) -> str:
        """Format temperature."""
        try:
            return f'{float(celsius):.1f}°C'
        except (TypeError, ValueError):
            return '--°C'

    @staticmethod
    def format_rainfall(mm: float) -> str:
        """Format rainfall amount."""
        try:
            return f'{float(mm):.1f}mm'
        except (TypeError, ValueError):
            return '--mm'

    @staticmethod
    def format_humidity(percent: float) -> str:
        """Format humidity percentage."""
        try:
            return f'{float(percent):.0f}%'
        except (TypeError, ValueError):
            return '--'

    @staticmethod
    def format_soil_ph(ph: float) -> str:
        """Format soil pH value with status."""
        try:
            ph_val = float(ph)
            if ph_val < 6.0:
                status = 'Acidic'
            elif ph_val < 7.0:
                status = 'Slightly Acidic'
            elif ph_val < 8.0:
                status = 'Neutral'
            elif ph_val < 8.5:
                status = 'Slightly Alkaline'
            else:
                status = 'Alkaline'
            return f'{ph_val:.2f} ({status})'
        except (TypeError, ValueError):
            return '--'

    @staticmethod
    def format_file_size(bytes_size: int) -> str:
        """Format file size in human-readable format."""
        try:
            size = float(bytes_size)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f'{size:.2f}{unit}'
                size /= 1024.0
            return f'{size:.2f}TB'
        except (TypeError, ValueError):
            return '0B'

    @staticmethod
    def format_crop_yield(kg_per_hectare: float) -> str:
        """Format crop yield."""
        try:
            yield_val = float(kg_per_hectare)
            quintals = yield_val / 100  # 1 quintal = 100 kg
            return f'{quintals:.2f} quintals/hectare'
        except (TypeError, ValueError):
            return '--'

    @staticmethod
    def format_profit(profit_inr: float) -> str:
        """Format profit amount."""
        try:
            amount = float(profit_inr)
            return f'₹{amount:,.0f}'
        except (TypeError, ValueError):
            return '₹0'

    @staticmethod
    def format_confidence_score(score: float) -> str:
        """Format ML confidence score."""
        try:
            confidence = float(score) * 100
            if confidence >= 90:
                status = 'Very High'
            elif confidence >= 75:
                status = 'High'
            elif confidence >= 60:
                status = 'Medium'
            else:
                status = 'Low'
            return f'{confidence:.0f}% ({status})'
        except (TypeError, ValueError):
            return '--'


def format_currency(amount: float) -> str:
    """Format currency."""
    return Formatters.format_currency(amount)


def format_date(date, format_str: str = '%d-%m-%Y') -> str:
    """Format date."""
    return Formatters.format_date(date, format_str)


def format_time_ago(timestamp: datetime) -> str:
    """Format time ago."""
    return Formatters.format_time_ago(timestamp)


def format_temperature(celsius: float) -> str:
    """Format temperature."""
    return Formatters.format_temperature(celsius)


def format_soil_ph(ph: float) -> str:
    """Format soil pH."""
    return Formatters.format_soil_ph(ph)

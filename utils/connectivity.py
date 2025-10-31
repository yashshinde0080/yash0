"""Internet connectivity utilities."""

import socket
import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class ConnectivityManager:
    """Manages internet connectivity checks."""

    def __init__(self):
        """Initialize connectivity manager."""
        self.is_online = False
        self._connectivity_callbacks = []

    def check_connectivity(self, timeout: int = 5) -> bool:
        """
        Check if device has internet connectivity.

        Args:
            timeout: Socket timeout in seconds

        Returns:
            True if online, False otherwise
        """
        try:
            # Try to connect to a reliable DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            if not self.is_online:
                self.is_online = True
                self._notify_connectivity_change(True)
            return True
        except (socket.timeout, socket.error, OSError):
            if self.is_online:
                self.is_online = False
                self._notify_connectivity_change(False)
            return False

    def is_connected(self) -> bool:
        """Get current connectivity status."""
        return self.is_online

    def register_callback(self, callback: Callable):
        """Register callback for connectivity changes."""
        if callback not in self._connectivity_callbacks:
            self._connectivity_callbacks.append(callback)

    def unregister_callback(self, callback: Callable):
        """Unregister callback for connectivity changes."""
        if callback in self._connectivity_callbacks:
            self._connectivity_callbacks.remove(callback)

    def _notify_connectivity_change(self, is_online: bool):
        """Notify all registered callbacks of connectivity change."""
        for callback in self._connectivity_callbacks:
            try:
                callback(is_online)
            except Exception as e:
                logger.error(f'Error in connectivity callback: {str(e)}')


# Global connectivity manager
connectivity_manager = ConnectivityManager()


def is_online(timeout: int = 5) -> bool:
    """Check if device is online."""
    return connectivity_manager.check_connectivity(timeout)


def get_connectivity_status() -> bool:
    """Get current connectivity status."""
    return connectivity_manager.is_connected()

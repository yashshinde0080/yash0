"""Offline mode management and sync coordination."""

import logging
import threading
from datetime import datetime
from typing import Callable, Optional

from database.db_manager import get_db
from database.models import UserSettings, SyncQueue
from utils.connectivity import connectivity_manager, is_online
from config.settings import CONNECTIVITY_CHECK_INTERVAL

logger = logging.getLogger(__name__)


class OfflineManager:
    """Manages offline mode and sync coordination."""

    def __init__(self):
        """Initialize offline manager."""
        self.db = get_db()
        self.is_offline = False
        self._connectivity_check_thread = None
        self._stop_checking = False
        self._callbacks = []

    def start_connectivity_monitoring(self):
        """Start background connectivity monitoring."""
        self._stop_checking = False
        self._connectivity_check_thread = threading.Thread(
            target=self._monitor_connectivity,
            daemon=True
        )
        self._connectivity_check_thread.start()
        logger.info('Started connectivity monitoring')

    def stop_connectivity_monitoring(self):
        """Stop connectivity monitoring."""
        self._stop_checking = True
        if self._connectivity_check_thread:
            self._connectivity_check_thread.join(timeout=5)
        logger.info('Stopped connectivity monitoring')

    def _monitor_connectivity(self):
        """Monitor connectivity in background."""
        import time
        while not self._stop_checking:
            try:
                was_online = not self.is_offline
                is_now_online = is_online(timeout=5)

                if was_online and not is_now_online:
                    # Went from online to offline
                    self.is_offline = True
                    logger.warning('Device went offline')
                    self._notify_connectivity_change(False)

                elif not was_online and is_now_online:
                    # Went from offline to online
                    self.is_offline = False
                    logger.info('Device came online')
                    self._notify_connectivity_change(True)

                time.sleep(CONNECTIVITY_CHECK_INTERVAL)
            except Exception as e:
                logger.error(f'Error in connectivity check: {str(e)}')
                time.sleep(60)  # Wait 60 seconds before retrying

    def is_in_offline_mode(self) -> bool:
        """Check if device is in offline mode."""
        return self.is_offline

    def enable_offline_mode(self):
        """Manually enable offline mode."""
        try:
            session = self.db.get_session()
            user = session.query(UserSettings).filter_by(id=1).first()
            if user:
                user.offline_mode = True
                session.commit()
            session.close()
            self.is_offline = True
            logger.info('Offline mode enabled')
        except Exception as e:
            logger.error(f'Error enabling offline mode: {str(e)}')

    def disable_offline_mode(self):
        """Disable manual offline mode."""
        try:
            session = self.db.get_session()
            user = session.query(UserSettings).filter_by(id=1).first()
            if user:
                user.offline_mode = False
                session.commit()
            session.close()
            self.is_offline = False
            logger.info('Offline mode disabled')
        except Exception as e:
            logger.error(f'Error disabling offline mode: {str(e)}')

    def register_sync_callback(self, callback: Callable):
        """Register callback for when device comes online."""
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def _notify_connectivity_change(self, is_online: bool):
        """Notify callbacks of connectivity change."""
        for callback in self._callbacks:
            try:
                callback(is_online)
            except Exception as e:
                logger.error(f'Error in connectivity callback: {str(e)}')

    # ==================== Sync Queue Management ====================

    def queue_for_sync(self, entity_type: str, entity_id: int, action: str, payload: dict):
        """Queue data for sync when online."""
        try:
            session = self.db.get_session()
            import json

            sync_item = SyncQueue(
                entity_type=entity_type,
                entity_id=entity_id,
                action=action,
                payload=json.dumps(payload),
                status='pending'
            )

            session.add(sync_item)
            session.commit()
            session.close()

            logger.info(f'Queued {entity_type} {entity_id} for {action} sync')
        except Exception as e:
            logger.error(f'Error queuing for sync: {str(e)}')

    def get_pending_syncs(self) -> list:
        """Get all pending sync items."""
        try:
            session = self.db.get_session()
            pending = session.query(SyncQueue).filter_by(status='pending').all()
            session.close()
            return pending
        except Exception as e:
            logger.error(f'Error getting pending syncs: {str(e)}')
            return []

    def get_failed_syncs(self) -> list:
        """Get all failed sync items."""
        try:
            session = self.db.get_session()
            failed = session.query(SyncQueue).filter_by(status='failed').all()
            session.close()
            return failed
        except Exception as e:
            logger.error(f'Error getting failed syncs: {str(e)}')
            return []

    def mark_sync_as_syncing(self, sync_id: int):
        """Mark sync item as being synced."""
        try:
            session = self.db.get_session()
            sync_item = session.query(SyncQueue).filter_by(id=sync_id).first()
            if sync_item:
                sync_item.status = 'syncing'
                session.commit()
            session.close()
        except Exception as e:
            logger.error(f'Error marking sync as syncing: {str(e)}')

    def mark_sync_as_completed(self, sync_id: int):
        """Mark sync item as completed."""
        try:
            session = self.db.get_session()
            sync_item = session.query(SyncQueue).filter_by(id=sync_id).first()
            if sync_item:
                sync_item.status = 'completed'
                sync_item.synced_at = datetime.utcnow()
                session.commit()
            session.close()
            logger.info(f'Sync {sync_id} completed')
        except Exception as e:
            logger.error(f'Error marking sync as completed: {str(e)}')

    def mark_sync_as_failed(self, sync_id: int, retry_limit: int = 3):
        """Mark sync item as failed or retry."""
        try:
            session = self.db.get_session()
            sync_item = session.query(SyncQueue).filter_by(id=sync_id).first()
            if sync_item:
                sync_item.retry_count += 1

                if sync_item.retry_count >= retry_limit:
                    sync_item.status = 'failed'
                    logger.error(f'Sync {sync_id} failed after {retry_limit} retries')
                else:
                    sync_item.status = 'pending'
                    logger.warning(f'Sync {sync_id} failed, will retry (attempt {sync_item.retry_count})')

                session.commit()
            session.close()
        except Exception as e:
            logger.error(f'Error marking sync as failed: {str(e)}')

    def clear_completed_syncs(self):
        """Delete completed sync items."""
        try:
            session = self.db.get_session()
            deleted = session.query(SyncQueue).filter_by(status='completed').delete()
            session.commit()
            session.close()
            logger.info(f'Cleared {deleted} completed sync items')
        except Exception as e:
            logger.error(f'Error clearing completed syncs: {str(e)}')

    def get_sync_stats(self) -> dict:
        """Get sync queue statistics."""
        try:
            session = self.db.get_session()
            total = session.query(SyncQueue).count()
            pending = session.query(SyncQueue).filter_by(status='pending').count()
            syncing = session.query(SyncQueue).filter_by(status='syncing').count()
            completed = session.query(SyncQueue).filter_by(status='completed').count()
            failed = session.query(SyncQueue).filter_by(status='failed').count()
            session.close()

            return {
                'total': total,
                'pending': pending,
                'syncing': syncing,
                'completed': completed,
                'failed': failed,
            }
        except Exception as e:
            logger.error(f'Error getting sync stats: {str(e)}')
            return {}


# Global offline manager instance
offline_manager = None


def get_offline_manager():
    """Get or create global offline manager."""
    global offline_manager
    if offline_manager is None:
        offline_manager = OfflineManager()
    return offline_manager

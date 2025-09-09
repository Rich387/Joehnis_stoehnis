"""Thread-safe counter with simple file persistence.
This is intentionally small and dependency-free so it can be tested independently.
"""
import json
import logging
from pathlib import Path
from threading import Lock

logger = logging.getLogger("seufz.counter")

class Counter:
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self._lock = Lock()
        self._count = 0
        self._load()

    def _load(self):
        try:
            if self.file_path.exists():
                with self.file_path.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._count = int(data.get('count', 0))
                logger.info("Loaded %s -> %s", self.file_path, self._count)
        except Exception:
            # If file is corrupted or unreadable, start from 0
            self._count = 0
            logger.exception("Failed to load counter file %s", self.file_path)

    def _save(self):
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with self.file_path.open('w', encoding='utf-8') as f:
                json.dump({'count': self._count}, f)
            logger.info("Saved %s -> %s", self.file_path, self._count)
        except Exception:
            # Best-effort persistence; ignore errors for now
            logger.exception("Failed to save counter file %s", self.file_path)
            pass

    def get(self):
        with self._lock:
            # ensure we reflect any changes written by other processes
            self._load()
            return self._count

    def increment(self):
        with self._lock:
            self._count += 1
            self._save()
            return self._count

    def decrement(self):
        with self._lock:
            self._count -= 1
            self._save()
            return self._count

    def set(self, value: int):
        with self._lock:
            self._count = int(value)
            self._save()
            return self._count

"""
rate_limiter.py - Rate limiting utility for API calls

A rate limiter to prevent exceeding API quotas:
- Tracks API calls per minute and per day
- Provides waiting functionality when limits are reached
- Returns remaining quota information

Dependencies:
- datetime
- collections

Related files: 
- src/gemini/gemini_client.py
"""

import time
import logging
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for Gemini API calls"""

    def __init__(self, max_calls_per_minute: int = 30, max_calls_per_day: int = 500):
        """
        Initialize rate limiter with default limits.

        Args:
            max_calls_per_minute: Maximum API calls per minute
            max_calls_per_day: Maximum API calls per day
        """
        self.max_calls_per_minute = max_calls_per_minute
        self.max_calls_per_day = max_calls_per_day

        # Initialize counters
        self.reset_counters()

    def reset_counters(self):
        """Reset all rate limit counters"""
        self.minute_calls = 0
        self.day_calls = 0
        self.last_minute_reset = datetime.now()
        self.last_day_reset = datetime.now()

    def update_counters(self):
        """Update counters based on elapsed time"""
        now = datetime.now()

        # Check if minute has elapsed
        if now - self.last_minute_reset > timedelta(minutes=1):
            self.minute_calls = 0
            self.last_minute_reset = now

        # Check if day has elapsed
        if now - self.last_day_reset > timedelta(days=1):
            self.day_calls = 0
            self.last_day_reset = now

    def check_and_wait(self):
        """
        Check rate limits and wait if necessary.

        Returns:
            None
        """
        self.update_counters()

        # Check if we're approaching minute limit
        if self.minute_calls >= self.max_calls_per_minute:
            wait_time = 60 - (datetime.now() - self.last_minute_reset).seconds
            logger.warning(
                f"Rate limit approaching: waiting {wait_time} seconds")
            time.sleep(wait_time + 1)  # Add 1 second buffer
            self.update_counters()  # Refresh counters after waiting

        # Check if we're approaching day limit
        if self.day_calls >= self.max_calls_per_day:
            logger.error("Daily rate limit reached, cannot proceed")
            raise Exception("Daily API rate limit reached")

        # Increment counters
        self.minute_calls += 1
        self.day_calls += 1

    def get_status(self) -> Dict[str, Any]:
        """
        Get current rate limit status.

        Returns:
            Dictionary with rate limit information
        """
        self.update_counters()

        return {
            "minute": {
                "used": self.minute_calls,
                "limit": self.max_calls_per_minute,
                "remaining": self.max_calls_per_minute - self.minute_calls,
                "resets_in_seconds": 60 - (datetime.now() - self.last_minute_reset).seconds
            },
            "day": {
                "used": self.day_calls,
                "limit": self.max_calls_per_day,
                "remaining": self.max_calls_per_day - self.day_calls,
                "resets_in_seconds": 86400 - (datetime.now() - self.last_day_reset).seconds
            }
        }

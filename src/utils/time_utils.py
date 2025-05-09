# src/utils/time_utils.py
from datetime import datetime, timezone, timedelta
import pytz
from typing import Optional, Tuple

def parse_timezone_offset(offset_str: Optional[str]) -> Tuple[int, int]:
    """
    Parse timezone offset string to hours and minutes.
    
    Args:
        offset_str: Timezone offset string (e.g., '+02:00')
        
    Returns:
        Tuple of (hours, minutes)
    """
    if not offset_str:
        return 0, 0
        
    # Handle Z (UTC) timezone
    if offset_str == 'Z':
        return 0, 0

def get_timezone(timezone_str: Optional[str]) -> timezone:
    """
    Get a timezone object from a timezone string.
    
    Args:
        timezone_str: Timezone string (e.g., 'UTC', 'Europe/Berlin', '+02:00')
        
    Returns:
        timezone object
    """
    if not timezone_str:
        return timezone.utc
        
    try:
        # Try to parse as timezone name
        return pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        # Try to parse as offset
        hours, minutes = parse_timezone_offset(timezone_str)
        return timezone(timedelta(hours=hours, minutes=minutes))

def create_timezone(timezone_str: Optional[str]) -> timezone:
    """
    Create a timezone object from a timezone string.
    
    Args:
        timezone_str: Timezone string (e.g., 'UTC', 'Europe/Berlin', '+02:00')
        
    Returns:
        timezone object
    """
    return get_timezone(timezone_str)
        
    # Parse sign
    sign = 1
    if offset_str[0] == '-':
        sign = -1
        offset_str = offset_str[1:]
    elif offset_str[0] == '+':
        offset_str = offset_str[1:]
    
    # Parse hours and minutes
    parts = offset_str.split(':')
    hours = int(parts[0]) * sign
    minutes = int(parts[1]) * sign if len(parts) > 1 else 0
    
    return hours, minutes

def create_timezone(offset_str):
    """
    Create timezone from src.offset string.
    
    Args:
        offset_str: Timezone offset string (e.g., '+02:00')
        
    Returns:
        timezone object
    """
    hours, minutes = parse_timezone_offset(offset_str)
    return timezone(timedelta(hours=hours, minutes=minutes))

def localize_timestamp(timestamp, tz_offset):
    """
    Apply timezone offset to timestamp.
    
    Args:
        timestamp: datetime object
        tz_offset: Timezone offset string (e.g., '+02:00')
        
    Returns:
        Localized datetime
    """
    tz = create_timezone(tz_offset)
    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=tz)
    else:
        return timestamp.astimezone(tz)

def utc_to_local(utc_dt, tz_offset):
    """
    Convert UTC datetime to local time.
    
    Args:
        utc_dt: UTC datetime object
        tz_offset: Timezone offset string (e.g., '+02:00')
        
    Returns:
        Local datetime
    """
    tz = create_timezone(tz_offset)
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz)

def local_to_utc(local_dt, tz_offset):
    """
    Convert local datetime to UTC.
    
    Args:
        local_dt: Local datetime object
        tz_offset: Timezone offset string (e.g., '+02:00')
        
    Returns:
        UTC datetime
    """
    tz = create_timezone(tz_offset)
    return local_dt.replace(tzinfo=tz).astimezone(timezone.utc)
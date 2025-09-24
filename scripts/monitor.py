#!/usr/bin/env python3
import requests
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_orthanc_health():
    """Check Orthanc server health"""
    try:
        response = requests.get('http://localhost:8042/system', 
                              auth=('admin', 'admin123'), timeout=5)
        if response.status_code == 200:
            logger.info("Orthanc server: OK")
            return True
        else:
            logger.error(f"Orthanc server error: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Orthanc server unreachable: {e}")
        return False

def check_database():
    """Check database connectivity"""
    try:
        response = requests.get('http://localhost:8081/api/info', timeout=5)
        if response.status_code == 200:
            logger.info("Database: OK")
            return True
        else:
            logger.error(f"Database error: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Database unreachable: {e}")
        return False

def get_system_stats():
    """Get system statistics"""
    try:
        response = requests.get('http://localhost:8042/statistics', 
                              auth=('admin', 'admin123'), timeout=5)
        if response.status_code == 200:
            stats = response.json()
            logger.info(f"Studies: {stats.get('CountStudies', 0)}, "
                       f"Series: {stats.get('CountSeries', 0)}, "
                       f"Instances: {stats.get('CountInstances', 0)}")
            return stats
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
    return None

if __name__ == "__main__":
    logger.info(f"Health check started at {datetime.now()}")
    
    orthanc_ok = check_orthanc_health()
    db_ok = check_database()
    stats = get_system_stats()
    
    if orthanc_ok and db_ok:
        logger.info("All systems operational")
    else:
        logger.error("System issues detected")

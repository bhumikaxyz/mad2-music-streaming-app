from dotenv import load_dotenv
load_dotenv()
import os



enable_utc=False
from dotenv import load_dotenv
load_dotenv()
import os

# CELERY_BROKER_URL=redis://default:X8kWly7NmJxeETDtmtsG8YZee2Bb3X1j@redis-10155.c305.ap-south-1-1.ec2.cloud.redislabs.com:10155
# CELERY_RESULT_BACKEND=redis://default:X8kWly7NmJxeETDtmtsG8YZee2Bb3X1j@redis-10155.c305.ap-south-1-1.ec2.cloud.redislabs.com:10155
# CACHE_REDIS_HOST=redis-10155.c305.ap-south-1-1.ec2.cloud.redislabs.com
# CACHE_REDIS_PORT=10155
# CACHE_REDIS_PASSWORD=X8kWly7NmJxeETDtmtsG8YZee2Bb3X1j



broker_url = os.getenv('CELERY_BROKER_URL')
result_backend = os.getenv('CELERY_RESULT_BACKEND')
timezone = "Asia/kolkata"
broker_connection_retry_on_startup=True
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

"""
    配置
"""

sender = ""
email_password = ""
receiver = ""

# crawler
AREA = "china/beijing/chaoyang-district"

try:
    from local_settings import *
except ImportError:
    pass

from celery import Celery
from django.conf import settings
import os
# 1 添加环境变量，告知Celery为哪个项目提供服务
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mm.settings')

# 2. 创建Celery对象
app = Celery('mm')

# 3. 配置(主要是任务队列)
app.conf.update(
    BROKER_URL = 'redis://@127.0.0.1:6379/1'
)
# 4. 告知Celery去应用目录下查找任务函数
app.autodiscover_tasks(settings.INSTALLED_APPS)
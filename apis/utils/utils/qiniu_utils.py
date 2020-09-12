"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/21-15:29
INSTRUCTIONS:   七牛token
"""

from qiniu import Auth, put_file
import qiniu.config
from main.settings import ACCESS_KEY, QINUI_SECRET_KEY, BUCKET_NAME

# 构建鉴权对象
q = Auth(ACCESS_KEY, QINUI_SECRET_KEY)


"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/21-15:29
INSTRUCTIONS:   七牛token
"""

from qiniu import Auth, put_file
from main.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY

# 构建鉴权对象
q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)


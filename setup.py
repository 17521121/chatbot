# pip install -r requirements.txt

import os
try:
    os.makedirs('logs')
    os.makedirs('models')
    os.makedirs('ED')
    os.makedirs('torch_pre_load')
except OSError as e:
    pass


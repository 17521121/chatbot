
import os
try:
    os.makedirs('logs')
    os.makedirs('models')
    os.makedirs('ED')
    os.makedirs('torch_pre_load')
except OSError as e:
    pass

from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 6):
    sys.exit("Sorry, Python >=3.6 is required for EmpatheticDialogues.")

setup(
    name="chatbot_camthong",
    version="1.0",
    description=(
        "Khoá luận tốt nghiệp 2021, Khoa Khoa học máy tính"
    ),
    author=("Đặng Quốc Tiến, 17521121; Phạm Thừa Tiểu Thành, 17520156"),
    url="https://arxiv.org/abs/1811.00207",
    python_requires=">=3.6",
    packages=[
        "transformers==4.0.0",
        "vncorenlp",
        "fairseq==0.10.0",
        "flask-ngrok",
        "flask_fontawesome",
        "googletrans==3.1.0a0"
    ]
)

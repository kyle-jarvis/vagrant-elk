from setuptools import setup, find_packages
from shutil import rmtree
import os

for build_dir in ['./build', './vagrant_elk_examples.egg_info']:
    if os.path.exists(build_dir):
        rmtree(build_dir)

setup(
    name="vagrant-elk-examples",
    version="1.0.0",
    author="Kyle Jarvis",
    description="Things to do in this VM",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "spark-es-demo = examples.spark_demo:cli"
            ]
        }
)

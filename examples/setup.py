from setuptools import setup, find_packages


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

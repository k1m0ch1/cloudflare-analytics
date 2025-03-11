from setuptools import setup, find_packages
import subprocess

# VERSION = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()

setup(
    name="cfmetrics",
    version="0.1.3",
    author="k1m0ch1",
    author_email="yahya.kimochi@gmail.com",
    description="Python Library for cloudflare analytics web",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/k1m0ch1/cloudflare-analytics",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
)

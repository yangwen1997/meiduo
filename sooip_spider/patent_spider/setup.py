# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='patent_spider',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy':['settings=patent_spider.settings']},
)
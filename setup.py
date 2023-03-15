# -*- coding: utf-8 -*-
#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pyaitools',
    version='1.4.8',
    description='AI tools-code!',
    url='https://github.com/AITutorials/aitools/',
    author='Stephen.Z',
    author_email='15242200221@163.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='python ai tools',
    packages = find_packages(exclude = ['MANIFEST.in']),
    include_packages_data = True
    )   

#!/usr/bin/env python

from setuptools import setup

version = open("files/version.txt").read().strip()
long_description = open("README.md").read().strip()

setup(
    name='CERBERUS PHISH',
    version=version,
    description='A python phishing script for login phishing, image phishing video phishing an many more!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='kingfonpro',
    author_email='kasroudrakrd@gmail.com',
    license="GPLv3",
    url='https://github.com/kingfonpro/CERBERUS-PHISH/',
    scripts=['cerberusphish'],
    install_requires=["requests", "bs4"]
)

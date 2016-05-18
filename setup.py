#coding: utf-8
from setuptools import setup, find_packages

setup(
    name='sdl',
    version="0.1",
    packages=find_packages(),

    install_requires = ['lxml>=3.3'],

    author='Rafał Korzeniewski',
    author_email='korzeniewski@gmail.com',
    description='Survey Domain Language - parse and serialize to some outputs',
    license = "PSF",
    url='https://github.com/rkorzen/KreaturaParser.git',
    test_suite="sdl.tests"

)
#coding: utf-8
from setuptools import setup, find_packages

setup(
    name='SDL',
    version="",
    description='Tools to build surveys and clean data. IBIS and Dimensions',
    #long_description=open('docs/manual.md').read(),
    author='Rafał Korzeniewski',
    author_email='korzeniewski@gmail.com',
    url='https://github.com/rkorzen/KreaturaParser',
    license='Copyright Rafał Korzeniewski',
    packages=find_packages(exclude=('example', )),
    include_package_data=True,
    zip_safe=True,
    setup_requires=[
        #'versiontools >= 1.6',
        #'lxml >= 3.3.5',
    ],
    classifiers=[
        'Environment :: Web Environment or desktop',
        #'Framework :: Python',
        #'Intended Audience :: Developers',
        #'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        #'Topic :: ',
        #'Topic :: Software Development :: Libraries :: Python Modules',
    ],

)
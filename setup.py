###
Setup script for sets-n-plots
###

from setuptools import setup, find_packages

readme = open('README.rst').read()
license = open('LICENSE').read()

setup(
    name='sets-n-plots',
    version='0.1.0',
    description='Statistical analysis and graph generating package',
    long_description=readme,
    author='Boris Epstein',
    author_email='borepstein@gmail.com',
    url='https://github.com/borepstein/sets-n-plots',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')
    )

from distutils.core import setup

setup(
    name='google_status',
    version=open('VERSION').read(),
    packages=['google_status',],
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
)
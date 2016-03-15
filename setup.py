"""
Flask-SenseAPI
-------------

Flask Extension for CommonSense
"""
from setuptools import setup


setup(
    name='Flask-SenseAPI',
    version='1.0',
    url='https://github.com/senseobservationsystems/flask-senseapi',
    author='Ricky Hariady',
    author_email='ricky@sense-os.nl',
    description='Flask Extension for CommonSense',
    long_description=__doc__,
    py_modules=['flask_senseapi'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'senseapi'
    ]
)
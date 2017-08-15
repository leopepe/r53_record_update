from setuptools import setup, find_packages
from r53_record_update import __version__ as version

setup(
    name='r53_record_update',
    py_modules=['r53_record_update'],
    version=version.__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['boto3'],
    url='https://github.com/leopepe/r53_record_update.git',
    license='Simplified BSD',
    author='Leonardo Pepe',
    author_email='lpepefreitas@gmail.com',
    description='App to simplify the DNS record management of ASG instances'
)



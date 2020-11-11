from pkg_resources import parse_requirements
from setuptools import find_packages, setup


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


setup(
    name='converter',
    version='0.0.1',
    author='Ivan Shaibakov',
    author_email='ivan.shaibakov@gmail.com',
    license='MIT',
    description='Конвертер валюты',
    long_description=open('README.md').read(),
    url='',
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'converter-api = converter.api.main:main',
        ]
    },
    include_package_data=True
)

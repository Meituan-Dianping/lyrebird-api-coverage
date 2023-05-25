from setuptools import setup,find_packages
import os
import runpy

here = os.path.abspath(os.path.dirname(__file__))

VERSION = runpy.run_path(
    os.path.join(here, 'lyrebird_api_coverage', 'version.py')
)['VERSION']

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lyrebird-api-coverage',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/meituan/lyrebird-api-coverage',
    author='HBQA',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ),
    entry_points={
        'lyrebird_plugin': [
            'lyrebird_api_coverage = lyrebird_api_coverage.manifest'
        ]
    },
    install_requires=[
        'lyrebird>=2.10.3',
        'jsonschema'
    ],
    extras_require={
        'dev': [
            "autopep8",
            "pylint",
            "pytest"
        ]
    }
)

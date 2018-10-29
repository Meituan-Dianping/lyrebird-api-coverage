from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lyrebird-api-coverage',
    version='0.2.4',
    packages=['lyrebird_api_coverage'],
    url='https://github.com/meituan/lyrebird-api-coverage',
    author='HBQA',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ),
    entry_points={
        'console_scripts': [
        ],
        'lyrebird_data_handler': [
            'api_coverage = lyrebird_api_coverage.proxy.proxy_handler:MyDataHandler'
        ],
        'lyrebird_web': [
            'api_coverage = lyrebird_api_coverage.app_ui:AppUI'
        ]
    },
    install_requires=[
        'lyrebird',
        'jsonschema'
    ]

)

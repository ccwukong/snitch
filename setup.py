from setuptools import setup, find_packages

setup(
    name='snitch',
    version='0.1.0',
    description='snitch is a CLI tool that helps you do health check, API contract validation and load testing agaist your microservices.',
    url='https://github.com/ccwukong/snitch',
    author='Chen Cheng',
    author_email='ccwukong@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['anyio',
                      'asyncclick',
                      'tox',
                      'coverage',
                      'aiohttp'
                      ],
    classifiers=[
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: >=3.8',
    ],
    platforms='any',
)

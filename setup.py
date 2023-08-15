from setuptools import setup
from stargazerz import __version__

setup(
    name='stargazerz',
    version=__version__,
    description='Instantly Retrieve Email Addresses and Usernames of Stargazers from Designated Repositories, Achieving Unparalleled Speed and Efficiency - All Without the Need for an API Key',
    author='Noah Kay',
    author_email='noahkay13@gmail.com',
    url='https://github.com/Frikallo/stargazerz',
    packages=['stargazerz'],
    install_requires=[
        'beautifulsoup4==4.12.2',
        'bs4==0.0.1',
        'requests==2.31.0',
        'tqdm==4.66.1',
    ],
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
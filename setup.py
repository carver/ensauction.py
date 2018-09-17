"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

extras_require = {
    'test': [
        "pytest>=3.8.0,<4",
        "pytest-mock",
        "web3[tester]>=4,<5",
    ],
    'lint': [
        "flake8>3,<4",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "pytest-xdist",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "ipython",
    ],
}

extras_require['dev'] = (
    extras_require['dev'] +
    extras_require['test'] +
    extras_require['lint']
)

setup(
    name='ensauction',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0-alpha.1',

    description='Ethereum Name Service Auction, in Python',

    # The project's main homepage.
    url='https://github.com/carver/ensauction.py',

    # Author details
    author='Jason Carver',
    author_email='ut96caarrs@snkmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Topic :: Database :: Front-Ends',
        'Topic :: Internet :: Finger',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Security :: Cryptography',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='ethereum eth web3 web3.py ENS',

    python_requires='>=3.5',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests', 'venv']),

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['web3>=4.0.0'],

    extras_require=extras_require,
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
)

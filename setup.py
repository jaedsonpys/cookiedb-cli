from setuptools import setup
from cookiedbcli import __version__

with open(f'README.md', 'r') as reader:
    readme = reader.read()

setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='cookiedb-cli',
    description='The CLI for interactive use of CookieDB. ',
    version=__version__,
    long_description_content_type='text/markdown',
    long_description=readme,
    python_requires='>=3.6',
    license='GPL',
    packages=['cookiedbcli'],
    install_requires=['cookiedb==4.2.1'],
    url='https://github.com/jaedsonpys/cookiedb-cli',
    project_urls={
        'Source code': 'https://github.com/jaedsonpys/cookiedb-cli',
        'License': 'https://github.com/jaedsonpys/cookiedb-cli/blob/master/LICENSE',
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers'
    ],
    entry_points={
        'console_scripts': [
            'cookiedb = cookiedbcli.main:main'
        ]
    },
    keywords=['database', 'cli', 'console', 'cookiedb']
)

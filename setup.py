"""
Install purpleair as a development copy by running this file
`python setup.py develop`
"""


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='purpleair',
    version='1.0.6',
    description='Python API Client to get and transform PurpleAir data.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Christopher Sardegna',
    author_email='purpleair@reagentx.net',
    url='https://github.com/ReagentX/purple_air_api/',
    packages=find_packages(),
    install_requires=['requests', 'requests_cache', 'thingspeak', 'geopy', 'pandas'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

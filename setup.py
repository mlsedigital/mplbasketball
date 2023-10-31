from setuptools import setup, find_packages

setup(
    name='mplbasketball',
    description='Basketball plotting library for use with matplotlib.',
    version='0.0.1',
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    install_requires=[
        "requests",
        "matplotlib",
        "numpy",
        "pandas",
        "setuptools"
    ]
)

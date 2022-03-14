from setuptools import setup, find_packages

setup(
    name="multitran-cli",
    version="0.1.0",
    description="Unofficial multitran.com command line interface",
    long_description=open('README.md').read(),
    author='scrapix',
    url="https://github.com/scrapix/multitran-cli",
    packages=find_packages(),
    license="License",
    scripts=["scripts/multitran-cli.py"],
    install_requires=["bs4", "requests", "colorama"]
)

from setuptools import setup, find_packages

setup(
    name="multitran_cli",
    version="0.1.1",
    description="Unofficial multitran.com command line interface",
    long_description=open('README.md').read(),
    author='scrapix',
    url="https://github.com/scrapix/multitran_cli",
    packages=find_packages(),
    license="License",
    scripts=["scripts/multitran_cli.py"],
    install_requires=["bs4", "requests", "colorama"]
)

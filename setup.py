from setuptools import setup, find_packages

setup(
    name="multitran_cli",
    extras_require=dict(tests=["pytest"]),
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    version="0.1.1",
    description="Unofficial multitran.com command line interface",
    long_description=open('README.md').read(),
    author='scrapix',
    url="https://github.com/scrapix/multitran_cli",
    license="License",
    scripts=["src/multitran/multitran_cli.py"],
    install_requires=["bs4", "requests", "colorama"],
)

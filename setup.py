from setuptools import setup, find_packages

setup(
    name="multitran_cli",
    extras_require=dict(tests=["pytest"]),
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    scripts=["src/multitran_cli/multitran.py"],
    entry_points={
        'console_scripts': ['multitran = multitran_cli.multitran:run']
    },
    install_requires=["bs4", "requests", "colorama"],
    version="0.1.2",
    description="Unofficial multitran.com command line interface",
    long_description=open('README.md').read(),
    author='scrapix',
    url="https://github.com/scrapix/multitran_cli",
    license="License"
)

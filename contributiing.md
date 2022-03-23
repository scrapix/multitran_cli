# Project Setup

### Setup Project with pytest
Let's create an editable install.
Python has projects and PyCharm does as well. In this tutorial step, let's make both, with a virtual environment, and set the project up to use pytest.

`pip install -e ".[tests]"`

### Configure Testing
Setup default test runnter
`Preferences > Tools > Python Integrated Tools > Testing > Default test runnter > pytest `

### Creating a python package for a new release
`python setup.py sdist`


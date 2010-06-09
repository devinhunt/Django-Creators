from setuptools import setup, find_packages

setup(
    name = "django-creators",
    version = "1.0",
    url = 'http://github.com/',
    license = 'Private',
    description = "The management and video server for the Vice Creators Project parties.",
    author = 'Devin Hunt',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
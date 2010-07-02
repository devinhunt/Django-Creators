from setuptools import setup, find_packages

setup(
    name = "django-creators",
    version = "0.2",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    
    # Scripts and Dependencies
    install_requires = ['setuptools',
                        'zc.buildout',
                        'zc.recipe.egg',
                        'South',
                        'simplejson',
                        ],
    
    # Author Information
    author = 'Devin Hunt',
    author_email = 'devinhunt@gmail.com',
    description = '.',
    license = 'Private',
    url = 'http://www.hailpixel.com',
)
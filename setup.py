import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'cornice',
    'pyramid_whoauth', 'mozsvc', 'limone', 'limone_zodb',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'ZODB3',
    'waitress',
    ]
test_requires = [
    "webtest",
    "pytest",
    "pytest-cov",
    "pytest-capturelog",
    ]

setup(name='organicseeds_webshop_api',
      version='0.0',
      description='organicseeds_webshop_api',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      test_suite="organicseeds_webshop_api.tests",
      extras_require=dict(
        test = test_requires, ),
      entry_points="""\
      [paste.app_factory]
      main = organicseeds_webshop_api:main
      """,
      )

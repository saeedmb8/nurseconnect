import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requires = filter(None, f.readlines())

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(name='nurseconnect',
      version=version,
      description='nurseconnect',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Praekelt Foundation',
      author_email='dev@praekelt.com',
      url='None',
      license='BSD',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      dependency_links=["https://github.com/praekelt/molo.profiles.git@feature/reset_password#egg=molo.profiles",],
      install_requires=requires,
      tests_require=requires,
      entry_points={})

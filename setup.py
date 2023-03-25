from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in education_lms/__init__.py
from education_lms import __version__ as version

setup(
	name="education_lms",
	version=version,
	description="Learning management system for erpnext education",
	author="OMar",
	author_email="lms@mail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

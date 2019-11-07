from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
	user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

	def initialize_options(self):
		TestCommand.initialize_options(self)
		self.pytest_args = list()

	def finalize_options(self):
		TestCommand.finalize_options(self)
		self.test_args = list()
		self.test_suite = True

	def run_tests(self):
		import pytest
		import sys
		errno = pytest.main(self.pytest_args)
		sys.exit(errno)

setup(
		name = 'raven',
		version = '0.2',
		description = 'Python library for communicating with a RAVEn device',
		long_description = 'Python library for communicating with a Rainforest Automation RAVEn RFA-Z106 device',
		maintainer = 'Kevin Rauwolf',
		url = 'https://github.com/squidpickles/raven',
		license = 'BSD License',
		packages = ['raven', ],
		install_requires = ['paho-mqtt', ],
		tests_require = ['pytest', 'pytest-coverage'],
		keywords = ['RAVEn', 'RFA-Z106', ],
		cmdclass = {'test': PyTest, },
		classifiers = [
			'Development Status :: 3 - Alpha',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: BSD License',
			'Natural Language :: English',
			'Programming Language :: Python :: 3',
			'Topic :: Home Automation',
			'Topic :: Software Development :: Libraries',
		],
)

from setuptools import setup

# with open('README.rst') as readme_file:
#     readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

with open("requirements.txt") as requires_file:
    requirements = requires_file.read().split("\n")

requirements = [requirement for requirement in requirements if not ("+" in requirement)]
    
test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='gravitic',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="""An abstract gravitational wave pipeline constructor.""",
    #long_description=readme + '\n\n' + history,
    author="Daniel Williams",
    author_email='daniel.williams@ligo.org',
    url='https://github.com/transientlunatic/gravitic',
    packages=['gravitic'],
    package_dir={'gravitic': 'gravitic'},
    entry_points={
        'console_scripts': [
            'gravitic=gravitic.cli:gravitic'
        ]
    },
    include_package_data=True,
    # install_requires=requirements,
    zip_safe=True,
    # keywords='supervisor, pe, ligo, asimov',
    test_suite='tests',
    tests_require=test_requirements,
)

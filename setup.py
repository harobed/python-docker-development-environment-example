import os, re

# TODO maybe migrate to http://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

v = open(os.path.join(here, 'demo_polls', '__init__.py'))
version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

setup(
    name='demo_polls',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements("requirements.txt"),
    entry_points="""
    [console_scripts]
    polls = demo_polls.cli:cli
    """
)

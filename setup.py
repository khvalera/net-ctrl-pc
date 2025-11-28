
from setuptools import setup, find_packages

setup(
    name="net-ctrl-pc",
    version="1.0.0",
    description="Net Control PC Server and Client",
    author="khvalera@ukr.net",
    author_email="khvalera@ukr.net",
    url="https://github.com/khvalera/net-ctrl-pc",
    packages=find_packages(),
    install_requires=[
        "importlib_resources==5.10.1",
        "zipp<3.0",
        "paho-mqtt>=1.5.0,<2.0",
        "PyYAML>=5.4",
    ],
    #entry_points={
    #    "console_scripts": [
    #        "ncp-server = net_ctrl_pc.server.main:main",
    #        "ncp-client = net_ctrl_pc.client.main:main",
    #    ],
    #},
    package_data={
        "net_ctrl_pc": [ "locale/**/*.*",],
        'net_ctrl_pc': ['data/*.yaml'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

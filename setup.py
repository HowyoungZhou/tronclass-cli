import setuptools

import tronclass_cli

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="tronclass-cli",
    version=tronclass_cli.__version__,
    author="Howyoung Zhou",
    author_email="howyoungzhou@yahoo.com",
    description="Command-line interface for Tronclass.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HowyoungZhou/tronclass-cli",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "tcc = tronclass_cli.__main__:main"
        ]
    },
    python_requires='>=3.5',
)

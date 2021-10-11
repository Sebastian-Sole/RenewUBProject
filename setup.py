import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RenewUB",
    version="0.0.1",
    author="Sebastian Sole & Julian Grande",
    author_email="julian@digitalvenue.no",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juliangra/RenewUB",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

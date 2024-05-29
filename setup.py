from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="prlplot",
    version="0.1.0",
    author="Abhay Deshpande",
    author_email="a.deshpande012@gmail.com",
    description="A collection of simple opinionated plotting tools for generating high-quality plots for scientific papers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/personalrobotics/PRLPlot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib>=3.0.0",
    ],
)

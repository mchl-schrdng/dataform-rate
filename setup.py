from setuptools import setup, find_packages

setup(
    name="dataform-rate",
    version="0.1.2",
    description="Simple tool to test your Dataform project",
    author="Mchl Schrdng",
    author_email="mchl.schrdng@gmail.com",
    url="https://github.com/mchl-schrdng/dataform-rate",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",  
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

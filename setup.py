from setuptools import find_packages, setup

setup(
    name="cocosplit",
    version="0.1.0",
    packages=find_packages(where="source"),  # Specify source directory
    package_dir={"": "source"},  # Tell distutils packages are under src
    install_requires=[
        "scikit-learn",
        "funcy",
        "scikit-multilearn",
    ],
    python_requires=">=3.10",
)

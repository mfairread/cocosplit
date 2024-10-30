from setuptools import setup, find_packages

setup(
    name="cocosplit",
    version="0.2.0",
    packages=find_packages(),  # Finds and includes all packages in `my_package`
    entry_points={
        'console_scripts': [
            'my-package=my_package.__main__:main',  # Creates `my-package` CLI command
        ],
    },
    python_requires='>=3.10',  # Specify the Python version compatibility
    install_requires=[],  # List your package dependencies here
)

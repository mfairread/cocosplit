from setuptools import setup, find_packages

setup(
    name="cocosplit",
    version="0.2.0",
    packages=find_packages(), 
    entry_points={
        'console_scripts': [
            'cocosplit=source.__main__:main',  
        ],
    },
    python_requires='>=3.10',  
    install_requires=[], 
)

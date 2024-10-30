from setuptools import setup, find_packages

setup(
    name="cocosplit",
    version="0.2.0",
    packages=find_packages("source"), 
    package_dir={"": "source"},
    entry_points={
        'console_scripts': [
            'cocosplit=coco_split.__main__:main',  
        ],
    },
    python_requires='>=3.10',  
    install_requires=[], 
)

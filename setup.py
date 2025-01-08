from setuptools import setup, find_packages

setup(
    name="shhhh",
    version="1.0.0-alpha1",
    packages=find_packages(),
    install_requires=[
        'pyaudio',
        'numpy',
        'pydub'
    ],
    # Altres opcions
)

from distutils.core import setup

setup(
    # Application name:
    name="Greemigration",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Kit Lee",
    author_email="wkle4993@gmail.com",

    # Packages
    packages=["gcpredict"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="planetanalytics.space",

    #
    # license="LICENSE.txt",
    description="Greemigration predicts the waiting time for the green card applications",

    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)

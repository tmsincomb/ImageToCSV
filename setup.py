#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = [
    "Click",
    "pandas",
    "opencv-python",
    "pytesseract",
    "pdftotext",
    "tabulate",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Troy Sincomb",
    author_email="troysincomb@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Converts An Image to a CSV. This exists because Chorus 3.0 are bat-shit and only show images for vital metadata.",
    entry_points={
        "console_scripts": [
            "imagetocsv=imagetocsv.cli:main",
        ],
    },
    install_requires=requirements,
    extras_require={"dev": ["pytest", "pre-commit", "twine", "wheel", "setuptools"]},
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    include_package_data=True,
    keywords="imagetocsv",
    name="imagetocsv",
    packages=find_packages(include=["imagetocsv", "imagetocsv.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tmsincomb/imagetocsv",
    version="0.1.0",
    zip_safe=False,
)

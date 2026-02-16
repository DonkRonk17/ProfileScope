#!/usr/bin/env python3
"""
Setup script for ProfileScope.

Install with:
    pip install -e .

Or:
    python setup.py install
"""

from setuptools import setup
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="profilescope",
    version="1.0.0",
    description="Python Performance Profiler with Beautiful Reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ATLAS (Team Brain)",
    author_email="logan@metaphy.dev",
    url="https://github.com/DonkRonk17/ProfileScope",
    py_modules=["profilescope"],
    python_requires=">=3.7",
    install_requires=[
        # Zero dependencies! Pure stdlib
    ],
    entry_points={
        "console_scripts": [
            "profilescope=profilescope:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: System :: Monitoring",
    ],
    keywords="profiling performance optimization python cProfile pstats bottleneck analysis",
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/ProfileScope/issues",
        "Source": "https://github.com/DonkRonk17/ProfileScope",
    },
)

"""Setup configuration for System Architecture Agent."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name="system-architect-agent",
    version="0.1.0",
    author="System Architect Agent Team",
    description="An AI-powered conversational agent for system design and architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/system-architect-agent",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "system-architect=system_architect.cli:main",
        ],
    },
    include_package_data=True,
)

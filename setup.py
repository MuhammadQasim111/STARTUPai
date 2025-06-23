#!/usr/bin/env python3
"""
Setup script for Startup AI Agent
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [line.strip() for line in requirements_path.read_text().splitlines() 
                   if line.strip() and not line.startswith("#")]

setup(
    name="startup-ai-agent",
    version="1.0.0",
    author="Muhammad Qasim",
    author_email="mqasim111786111@gmail.com",
    description="AI-powered startup analysis tool using OpenAI Agents SDK and Gemini API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/startup-ai-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Entrepreneurs",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "web": [
            "streamlit>=1.28.0",
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
        ],
        "viz": [
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
            "plotly>=5.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "startup=startup.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "startup": ["*.py", "*.md", "*.txt"],
    },
    keywords=[
        "startup",
        "ai",
        "analysis",
        "business",
        "entrepreneurship",
        "openai",
        "gemini",
        "machine-learning",
        "artificial-intelligence",
    ],
    project_urls={
        "Bug Reports": "https://github.com/your-username/startup-ai-agent/issues",
        "Source": "https://github.com/your-username/startup-ai-agent",
        "Documentation": "https://github.com/your-username/startup-ai-agent/wiki",
    },
) 
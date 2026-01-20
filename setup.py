from setuptools import setup, find_packages

setup(
    name="topsis-sachingoyal-102303557",
    version="1.0.0",
    author="Sachin Goyal",
    description="TOPSIS decision method Python package",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["numpy", "pandas"],
    entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main"
        ]
    },
    python_requires=">=3.7",
)

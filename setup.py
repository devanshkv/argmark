from setuptools import setup

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="argmark",
    version="0.3",
    packages=["argmark"],
    url="https://github.com/devanshkv/argmark",
    install_requires=required,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Devansh Agarwal",
    author_email="devansh.kv@gmail.com",
    description="Convert argparse based executable scripts to markdown documents.",
    entry_points={
        "console_scripts": [
            "argmark=argmark.argmark:main",
        ],
    },
    tests_require=["pytest", "pytest-cov"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
)

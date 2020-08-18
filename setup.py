from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="argmark",
    version="0.1",
    packages=["argmark"],
    url="https://github.com/devanshkv/argmark",
    install_requires=required,
    author="Devansh Agarwal",
    author_email="devansh.kv@gmail.com",
    description="Convert argparse based executable scripts to markdown documents.",
    entry_points={"console_scripts": ["argmark=argmark.argmark:main", ], },
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

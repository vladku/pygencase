from setuptools import setup

setup(
    name="pygencase",
    version="0.0.1",
    description="Generate 'use/test' cases",
    author="Kurovkyi Vladyslav",
    packages = ["pygencase"],

    # the following makes a plugin available to pytest
    entry_points = {
        "pytest11": [
            "name_of_plugin = pygencase.plugin",
        ]
    },

    # custom PyPI classifier for pytest plugins
    classifiers=[
        "Framework :: Pytest",
    ],
    python_requires=">=3.6",
)
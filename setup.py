from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
        name="mysqlmanager",
        version="0.0.5",
        author="CARRASCOSA, Alexandre",
        description="Personal package to manage Database from MySQL",
        long_description=page_description,
        long_description_content_type="text/markdown",
        url="https://github.com/AlexandreCarrascosa/mysql-manage-package",
        packages=find_packages(),
        install_requires=requirements,
        python_requires = ">=3.8",
        )


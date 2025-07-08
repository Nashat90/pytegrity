import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytegrity",
    version="0.1.0",
    author="Nashat Jumaah Omar",
    author_email="nashattt90@gmail.com",
    description="Well Integrity Log analysis and Visualization tool [This is a Test Release]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nashat90/flotech",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
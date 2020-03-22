import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gui-miotto",
    version="0.0.1",
    author="Gui Miotto",
    author_email="guilherme.miotto@gmail.com",
    description="Creates strutured cuboidal meshes for volumes with axial "
                "cylindrical symmetry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gui-miotto/HexMeshCylinders",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
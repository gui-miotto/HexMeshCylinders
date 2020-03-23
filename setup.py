import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HexMeshCylinders",
    version="0.0.1",
    author="Gui Miotto",
    author_email="guilherme.miotto@gmail.com",
    description="Creates structured hexahedral meshes for volumes with cylindrical "
                "symmetry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gui-miotto/HexMeshCylinders",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.7',
)
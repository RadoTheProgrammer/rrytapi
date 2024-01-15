from setuptools import setup, find_packages
#
print(find_packages())
setup(
    name='rrprettier',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        # List any dependencies your library may have
    ],
    long_description="to prettify data",
    long_description_content_type="text/markdown"
)
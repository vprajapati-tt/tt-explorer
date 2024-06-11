import setuptools

setuptools.setup(
    name="tt-adapter",  
    version="0.1",
    author="Vraj Prajapati",
    author_email="vprajapati@tenstorrent.com",
    description="Tenstorrent Adapter for Google's AI Model Explorer",
    long_description_content_type="text/markdown",
    url="https://github.com/vprajapati-tt/tt-explorer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "ai-edge-model-explorer",  # Add any dependencies required by your Python scripts
    ],
    # Add the extension module built with pybind11
) 

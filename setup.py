setup(
    name=PKG_NAME,  # Replace with your own username
    version="0.0.1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    install_requires=[
        "boto3==1.17.46",
        "botocore==1.20.46",
        "simplejson"
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "robo_cluster = robo_cluster.__main__:main"
        ]
    }
)
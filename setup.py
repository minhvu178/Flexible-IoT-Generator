from setuptools import setup, find_packages

setup(
    name="flexible-iot-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pymongo>=4.0",
        "apscheduler>=3.10",
        "python-dotenv>=1.0",
        "pydantic>=2.0",
        "pytz>=2023.3"
    ],
    entry_points={
        'console_scripts': [
            'flexible-iot-generator=src.__main__:main'
        ]
    },
    python_requires='>=3.8',
    author="Your Name",
    description="Flexible IoT data generator for simulating factory environments",
    url="https://github.com/yourusername/flexible-iot-generator"
)

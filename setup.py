from setuptools import find_packages, setup

setup(
    name="gcs_modern_data_stack",
    packages=find_packages(exclude=["gcs_modern_data_stack_tests"]),
    package_data={"gcs_modern_data_stack": ["../dbt_project/*", "../dbt_project/*/*"]},
    install_requires=[
        "dagster",
        "boto3",
        "python-dotenv",
        "dagster-airbyte",
        "dagster-dbt",
        "pandas",
        "numpy",
        "scipy",
        "dbt-core",
        "packaging<22.0",  # match dbt-core's requirement to workaround a resolution issue
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
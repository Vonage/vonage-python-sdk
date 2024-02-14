resource(name='pyproject', source='pyproject.toml')

python_distribution(
    name='vonage-utils',
    dependencies=[':pyproject'],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['https://test.pypi.org/legacy/'],
)

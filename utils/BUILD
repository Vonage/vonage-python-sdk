resource(name='pyproject', source='pyproject.toml')

python_distribution(
    name='vonage-utils',
    dependencies=[':pyproject', 'utils/src/utils'],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['https://test.pypi.org/legacy/'],
)

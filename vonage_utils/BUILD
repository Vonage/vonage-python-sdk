resource(name='pyproject', source='pyproject.toml')

file(name='readme', source='README.md')

python_distribution(
    name='vonage-utils',
    dependencies=[':pyproject', ':readme', 'vonage_utils/src/vonage_utils'],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

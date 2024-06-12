resource(name='pyproject', source='pyproject.toml')

file(name='readme', source='README.md')

python_distribution(
    name='vonage_network',
    dependencies=[':pyproject', ':readme', 'vonage_network/src/vonage_network'],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

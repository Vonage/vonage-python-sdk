resource(name='pyproject', source='pyproject.toml')

file(name='readme', source='README.md')

python_distribution(
    name='vonage',
    dependencies=[':pyproject', ':readme', 'vonage/src/vonage'],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

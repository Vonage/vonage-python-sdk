resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-numbers',
    dependencies=[
        ':pyproject',
        ':readme',
        'number_management/src/vonage_numbers',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

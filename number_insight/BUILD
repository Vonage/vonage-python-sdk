resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-number-insight',
    dependencies=[
        ':pyproject',
        ':readme',
        'number_insight/src/vonage_number_insight',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

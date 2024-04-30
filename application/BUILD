resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-application',
    dependencies=[
        ':pyproject',
        ':readme',
        'application/src/vonage_application',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

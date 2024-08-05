resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-account',
    dependencies=[
        ':pyproject',
        ':readme',
        'account/src/vonage_account',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

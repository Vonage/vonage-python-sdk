resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-users',
    dependencies=[
        ':pyproject',
        ':readme',
        'users/src/vonage_users',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

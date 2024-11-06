resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-jwt',
    dependencies=[
        ':pyproject',
        ':readme',
        'jwt/src/vonage_jwt',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

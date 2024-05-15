resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-camara-auth',
    dependencies=[
        ':pyproject',
        ':readme',
        'camara_auth/src/vonage_camara_auth',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

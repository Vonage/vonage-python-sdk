resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-network-auth',
    dependencies=[
        ':pyproject',
        ':readme',
        'network_auth/src/vonage_network_auth',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

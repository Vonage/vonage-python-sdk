resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-http-client',
    dependencies=[
        ':pyproject',
        ':readme',
        'http_client/src/vonage_http_client:http_client',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

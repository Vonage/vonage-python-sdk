resource(name='pyproject', source='pyproject.toml')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-http-client',
    dependencies=[':pyproject', 'http_client/src/http_client', 'utils/src/utils'],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['https://test.pypi.org/legacy/'],
)

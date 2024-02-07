resource(name='pyproject', source='pyproject.toml')

python_distribution(
    name='vonage-number-insight',
    dependencies=[':pyproject', 'ni2/src/ni2'],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['https://test.pypi.org/legacy/'],
)

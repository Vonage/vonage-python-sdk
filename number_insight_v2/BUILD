resource(name='pyproject', source='pyproject.toml')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-number-insight',
    dependencies=[':pyproject', 'number_insight_v2/src/number_insight_v2'],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['https://test.pypi.org/legacy/'],
)

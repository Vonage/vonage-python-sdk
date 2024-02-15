resource(name='pyproject', source='pyproject.toml')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-number-insight-v2',
    dependencies=[
        ':pyproject',
        'number_insight_v2/src/number_insight_v2',
        'utils/src/utils',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['https://test.pypi.org/legacy/'],
)

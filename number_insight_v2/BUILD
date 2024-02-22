resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-number-insight-v2',
    dependencies=[
        ':pyproject',
        ':readme',
        'number_insight_v2/src/vonage_number_insight_v2',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-identity-insights',
    dependencies=[
        ':pyproject',
        ':readme',
        'identity_insights/src/vonage_identity_insights',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

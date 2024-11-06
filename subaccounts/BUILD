resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-subaccounts',
    dependencies=[
        ':pyproject',
        ':readme',
        'subaccounts/src/vonage_subaccounts',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

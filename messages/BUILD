resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-messages',
    dependencies=[
        ':pyproject',
        ':readme',
        'messages/src/vonage_messages',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-voice',
    dependencies=[
        ':pyproject',
        ':readme',
        'voice/src/vonage_voice',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

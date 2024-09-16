resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-video',
    dependencies=[
        ':pyproject',
        ':readme',
        'video/src/vonage_video',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

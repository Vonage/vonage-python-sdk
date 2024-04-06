resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-verify-v2',
    dependencies=[
        ':pyproject',
        ':readme',
        'verify_v2/src/vonage_verify_v2',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

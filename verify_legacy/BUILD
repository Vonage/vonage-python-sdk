resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-verify',
    dependencies=[
        ':pyproject',
        ':readme',
        'verify_legacy/src/vonage_verify_legacy',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

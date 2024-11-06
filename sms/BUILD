resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-sms',
    dependencies=[
        ':pyproject',
        ':readme',
        'sms/src/vonage_sms',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

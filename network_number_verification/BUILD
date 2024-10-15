resource(name='pyproject', source='pyproject.toml')
file(name='readme', source='README.md')

files(sources=['tests/data/*'])

python_distribution(
    name='vonage-network-number-verification',
    dependencies=[
        ':pyproject',
        ':readme',
        'network_number_verification/src/vonage_network_number_verification',
    ],
    provides=python_artifact(),
    generate_setup=False,
    repositories=['@pypi'],
)

from setuptools import setup, find_packages

# packages = [
#     'cullerton.agora',
#     'cullerton.agorapi',
# ]

requires = [
    'sqlalchemy',
    'pyramid',
]

setup(
    name='cullerton.agora',
    version="0.0.1",
    packages=find_packages(),
    install_requires=requires,
    author='mike cullerton',
    author_email='michaelc@cullerton.com',
    description='A forum for ideas',
    url='https://github.com/cullerton/cullerton.agora',
    download_url='https://github.com/cullerton/agora/tarball/0.0.1',
    keywords=['academic', 'simple', 'example'],
    classifiers=[],
    entry_points="""\
    [paste.app_factory]
    main = cullerton.agorapi:main
    [console_scripts]
    initialize_agora_db = cullerton.agora.initialize_db:main
    """,
    package_data={
        '': ['*.txt', '*.rst', '*.ipynb'],
    },
)

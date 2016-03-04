from setuptools import setup

packages = [
    'agora',
    'agorapi',
]

requires = [
    'sqlalchemy',
    'pyramid',
]

setup(
    name='agora',
    version="0.2",
    packages=packages,
    install_requires=requires,
    author='mike cullerton',
    author_email='michaelc@cullerton.com',
    description='A forum for ideas',
    url='https://github.com/cullerton/agora',
    download_url='https://github.com/cullerton/agora/tarball/0.2',
    keywords=['academic', 'simple', 'example'],
    classifiers=[],
    entry_points="""\
    [paste.app_factory]
    main = agorapi:main
    [console_scripts]
    initialize_agora_db = agora.initialize_db:main
    """,
    package_data={
        '': ['*.txt', '*.rst', '*.ipynb'],
    },
)

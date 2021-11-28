from setuptools import setup

setup(
    name            = 'pykorbit',
    version         = '0.2.1',
    description     = 'python wrapper for Korbit API',
    url             = 'https://github.com/sharebook-kr/pykorbit',
    author          = 'brayden.jo, jonghun.yoo',
    author_email    = 'brayden.jo@outlook.com, jonghun.yoo@outlook.com',
    install_requires= ['requests', 'pandas', 'datetime', 'numpy', 'xlrd', 'PyJWT', 'websockets'],
    license         = 'MIT',
    packages        = ['pykorbit'],
    zip_safe        = False
)
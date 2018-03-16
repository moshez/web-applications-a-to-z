import setuptools
setuptools.setup(
packages=setuptools.find_packages() +
         ['twisted.plugins'],
install_requires=['Twisted',
                  'pyramid',
                  'sqlalchemy'],
)

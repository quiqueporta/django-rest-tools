from setuptools import setup

from django_rest_tools import get_version


setup(
    name='django-rest-tools',
    version=get_version(),
    license='GPLv3',
    author='Quique Porta',
    author_email='quiqueporta@gmail.com',
    description='Tools for Django Rest Framework',
    long_description=open('README.rst').read(),
    url='https://github.com/quiqueporta/django-rest-tools',
    download_url='https://github.com/quiqueporta/django-rest-tools/releases',
    keywords=['django', 'djangorestframework', 'tools'],
    packages=['django_rest_tools'],
    install_requires=['django', 'djangorestframework'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ],
)

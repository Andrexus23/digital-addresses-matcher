from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='digital-address-matcher',
  version='1.0.0',
  author='Andrexus23',
  description='Преобразование строки адреса в последовательность кодов КЛАДР',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.10',
  ],
  keywords='NER, address matching, KLADR',
  project_urls={
    'GitHub': 'https://github.com/Andrexus23/digital-addresses-matcher'
  },
  python_requires='>=3.10'
)
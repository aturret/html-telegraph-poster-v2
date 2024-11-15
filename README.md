[![build](https://github.com/mercuree/html-telegraph-poster/actions/workflows/python-package.yml/badge.svg)](https://github.com/mercuree/html-telegraph-poster/actions/workflows/python-package.yml)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/html-telegraph-poster?master)](https://pypi.org/project/html-telegraph-poster/)

# Python html to telegra.ph poster V2

Forked from [html-telegraph-poster](https://github.com/mercuree/html-telegraph-poster) by [mercuree](https://github.com/mercuree/).

Added async support and fixed some bugs (Because my projects need it). New features will be added soon.

Simple python function to post plain html text to https://telegra.ph/.
Telegra.ph allows `<a>, <blockquote>, <br>, <em>, <figure>, <h3>, <h4>, <img>, <p>, <strong>, ` elements.
It also supports embedded youtube and vimeo iframe tags.

About telegram telegra.ph service https://telegram.org/blog/instant-view

## Installation
```Shell
pip install html-telegraph-poster-v2
```

## Usage

```python
>> > from html_telegraph_poster_v2 import TelegraphPoster
>> > t = TelegraphPoster(use_api=True)
>> > t.create_api_token('Elon Musk', 'Elon', 'https://www.spacex.com/')  # second and third params are optional
{'access_token': '9f3bab568f*************', 'auth_url': 'https://edit.telegra.ph/auth/HFYo***********',
 'author_name': 'Elon', 'short_name': 'Elon Musk', 'author_url': 'https://www.spacex.com/'}
>> > t.post(title='Just another funny joke', author='by me', text='<blockquote>Really hard way</blockquote>')
{'path': 'Just-another-funny-joke-06-05-4', 'url': 'http://telegra.ph/Just-another-funny-joke-06-05-4'}
```
##### Use graph.org instead of telegra.ph
```python
>>> t = TelegraphPoster(use_api=True, telegraph_api_url='https://api.graph.org')
```
##### We can modify this article later:
```python
>>> t.edit(text=t.text + '<p>some text at the end</p>')
{'path': 'Just-another-funny-joke-06-05-4', 'url': 'http://telegra.ph/Just-another-funny-joke-06-05-4'}
```
##### Modify page created earlier:
```python
>>> t.edit(text="<p>new text</p>", path='/Another-one-page-06-05')
{'path': 'Another-one-page-06-05', 'url': 'http://telegra.ph/Another-one-page-06-05'}
```

## Generate persistent access token
Actually it's a good idea to generate access token and put it inside environment variables.
This command will generate .env file or append  TELEGRAPH_ACCESS_TOKEN at the end of it.
Note: script will not set environment variable. You can use [python-dotenv](https://github.com/theskumar/python-dotenv),
set it manually or hardcode it when call `TelegraphPoster(access_token='access_token_string')`
```Shell
python -m html_telegraph_poster_v2.create_account "Elon Musk" "Elon" "https://www.spacex.com/"
```

## Uploading images

Since telegra.ph is not support media uploading anymore, you can configure an image/video storage service.

Current supported services:

- AWS S3
- GitHub

```
## Utils module
Utils module provides ability to make some pre-process steps before document is passed to the converter.
#### Uploading all images to the telegra.ph

```python
from html_telegraph_poster_v2.utils import DocumentPreprocessor

dp = DocumentPreprocessor(html_string)
dp.upload_all_images()
dp.get_processed_html()  # this should return html string with uploaded and replaced image urls
```
Optionally you can pass base_url if the document contains images with relative paths
```python
dp.upload_all_images(base_url='https://example.com')
dp.get_processed_html() 
``` 

## Roadmap

- [ ] rewrite the command line interface for simple usage
- [ ] add automated test pipeline
- [ ] add more services for media uploading
  - [ ] imgur
  - [ ] google drive
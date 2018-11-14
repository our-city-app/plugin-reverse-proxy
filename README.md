# Reverse proxy plugin

Simple plugin for use with https://github.com/our-city-app/gae-plugin-framework


## Setup

Example configuration.json file:

```json
{
  "app_title": "Reverse proxy",
  "languages": [
    "en"
  ],
  "plugins": [
    {
      "name": "interactive_explorer",
      "order": 42,
      "version": "master",
      "url": "https://github.com/our-city-app/plugin-interactive-explorer.git"
    },
    {
      "name": "reverse_proxy",
      "order": 6,
      "version": "master",
      "url": "https://github.com/our-city-app/plugin-reverse-proxy.git"
    }
  ]
}
```


## Usage

Create a 'ProxyPath' datastore model:

```python
def run():
    from plugins.reverse_proxy.models import ProxyPath
    ProxyPath(key=ProxyPath.create_key('test'), url='https://2bfb58ed.eu.ngrok.io').put()
```
 
Going to https://your-app-id.appspot.com/proxy/test/abc will proxy to https://2bfb58ed.eu.ngrok.io/abc


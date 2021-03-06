es-graphite-shim 
================

[![Stories in Ready](https://badge.waffle.io/distributed-system-analysis/es-graphite-shim.png?label=ready&title=Ready)](https://waffle.io/distributed-system-analysis/es-graphite-shim)

### DESCRIPTION

[ElasticSearch as a timeseries Data source for Grafana](https://github.com/grafana/grafana/issues/1034):
There has been an ongoing discussion about this and ELK is a very useful stack indeed.
Hence, we came up with this shim, which does just that, by mocking Graphite instance API,
pipelining data from ElasticSearch, for Grafana.

### INSTALLATION

- Build the Dockerfile included here for containerized solution. Instructions
  for building and starting the container, are included in the Dockerfile.
  Before that, make sure you have copied `conf/local_settings_example.py` into
  `conf/local_settings.py` and edited the params as required. 

- For a real machine deployment, refer to `INSTALL-NOTES` ,
  
- Make sure you supply the params to config.js in grafana accordingly. Refer below:
```js
..
// Graphite & Elasticsearch example setup

datasources: {
  graphite: {
  type: 'graphite',
  url: "<URL of shim>",
  timezone: 'Asia/Kolkata',
 },
elasticsearch: {
  type: 'elasticsearch',
  url: "<ES Instance where dashboard metadata is to be stored>",
  index: 'grafana-dash',
  grafanaDB: true,
 }
},

..
```

The `timezone` option under `datasources.graphite` has to be mentioned
in case the timezone offsets differ. This normally has to be same as the
one mentioned under `local_settings.py` (change this line: `TIME_ZONE` = '')

### USAGE

To run this in development mode, just like any other
django project would be executed.

``` $ python manage.py runserver ```

Or, you might deploy this on a production server using nginx sample config file,
included with the source code, under ```conf/egs.conf.example```. '

Following that, on homepage, you will see some sample links.

There are two categories of the shim API, as follows:

1. __Render Query Type__: Here, the metric_path is a DOT (.) separated path (similar to graphite) that specifies
    the path of the query metrics, as per the hierarchy. This may be:

  - Format: ```/render/?target={{metric_path}}&from={{epoch_from}}&until={{epoch_until}}&format=json```

    ..where _metric_path_ is: ```metric1.sub_metric1.sub_sub_metric1. <and so on>```

  - The ```from=``` and ```until=``` fields specify the time durations between which the query
    is to be performed.

  - ```format=json``` ensures the response is JSON formatted.

  - Please note, for demonstration purposes, a sample query has been provided in the homepage
    HTML file. The params provided to it, come from within the views.py file under
    ```homepage(request)```. You could modify the query path and epoch intervals accordingly.

2. __Metric Search Query Type__: Here, when * is given, all the parent nodes in the metric path hierarchy are displayed as a result, along with information like, whether its a leaf node or not.

  - Format: ```/metrics/find?query=*```


## Is there a place to track current and future work items?
Yes, we are using GitHub Issues and Pull Requests managed via
[Waffle.io](https://waffle.io/distributed-system-analysis/es-graphite-shim) for that.


## Is there a mailing list for discussions?
Yes, [Google Groups](https://groups.google.com/forum/#!forum/es-graphite-shim)

### LICENSE
Refer to the file 'LICENSE'.

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/arcolife/es-graphite-shim/trend.png)](https://bitdeli.com/free "Bitdeli Badge")


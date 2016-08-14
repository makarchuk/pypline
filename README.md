# pypline
Lightweighg flexible pipeline inspired by logstash

This library intend to simplify creation of flexible and efficient logstash-like-pipelines.
It uses same inputs-filters-outputs approach. Each plugni is just a class which implement api and you can easily create you own filter if you want to. 

Config file actually is just python file which specify inpust, filters and outputs for pipeline and than call for a start of said pipeline
you can see example in `config.py`. 

Library is not production-ready yet, but i plan to make it usable and stable in not-so-distant future.

If you have any questions, ideas or advices about my poor designing - please create an issue.

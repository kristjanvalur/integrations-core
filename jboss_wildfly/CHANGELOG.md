# CHANGELOG - JBoss/WildFly

## 2.0.2 / 2023-07-10

***Fixed***:

* Bump Python version from py3.8 to py3.9. See [#14701](https://github.com/DataDog/integrations-core/pull/14701).

## 2.0.1 / 2022-04-05 / Agent 7.36.0

***Fixed***: 

* Remove check options from jmx template. See [#11686](https://github.com/DataDog/integrations-core/pull/11686).


## 2.0.0 / 2022-02-19 / Agent 7.35.0

***Changed***: 

* Correct metric_type for wildfly metrics. See [#8706](https://github.com/DataDog/integrations-core/pull/8706). Thanks [codylerum](https://github.com/codylerum).

***Added***: 

* Add `pyproject.toml` file. See [#11375](https://github.com/DataDog/integrations-core/pull/11375).

***Fixed***: 

* Fix namespace packaging on Python 2. See [#11532](https://github.com/DataDog/integrations-core/pull/11532).


## 1.7.2 / 2022-01-08 / Agent 7.34.0

***Fixed***: 

* Bump base check dependency. See [#10926](https://github.com/DataDog/integrations-core/pull/10926).
* Add comment to autogenerated model files. See [#10945](https://github.com/DataDog/integrations-core/pull/10945).


## 1.7.1 / 2021-11-13 / Agent 7.33.0

***Fixed***: 

* Fix description of JMX options. See [#10454](https://github.com/DataDog/integrations-core/pull/10454).


## 1.7.0 / 2021-10-04 / Agent 7.32.0

***Added***: 

* Add runtime configuration validation. See [#8940](https://github.com/DataDog/integrations-core/pull/8940).

***Fixed***: 

* Add server as generic tag. See [#10100](https://github.com/DataDog/integrations-core/pull/10100).


## 1.6.0 / 2021-07-12 / Agent 7.30.0

***Added***: 

* Enable `new_gc_metrics` JMX config option for new installations. See [#9501](https://github.com/DataDog/integrations-core/pull/9501).


## 1.5.2 / 2021-05-28 / Agent 7.29.0

***Fixed***: 

* Fix defaults for `collect_default_metrics` JMX config option. See [#9441](https://github.com/DataDog/integrations-core/pull/9441).
* Fix JMX config spec. See [#9364](https://github.com/DataDog/integrations-core/pull/9364).


## 1.5.1 / 2021-03-07 / Agent 7.27.0

***Fixed***: 

* Bump minimum base package version. See [#8443](https://github.com/DataDog/integrations-core/pull/8443).


## 1.5.0 / 2020-12-11 / Agent 7.25.0

***Added***: 

* Document new collect_default_jvm_metrics flag for JMXFetch integrations. See [#8153](https://github.com/DataDog/integrations-core/pull/8153).


## 1.4.0 / 2020-10-31 / Agent 7.24.0

***Added***: 

* Add missing custom_jar_paths option to config. See [#7809](https://github.com/DataDog/integrations-core/pull/7809).
* [doc] Add encoding in log config sample. See [#7708](https://github.com/DataDog/integrations-core/pull/7708).


## 1.3.3 / 2020-09-21 / Agent 7.23.0

***Fixed***: 

* Use consistent formatting for boolean values. See [#7405](https://github.com/DataDog/integrations-core/pull/7405).


## 1.3.2 / 2020-08-10 / Agent 7.22.0

***Fixed***: 

* Update logs config service field to optional. See [#7209](https://github.com/DataDog/integrations-core/pull/7209).
* Add new_gc_metrics to all jmx integrations. See [#7073](https://github.com/DataDog/integrations-core/pull/7073).


## 1.3.1 / 2020-06-29 / Agent 7.21.0

***Fixed***: 

* Assert new jvm metrics. See [#6996](https://github.com/DataDog/integrations-core/pull/6996).
* Fix template specs typos. See [#6912](https://github.com/DataDog/integrations-core/pull/6912).
* Adjust jmxfetch config. See [#6864](https://github.com/DataDog/integrations-core/pull/6864).


## 1.3.0 / 2020-05-17 / Agent 7.20.0

***Added***: 

* Allow optional dependency installation for all checks. See [#6589](https://github.com/DataDog/integrations-core/pull/6589).
* Add rmi_connection_timeout & rmi_client_timeout to config spec. See [#6459](https://github.com/DataDog/integrations-core/pull/6459).
* Add default template to openmetrics & jmx config. See [#6328](https://github.com/DataDog/integrations-core/pull/6328).


## 1.2.0 / 2020-04-04 / Agent 7.19.0

***Added***: 

* Fix service check name and add config spec. See [#6225](https://github.com/DataDog/integrations-core/pull/6225).

***Fixed***: 

* Remove logs sourcecategory. See [#6121](https://github.com/DataDog/integrations-core/pull/6121).
* Various doc fixes. See [#5944](https://github.com/DataDog/integrations-core/pull/5944).


## 1.1.1 / 2019-12-02 / Agent 7.16.0

***Fixed***: 

* Update example config to require `username` and `password`. See [#4445](https://github.com/DataDog/integrations-core/pull/4445).


## 1.1.0 / 2019-06-18 / Agent 6.13.0

***Added***: 

* Add log setup and configuration. See [#3672](https://github.com/DataDog/integrations-core/pull/3672).


## 1.0.0 / 2019-03-29 / Agent 6.11.0

***Added***: 

* JBoss/WildFly JMX Integration. See [#3320](https://github.com/DataDog/integrations-core/pull/3320).


# Changelog for the Thoth Naming Service

## [0.5.0] - 2018-Jun-12 - goern

### Added

Set resource limits of BuildConfig and Deployment to reasonable values, this will prevent unpredicted behavior on UpShift.

## [0.4.0] - 2018-05-01 - goern

### Added

Exporting per method, per endpoint Prometheus Metrics.

## [0.3.0] - 2018-04-28 - goern

### Added

The solver API is now querying OpenShift ImageStream API to get a list of images that carry the label _component=solver_.

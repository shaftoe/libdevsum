# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.1.1] - 2017-01-16
### Changed
- Validator.command_available now accepts the `abort` boolean parameter, will make it throw an `IOError` exception if command is not found or not executable.
- Now pytest tries to help keeping the changelog up to date looking for mismatch between __version__ and first entry with changelog data.

## [0.1.0] - 2017-01-13
### Added
- this changelog file to keep track of changes
- `libdevsum.__version__` to ease understanding what version is in use, for example when shipped in an AWS Lambda function

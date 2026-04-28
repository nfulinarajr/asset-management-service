# Asset Management Service
A simple full-stack asset management and validation service for ingesting, validating,
and tracking versioned digital assets.

## The Goal
The goal of this project is to build a small, lightweight, asset validation service to
do the following:
* Load asset metadata from a sample JSON file
* Validate assets using an extensible validation pipeline
* Store validated assets in a persistence layer
* Expose a simple API for querying assets
* Maintain integrity through meaningful unit tests

## The Approach
My validation pipeline approach for this project is focusing on classic design patterns,
highlighting extensibility, composability, and clear separation of goals!

To achieve this, my thought was to create modular components in the form of individual
`pipelines` that each define a list of `rules`, leaving the `ValidationPipeline` to
validate what it is being provided.

The `ValidationPipeline` is a generic container that validates any subject of a generic
type, *T*, as defined within each `Rule`. My goal here was to keep the validation as
generic as possible. The `ValidationPipeline` has a single responsibility of validating
a rule and reporting any errors it encounters.

Now, what is a `Rule`? They are simply single-responsibility classes that *actually*
perform the validation, which conforms to a `Rule[T]` Protocol. For this approach, the
`Rule` Protocol states that a `Rule` must implement a `validate(self, subject: T)`
method that returns `list[ValidationError]`, which is just a list of custom validation
errors. I was keeping scalability in mind, allowing teams to create as many rules as
they see fit without modifying existing code.

With so many rules, how do we organize them all? Enter the `pipeline`! It's this complex
system...kidding, it really is just a simple "factory" to determine which rules belong
to which pipeline. This promotes reusability since different teams can use existing
rules and add them to different pipelines. It also makes testing really simple, as can
be seen within the unit tests.

## The Functional Requirements
Data should be validated against the following asset data models

**Asset Rules and Schema**
* Uniqueness is described by its `name` and `type`
* Multiple assets with the same `name` and `type` combination are **not** allowed
* Each asset should be associated with at least **1** version

|Field         |Type   |Notes                                               |
|--------------|-------|----------------------------------------------------|
|Name          |`str`  |Required                                            |
|Type          |`enum` |character, prop, set, environment, vehicle, dressing|

**Version Rules and Schema**
* Uniqueness is described by its `asset`, `department`, and `version_number`
* Versions should increment linearly by integers

|Field         |Type             |Notes                                               |
|--------------|-----------------|----------------------------------------------------|
|Asset         |`foreign_key`    |Reference to the asset this version represents      |
|Department    |`str`            |modeling, texturing, rigging, animation, cfx, fx    |
|Version Number|`int`            |Greater than or equal to 1                          |
|Status        |`enum`           |active, inactive.                                   |

### Validation Pipeline
**Rules:**
* `Name` is required
* `Type` is a known and valid value
* `Department` is required
* `Version Number` is an integer greater than or equal to 1
* `Status` is a known and valid value

### Storage
With all this data, it needs to be stored somewhere! For this project, I opted to
implement a SQLite database. It has been quite a while since I implemented one so I
thought this would be a fun exercise to get reacquainted. I have it set up so that if a
file is not provided for a data store, it will default to an in-memory database.

### Python API
* `load_assets(json_file.json)`:
	* Loads assets and version data from a `JSON` file
* `add_asset(asset)`:
	* Adds an asset to the data store
	* Accepts an `Asset`
* `add_version(asset, version)`:
	* Adds a version to the data store
	* Accepts an `Asset` and `Version`
* `list_assets()`:
	* List all assets within the data store
* `list_versions(asset_name)`:
	* List all versions corresponding to the provided asset name
	* Accepts an asset name of type `str`
* `get_asset(asset_name)`:
	* Get an asset corresponding to the provided asset name
	* Accepts an asset name of type `str`
* `get_version(asset_name, version_number)`:
	* Get a version corresponding to the provided asset name and version number
	* Accepts an asset name of type `str` and a version number of type `int`

### CLI
A **C**command **L**ine **I**nterface is available if you prefer. To use it, simply
follow the following steps:
* Navigate to  `/asset-management-service`
* Execute the command `python ./bin/asset_management_service`
* You should see the following menu:
```
************************
Asset Management Service
************************

Welcome to the Asset Management Service!

This is a simple Asset and Version API

What would you like to do?

1. Load assets
2. Add asset
3. Add version
4. Get asset
5. Get version
6. List assets
7. List versions
8. Exit
```

## TODO:
* Add a React front-end
* Use JSON/YAML to automatically load and configure validation rules
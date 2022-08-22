## [0.6.0] - 2022-08-22

### Additions

- Add support for inserting SVGs inline, without writing files

### Refactors

- Unify the codeblock-formatting API under `execution.format_codeblock`
- Rewrite & refactor most of the plugin to be more maintainable
- Refactor the Python API so that the `termage` function is called by the CLI, not the other way around.

<!-- HATCH README END -->


## [0.5.0] - 2022-08-16

### Additions

- Support inserting unhandled plugin arguments into formatted markdown
- Add `--run` argument


## [0.4.0] - 2022-08-13

### Additions

- Inject `termage` mock-module into execution namespace to allow manipulating the
  terminal instance.

### Bugfixes

- Fix the target width used for line-breaking not updating per `_write` call
- Fix `title` parameter defaulting (and showing) `None`


## [0.3.2] - 2022-08-11

### Bugfixes

- Fix various issues caused by migration to Hatch that broke the MkDocs plugin.


## [0.3.1] - 2022-08-11

### Bugfixes

- Fix PyPi README being incorrect


## [0.3.0] - 2022-08-11

### Additions

- Support using global MkDocs configuration
- Add `chrome` CLI switch
- Export all `execution` functions, as well as a wrapper for the CLI, `termage`

### Refactors

- Move to `Hatch` build system


## [0.2.0] - 2022-05-26

### Refactors

- Rewrite the entire program to provide a standalone module, with CLI and MkDocs plugin bindings.


## [0.1.0] - 2022-05-25

- Initial version



<!-- HATCH URI DEFINITIONS START -->
[0.6.0]: https://github.com/bczsalba/termage/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/bczsalba/termage/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/bczsalba/termage/compare/0.3.2...0.4.0
[0.3.2]: https://github.com/bczsalba/termage/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/bczsalba/termage/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/bczsalba/termage/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/bczsalba/termage/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/bczsalba/termage/tree/v0.1.0

The `termage` MkDocs plugin lets you generate your documentation's SVGs every time you build it.

This has some advantages:

- Your screenshots will always remain up to date

    !!! note ""
        I know from personal experience how draining it can be to go through all images in your documentaition, see if they need to be replaced, re-create the original screenshot with the right settings & size and upload it to your site. `Termage` simplifies this by basically doing all of that for you, _every time_ your docs need to be updated.

- You are always going to test some parts of your function.

    !!! note ""
        Some errors, even in well-traversed codepaths may be very hard to catch. By putting your raw output _straight into_ your documentation, you ensure that as many people see it as possible. This hugely increases the chance of finding issues that no one would have reported for weeks.

- You have a good opportunity to write some visual example code!

    !!! note ""
        The easiest way to work with the plugin is to keep a set of source code files, and use the `include` option to display them on the page. By doing so, you offer some really good "getting started" material to newcomers to your project, and _ensure_ that it is fully functional!


## Set up

In order to use the plugin, you need to enable the following built-in markdown extensions:

```yaml title="mkdocs.yaml"
markdown_extensions:
  - attr_list
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
```

Additionally, you must also activate the plugin:

``` yaml title="mkdocs.yaml"
plugins:
  - termage:
      # Default config options
      write_files: False
      inline_styles: True
      name_template: "termage_{count}.svg"
      path: "assets"
      background: "#212121"
      foreground: "#dddddd"
      tabs: ["Python", "Output"]
      chrome: True
      width: 0
      height: 4
```

!!! warning
    Make sure to put this plugin in front of any other markdown pre-processors. This helps cut down on unintended, and hard to debug behaviour.


## Usage

The plugin will look for the syntax:

````
\```termage(-svg) option=value option=value...
{code}
```
````


All possible options can be found on their [page](options.md).

There are 2 directives possible:

- `termage <options>`:
    Generates a tabbed layout, with one tab for the Python source, and the other for the SVG output.

    ??? note "Example"
        ````
        \```termage title=Tabbed\ layout include=docs/src/source.py
        ```
        ````

        ```termage title=Tabbed\ layout include=docs/src/source.py
        ```

- `termage-svg <options>`:
    Generates only the output SVG, without the tabbed layout.

    ??? note "Example"
        ````
        \```termage-svg title=Tabbed\ layout include=docs/src/source.py
        ```
        ````

        ```termage-svg title=Tabbed\ layout include=docs/src/source.py
        ```

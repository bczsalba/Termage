## MkDocs plugin config options

Other than the ones listed below, the MkDocs plugin exposes a couple of configuration options.

### `write_files`

Write files during generation, instead of inserting their contents directly into the HTML.

!!! warning ""

    This setting, when used during `mkdocs serve`, can and likely will cause infinite reload-loops at the first file change. This is due to `assets/` (the default path) being watched by MkDocs' livereload implementation, so every time the docs regenerate, we generate SVGs which then triggers another reload.

    The only way I've found around this issue was by allowing inline SVG insertions, though it shoulnd't be a problem if you don't use `serve` or run it with `--no-livereload`.

**Default**: `False`

### `inline_styles`

<!-- TODO: Add reference link when available -->
Controls the PyTermGUI SVG export option of the same name. When set, element styles will be applied as `style=` attributes, instead of as classes defined earlier in the export.

**Default**: `True`

### `path`

Sets the path that output files will be written to. This path must be relative to `docs/`, NOT to the root of the repository.

**Requires**: `#!py3 write_files == True`

**Default**: `assets/`

### `name_template`


Controls the template string used to generate filenames. Templated variables available are:

- `count`: The generation-index of the given SVG
- `title`: The title passed as an option of the SVG.

!!! warning
    Since `title` may be empty, you should always include `count` in your template to avoid filename overlaps (and lost files).


**Requires**: `#!py3 write_files == True`

**Default**: `termage_{count}.svg`


## General (Python & MkDocs) options

Regardless of your entrypoint, the options available are going to be the same.


### Include

Includes a file within a codeblock. The file path must originate from the same directory as `mkdocs.yml`.

For example, let's say we have the following structure:

```
mkdocs.yml
docs/
    index.md 
    src/
        intro01.py
        intro02.py
```

To include `intro01.py` into a Termage block within `index.md`, you could use:

````
\```termage include=docs/src/intro01.py
print("Code from the original codeblock is retained!")
```
````

!!! info
    The `include` option will always "prefix" the actual codeblock's value with whatever is included.

    As such, if `docs/src/intro01.py` had the content:

    ```python3
    print("Included text will always preface the real value of a codeblock")
    ```

    Termage will parse the block as:

    ````markdown
    \```termage <options>
    print("Included text will always preface the real value of a codeblock")
    print("Code from the original codeblock is retained!")
    ```
    ````


### Hide lines

The plugin has a special bit of syntax to signify `Run this line of code, but don't display it`. It is denoted by prefacing any hidden line with an ampersand (&):

!!! note ""

    ```` title="Source"
    \```termage title=Hidden\ lines
    &from pytermgui.pretty import print

    print(locals())
    ```
    ````

    ```termage title=Hidden\ lines
    &from pytermgui.pretty import print

    print(locals())
    ```



### Width and Height

Sets the terminal's dimension of the given axis. Must be given an integer, which will be taken as a character-count.

=== "`width=50` `height=10`"

    ```termage-svg include=docs/src/dimension_demo.py width=50 height=10
    ```

=== "`width=100` `height=20`"

    ```termage-svg include=docs/src/dimension_demo.py width=100 height=20
    ```

!!! info
    If no dimensions are provided, they default to (80, 24).



### Foreground & Background

Modifies the terminal's default colors. `foreground` is used for all non-styled text, and background is used as both the background to the terminal's contents as well as the window that it emulates.

=== "Default"

    ```termage-svg
    print("Hello")
    ```

=== "`foreground=green` `background=#DDDDDD`"

    ```termage-svg foreground=green background=#DDDDDD
    print("Hello")
    ```

!!! info
    Foreground defaults to __#DDDDDD__, and background defaults to __#212121__.


### Tabs

Sets the text labels of each of the tabs.

Accepts two values, delimited by a single `,`. The first value is used for the Python code, and the second is used for the SVG output.

=== "Default"

    ```termage include=docs/src/dimension_demo.py
    ```

=== "`tabs=Code,SVG`"

    ```termage include=docs/src/dimension_demo.py tabs=Code,SVG
    ```

### Title

Sets the title at the top of the output terminal.

!!! warning
    When using the plugin, make sure to escape any spaces present in your title!

    For example, instead of `title=My title`, or `title="My title"` use `title=My\ Title`.

=== "Default"

    ```termage-svg include=docs/src/dimension_demo.py
    ```

=== "`title=My\ fancy\ title`"

    ```termage-svg title=My\ fancy\ title include=docs/src/dimension_demo.py 
    ```

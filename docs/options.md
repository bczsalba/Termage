The format used by the plugin is the following:

````markdown
\```termage option=value ...
{python_code}
```
````

As all options are read as strings, there are some conversion that are done. **Digits** are turned into integers, and **`,` delimited strings** are turned into tuples.

!!! note "Using spaces"
    Strings may include space chars (" ") in them, but the spaces **must** be escaped:

    === "Bad"
        ```
        termage title=My Title
        ```

    === "Good"
        ```
        termage title=My\ Title
        ```

!!! info
    Currently, options can only be set on a per-block basis. This is subject to change.


## Hiding lines

By default, all lines within a `termage` block will be executed and shown in the `Python` tab. If you want to _execute_ a line, but not have it show up in the source code, you can prepend it using an ampersand (`&`):

```termage title=Hidden\ lines
&from pytermgui.pretty import print

# We are using the PTG print function, but that's not visible in the output
print(locals())
```

## Include

Includes a file within the codeblock. The file path's "origin" is wherever `mkdocs` runs from, which is usually the project root.

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


## Width & height

Sets the output terminal's dimensions, in characters.


=== "`width=50` `height=10`"

    ```termage-svg include=docs/src/dimension_demo.py width=50 height=10
    ```

=== "`width=100` `height=20`"

    ```termage-svg include=docs/src/dimension_demo.py width=100 height=20
    ```

!!! note
    If no dimensions are provided, Termage will use the golden standard (80, 20) dimension tuple.


## Foreground & background

Sets the output terminal's default colors.

Foreground will be used for any unstyled text. Background will be used for the titlebar and body of the "window".

=== "Default"

    ```termage-svg
    print("Hello")
    ```

=== "`foreground=green` `background=#DDDDDD`"

    ```termage-svg foreground=green background=#DDDDDD
    print("Hello")
    ```

!!! note
    Foreground defaults to __#DDDDDD__, and background defaults to __#212121__.


## Tabs

Sets the text labels of each of the tabs.

Accepts two values, delimited by a single `,`. The first value is used for the Python code, and the second is used for the SVG output.

=== "Default"

    ```termage include=docs/src/dimension_demo.py
    ```

=== "`tabs=Code,SVG`"

    ```termage include=docs/src/dimension_demo.py tabs=Code,SVG
    ```

## Title

Sets the title at the top of the output terminal.

!!! warning
    If your title includes a space, make sure to escape it!

    For example, instead of `title=My title`, or `title="My title"` use `title=My\ Title`.

=== "Default"

    ```termage-svg include=docs/src/dimension_demo.py
    ```

=== "`title=My\ fancy\ title`"

    ```termage-svg title=My\ fancy\ title include=docs/src/dimension_demo.py 
    ```

The Termage CLI offers a quick and customizable way to export SVGs from your terminal.

## Usage

You simply call `termage` with some code, and provide [options](options.md) to customize the output. By default, the output file will be printed to STDOUT, but you can export directly to a file using the `-o` flag.

`Termage` also accepts having code piped to it; this sets the `code` argument to `-`, which will cause it to read from STDIN.

## Showcase

```python3 title="source.py"

--8<--
docs/src/source.py
--8<--

```

### Syntax highlighting

=== "Code output"
    ```
    termage docs/source.py --title="Welcome to the Termage CLI!"
    ```


    ```termage-svg include=docs/src/source.py title=Welcome\ to\ the\ Termage\ CLI! height=12
    ```

=== "Code highlighting"
    ```
    termage source.py --title="Welcome to the Termage CLI!" --highlight
    ```


    ```termage-svg include=docs/src/source.py title=Welcome\ to\ the\ Termage\ CLI! highlight=1 height=10
    ```



There are times when you don't need to show the code behind a screenshot. We offer the special declaration `termage-svg` to return the SVG file without the tabbed layout.

All arguments and behaviour is shared between `termage` and `termage-svg`, with the exception of the difference in layout.

```termage-svg title=Straight\ to\ SVG! height=15
from pytermgui.pretty import print

print(locals())
```

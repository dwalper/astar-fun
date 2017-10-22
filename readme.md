# A* fun ft. MVC v0.1

This is a fun (for some definition of fun) interactive demonstration of the A* pathfinding algorithm in action. I used MVC to keep things clean. The shortest path to the goal is shown on-screen as a red line. You can move the little dude using your keyboard's arrow keys, or click to add walls, and the path will automatically update to reflect the new position/obstacles.

Word of warning - there's currently no collision detection, so you can walk through walls or right off the map (which will cause an index error, not to mention shake your infallible conviction that the earth is a sphere*).

## Getting Started

I started this project using Pygame for graphics, only to become insanely frustrated at its limitations. Pyglet has great documentation and lets you get a taste for OpenGL's API.

### Prerequisites

This was tested on Python 3.6. The only non-standard dependency is pyglet, a pretty sweet OpenGL wrapper for Python. It's much faster than pygame, though much more "bare metal" as it were - you have to use the OpenGL API to draw lines, for example.

To install pyglet, just:

```
pip install pyglet
say "oink oink oink" # mac only
```


## License

This project is licensed under the MIT License. Go nuts.

* Oblate spheroid. Whatever.

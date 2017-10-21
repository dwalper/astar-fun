# A* fun

This is a fun interactive demonstration of the A* pathfinding algorithm in action. The shortest path to the goal is shown on-screen as a red line. You can move the little dude using your keyboard's arrow keys, or click to add walls, and the path will automatically update to reflect the new position/obstacles.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

I started this project using Pygame for graphics, only to become insanely frustrated at its limitations. Pyglet has great documentation and lets you get a taste for OpenGL's API.

### Prerequisites

This was tested on Python 3.6. The only non-standard dependency is pyglet, a pretty sweet OpenGL wrapper for Python. It's much faster than pygame, though much more "bare metal" as it were - you have to use the OpenGL API to draw lines, for example. Cocos2D extends pyglet and provides additional gaming functionality, although it's probably one of the worst-documented libraries I've yet come across so I've avoided using it.

To install pyglet, just:

```
pip install pyglet
```


## License

This project is licensed under the MIT License. Go nuts.

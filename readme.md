# A* fun ft. MVC v0.1

This is a fun (for some definition of fun) interactive demonstration of the A* pathfinding algorithm in action. I implemented the algorithm from scratch using linked lists to get a better intuition for how it works, and I used MVC to keep things clean. The shortest path to the goal is shown on-screen as a red line. You can move the little dude using your keyboard's arrow keys, or click to add walls, and the path will automatically update to reflect the new position/obstacles.

Word of warning - there's currently no collision detection, so you can walk through walls or right off the map (which will cause an index error, not to mention shake your infallible conviction that the earth is a sphere*).

### Prerequisites

This was tested on Python 3.6. The only non-standard dependency is pyglet, a pretty sweet OpenGL wrapper for Python. It's much faster than pygame, though much more "bare metal" as it were - you have to use the OpenGL API to draw lines, for example.

This probably won't work properly in Python 2.x.

To install pyglet, just:

```
pip install pyglet
say "oink oink oink" # mac only
```

### Installation

Just clone this repo on your local machine:

```
git clone https://github.com/dwalper/astar-fun.git
```

## License

This project is licensed under the MIT License.



\* Oblate spheroid. Whatever.

# Spaceship-TickTockNetworks

![image](https://github.com/Ronaldzzzzz/Spaceship-TickTockNetworks/blob/main/doc/image.gif)

[Demo Video - YouTube](https://youtu.be/YRqH1x5lAp0)

This is the initial interview project from Tick Tock Networks.
In this project, you will build a spaceship dodging game in terminal.

* Use the terminal as the game screen and the keyboard as controller.
* Generate obstacles (e.g., '-' in demo) in random locations.
* Control the spaceship (e.g., '*' in demo) to dodge the obstacles.
* Check if the spaceship hits the obstacles (e.g., 'x' in demo).
* Finally, provide a score for how the player performs (e.g., in demo we count how many rows the spaceship crossed).

## Instructions

Using arrow key() to control the spaceship and dodge the obstacle as many as you can!

| Keys | Move                         |
| ---- | ---------------------------- |
| `←`  | Move Left                    |
| `→`  | Move Right                   |
| `q`  | Quit game                    |
| `r`  | Restart game(when game over) |

### Installation

This project is written by `Python 3` and use the follow library. Make sure it is installed.

#### Prerequisites

```bash
pip3 install windows-curses, argparse
```

Or using the pre-build version if you are using Windows platform.

#### Pre-build

Download the zip file from release.

### Start Game

#### Source Code

<pre>
python3 main.py <i>[--HELP] [--HEIGHT] number [--WIDTH] number [--DIFFICULTY] number</i>
</pre>

#### Pre-build (Windows)

Execute `.exe` file on a terminal or PowerShell.

<pre>
C:\Users\Ronald> main.exe <i>[--HELP] [--HEIGHT] number [--WIDTH] number [--DIFFICULTY] number</i>
</pre>

#### Arguments

| Command           | Description                                                     | Usage             |
| ----------------- | --------------------------------------------------------------- | ----------------- |
| `--HELP`| Print description and usage                                     | `main.exe --HELP` |
| `--height`        | Set the height of the game (must greater than 7) (default = 24) | `--height 24`     |
| `--width`         | Set the width of the game (must greater than 65) (default = 80) | `--width 80`     |
| `--difficulty`    | Difficuly of the game (between 1-10) (default = 1)              | `--difficulty 1`  |

#### Scoring

When the spaceship pass a line, you can get the score. The more difficult, the more score. The higher difficulty will increase the dropping speed. At `--difficulty 1`, you will get `1` point when pass a line, `--difficulty 2` will get `2`, and so on.

## Reference

[ascii_racer](https://github.com/UpGado/ascii_racer) - UpGado

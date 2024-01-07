# FROGGER

## Requirements:

- python (`>3.8`)
  - Ubuntu 20.04 LTS is the oldest Ubuntu supported for this game
- GNU/Linux OS (it might work in MacOS or Windows, but hasn't been tested)
- Your user should be in `input` and `tty` groups (or you can run the script as sudo). After adding them, remember to reboot your machine. Add those groups to the user executing:

```console
$ sudo usermod -aG tty,input $USER
```

## How to run:

1. Create a venv: `python -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install the reqs: `pip install -r requirements.txt`
4. Run the game: `python src/main.py`

## Instructions:

- You can move the frog with the arrows (or, alternatively, `WASD`)
- Press `q` to quit the game

# VideoToAscii
A simple program that plays videos on the terminal.

## Installation
In order to use the program, you'll have to install opencv on your computer. You can install opencv by running the following command:

```bash
pip install opencv-python
```

opencv package link: [opencv-python](https://pypi.org/project/opencv-python/)

You can then download and run `VideoToAscii.py` from this [github repository](https://github.com/AhmadElshiltawi/VideoToAscii/).

## Usage
```bash
python3 VideoToAscii <path-to-video> [-i] [-w frame-width-size]
```
-i: Inverts the colour scale of the ascii characters
-w: Changes the width of each from of a video. The number specified is in pixels. The height of each frame will be calculated to keep the ratio of the original frame.
## Showcase
![](https://github.com/AhmadElshiltawi/VideoToAscii/blob/main/Documents/maxwell.gif)
[Original video](https://www.youtube.com/watch?v=kOG0_qjKWEI)

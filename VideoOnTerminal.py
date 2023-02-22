import math
import sys
import cv2
import os
import time


class VideoToAscii:
    def __init__(self, video_path, reverse=False):
        # Create images folder
        if not os.path.exists('./frames'):
            os.makedirs('frames')
        else:
            for file in os.listdir('./frames'):
                os.remove(os.path.join('./frames', file))

        # Ascii variables
        self.ascii_characters = list(" .:-=+*#%@")
        self.ascii_length = len(self.ascii_characters)

        # Reverse ascii characters if needed
        if reverse:
            self.ascii_characters = self.ascii_characters[::-1]

        # Current frame variables
        self.current_frame_path = ""
        self.current_frame_count = 0

        # Current image object
        self.current_image = None

        # Video frame directory
        self.image_path = './frames'

        self.video_finished = False

        # Video object
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    # Close all windows
    def clean_up_frame(self):
        cv2.destroyAllWindows()
        if os.path.exists(self.current_frame_path):
            os.remove(self.current_frame_path)

    # Resize a frame to accommodate for the terminal's size. Default is a width of 100 pixels
    def resize(self, new_width=100):
        old_height, old_width, _ = self.current_image.shape

        # Calculate the new height
        new_height = int((new_width * old_height) / old_width)

        # Update current image
        self.current_image = cv2.resize(self.current_image, (new_width, new_height))

    # Save the next frame of the video
    def save_next_frame(self):
        # If the video finished, exit out of the function
        if self.video_finished:
            return

        # Read a frame from the video
        ret, frame = self.video.read()

        # If a frame exists, save it
        if ret:
            # Save the path of the frame
            self.current_frame_path = self.image_path + f"/frame_{str(self.current_frame_count)}.jpg"

            # Save the frame
            cv2.imwrite(self.current_frame_path, frame)

            self.current_frame_count += 1
            self.current_image = cv2.imread(self.current_frame_path)

        else:
            self.video_finished = True

    # Convert a frame into ascii characters
    def convert_to_ascii(self):
        ascii_image = ""

        self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)

        image_width, image_height = self.current_image.shape

        for row_index in range(image_width):
            for column_index in range(image_height):
                pixel_value = self.current_image[row_index, column_index]
                pixel_index = math.floor(pixel_value / (256 / self.ascii_length))
                ascii_image += self.ascii_characters[pixel_index]
            ascii_image += '\n'

        return ascii_image


# Clears the terminal screen
def clear_screen():
    print("\033c", end="")

if __name__ == "__main__":

    # Argument checking
    if not 2 <= len(sys.argv) <= 5:
        print("Usage: python3 VideoToAscii path to video [-i] [-w pixel width size]")
        exit(1)

    video_path = sys.argv[1]

    # Program parameters
    resize_pixel_width = 100
    invert_ascii = False

    if len(sys.argv) > 2:
        for i in (n + 2 for n in range(len(sys.argv[2:]))):
            if sys.argv[i].lower() == '-i':
                invert_ascii = True
                continue

            if sys.argv[i].lower() == '-w' and (len(sys.argv[2:]) != i - 1 and sys.argv[i + 1].isnumeric()):
                resize_pixel_width = int(sys.argv[i + 1])
                continue

            if sys.argv[i].isnumeric() and (sys.argv[i - 1] == '-w'):
                continue

            print('Usage: python3 VideoToAscii path to video [-i] [-w pixel width size]')
            exit(1)

    if resize_pixel_width > 1000:
        raise Exception("The pixel width given is too big!")

    if not os.path.isfile(video_path):
        raise Exception("A file with the specified path does not exist!")

    # Create a video to ascii object
    video_to_ascii = VideoToAscii(video_path, invert_ascii)

    while True:
        # Save next frame
        video_to_ascii.save_next_frame()

        # If the video is finished, the break out of loop
        if video_to_ascii.video_finished:
            break

        # Resize the frame
        video_to_ascii.resize(resize_pixel_width)

        # Print the frame in ascii
        print(video_to_ascii.convert_to_ascii())

        # Sleep for 0.0333 seconds. This results in a 30 frames per second animation
        time.sleep(0.0333)

        # Close all windows to prepare for next cycle
        video_to_ascii.clean_up_frame()

        # Clear the terminal
        clear_screen()
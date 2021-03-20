import subprocess
import cv2

def get_lines(path):
    cp = subprocess.Popen(
        "EmoFaceModel.exe " + path,
        shell=True,
        stdout=subprocess.PIPE
    )

    result_output = False

    while True:
        output = cp.stdout.readline()
        line = output.decode("utf-8")

        if line.startswith("---"):
            result_output = not result_output
            continue

        if line and result_output:
            yield line.replace("\n", "")
        if not line and cp.poll() is not None:
            break

fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
video = cv2.VideoWriter("video.mp4", fourcc, 3.0, (1280, 720))

for i in range(3):
    video.write(cv2.imread("sample.png"))
video.release()

for line in get_lines("video.mp4"):
    print(line)
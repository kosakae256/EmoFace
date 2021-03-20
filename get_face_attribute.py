import subprocess
import cv2
import os

def get_face_attribute(path):
    def get_lines(path):
        cp = subprocess.Popen(
            "EmoFaceModel.exe " + path,
            shell=True,
            stdout=subprocess.PIPE
        )

        result_output = False

        count = 0

        while True:
            if count >= 2:
                break

            output = cp.stdout.readline()
            line = output.decode("utf-8")

            if line.startswith("---"):
                result_output = not result_output
                count += 1
                continue

            if line and result_output:
                yield line.replace("\n", "")
            if not line and cp.poll() is not None:
                break

    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    video = cv2.VideoWriter("tmp.mp4", fourcc, 8.0, (1280, 720))

    for i in range(8):
        video.write(cv2.imread(path))
    video.release()

    data = {}

    for line in get_lines("tmp.mp4"):
        if line.startswith("image_quality"):
            data["image_quality"] = float(line.split(":")[1][1:])

        elif line.startswith("age"):
            data["age"] = int(line.split(":")[1][1:])

        elif line.startswith("gender"):
            data["gender"] = int(line.split(":")[1][1:])

        elif line.startswith("is_mask"):
            data["is_mask"] = int(line.split(":")[1][1:])

        elif line.startswith("glasses"):
            data["glasses"] = int(line.split(":")[1][1:])

        elif line.startswith("is_beard"):
            data["is_beard"] = int(line.split(":")[1][1:])

        elif line.startswith("charm_score"):
            data["charm_score"] = int(line.split(":")[1][1:])

        elif line.startswith("other_count"):
            data["other_count"] = int(line.split(":")[1][1:])

        elif line.startswith("is_positive"):
            data["is_positive"] = int(line.split(":")[1][1:])

        elif line.startswith("is_neutral"):
            data["is_neutral"] = int(line.split(":")[1][1:])

        elif line.startswith("is_negative"):
            data["is_negative"] = int(line.split(":")[1][1:])

        elif line.startswith("smile_score"):
            data["smile_score"] = int(line.split(":")[1][1:])

    # 生成するのに必要な仮ビデオファイルを削除
    os.remove("tmp.mp4")
    return data
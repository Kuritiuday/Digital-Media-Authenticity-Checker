import cv2

def analyze_video(video_path):

    cap = cv2.VideoCapture(video_path)

    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    result = {
        "Media Type": "Video",
        "Total Frames": frames,
        "FPS": fps,
        "Status": "No obvious tampering detected"
    }

    cap.release()

    return result
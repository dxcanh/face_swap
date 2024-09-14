import glob
import time
import shutil
import insightface
import warnings
from insightface.app import FaceAnalysis
import cv2
import logging
import tempfile
import gradio as gr
from gradio import Video
from moviepy.editor import VideoFileClip, ImageSequenceClip
import os
from gfpgan import GFPGANer  # Import the GFPGAN model

assert insightface.__version__ >= '0.7'

# Ignore specific warnings
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Initialize the FaceAnalysis app and swapper
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model('buffalo_l/inswapper_128.onnx')

# Initialize GFPGAN
gfpgan_model = GFPGANer(
    model_path='buffalo_l/GFPGANv1.4.pth',  
    upscale=1,  
    arch='clean',
    channel_multiplier=2,
    device='cuda'  # Use GPU for processing
)

def load_and_validate_source_image(source_file):
    img_source = cv2.imread(source_file)
    if img_source is None:
        raise ValueError(f"Could not read source image: {source_file}")

    faces_source = app.get(img_source)
    if len(faces_source) != 1:
        raise ValueError(f"Source image should have exactly one face: {source_file}")

    return faces_source

def break_video_into_frames(destination_file, temp_dir):
    clip = VideoFileClip(destination_file)
    clip.write_images_sequence(f'{temp_dir}/%04d.png')
    clip.close()  # Close the clip after it's no longer needed

    frames = glob.glob(f'{temp_dir}/*.png')
    frames.sort()
    return frames

def process_frames(frames, faces_source, temp_dir):
    for frame_path in frames:
        try:
            img_frame = cv2.imread(frame_path)
            if img_frame is None:
                raise ValueError(f"Could not read frame: {frame_path}")

            faces_frame = app.get(img_frame)
            res = img_frame.copy()
            for idx, face in enumerate(faces_frame):
                res = swapper.get(res, face, faces_source[0], paste_back=True)

            # Enhance the image using GFPGAN
            _, _, enhanced_img = gfpgan_model.enhance(res, has_aligned=False, only_center_face=False, paste_back=True)

            # Overwrite the original frame with the face-swapped and enhanced version
            cv2.imwrite(frame_path, enhanced_img)
            logging.info(f"Face swapping and enhancement completed for frame: {frame_path}")
        except Exception as e:
            logging.error(f"Error processing faces: {e}")
            raise ValueError("Error processing faces!") from e

def reassemble_video(frames, destination_file, temp_dir):
    clip = VideoFileClip(destination_file)
    fps = clip.fps

    # Convert frames to a list of file names
    frames = [f'{temp_dir}/{i:04d}.png' for i in range(len(frames))]

    new_clip = ImageSequenceClip(frames, fps=fps)
    new_clip = new_clip.set_audio(clip.audio)  # Keep the original audio
    output_file = f'images/output/video/output_{int(time.time())}.mp4'
    new_clip.write_videofile(output_file)
    new_clip.close()  # Close the new clip after it's no longer needed
    clip.close()  # Close the clip after it's no longer needed

    return output_file

def process_faces(source_file, destination_file):
    try:
        faces_source = load_and_validate_source_image(source_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            frames = break_video_into_frames(destination_file, temp_dir)
            if frames is None:
                return None
            process_frames(frames, faces_source, temp_dir)
            output_file = reassemble_video(frames, destination_file, temp_dir)
            return output_file
    except Exception as e:
        logging.error(f"Error processing faces: {e}")
        return None, None

def img2video(source_image, destination_video):
    source_file_path = "images/source/source.jpg"
    cv2.imwrite(source_file_path, source_image)

    # Print the original filename
    print(f"Original filename: {destination_video}")

    # Change the extension back to .mp4 if necessary
    if not destination_video.endswith(".mp4"):
        new_name = destination_video.rsplit(".", 1)[0] + ".mp4"
        os.rename(destination_video, new_name)
        destination_video = new_name

    destination_file_path = "images/destination/destination.mp4"
    destination_file_path = destination_file_path.replace("\\", "/")
    shutil.copy(destination_video, destination_file_path)

    # Delete the original file after copying
    os.remove(destination_video)

    output_file = process_faces(source_file_path, destination_file_path)

    return output_file
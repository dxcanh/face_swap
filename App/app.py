import gradio as gr
from App.faceswap_img import img2img
from App.faceswap_video import img2video

# image
img2img = gr.Interface(fn=img2img,
                       inputs=[gr.inputs.Image(label="Source Image", type="filepath"),
                               gr.inputs.Image(label="Destination Image", type="filepath"),
                               gr.inputs.Radio(["Real-ESRGAN"], label="Enhancement Method")],
                       outputs=gr.outputs.Image(label="Output Image Gallery", type="numpy"),
                       title="Face Swap Img2Img",
                       description="Swap faces between two images")

# video
img2video = gr.Interface(fn=img2video,
                         inputs= [gr.inputs.Image(label="Source Image"),
                                  gr.inputs.Video(label="Destination Video")],
                         outputs=[gr.outputs.Video(label="Output Video")],
                         title="Face Swap Video Img2MP4 Deepfake",
                         description="Swap faces from a source image into a .mp4 file",
                         capture_session=True
)
demo = gr.TabbedInterface([img2img, img2video], ["Image", "Video"])

demo.launch(server_name="0.0.0.0", server_port=5000, debug=False)

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

model_id = "/data/stable-diffusion-2-1"
cartoon_model = "/data/stableModel/manmaru.safetensors"

system_prompt = ',for children book, cartoon style, high quality'

class PicGenerator:
    def __init__(self):
        # self.pipe = StableDiffusionPipeline.from_pretrained(
        #     model_id, torch_dtype=torch.float16
        # )
        self.pipe = StableDiffusionPipeline.from_single_file(cartoon_model)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config)
        self.pipe = self.pipe.to("cuda")

    def generate(self, prompt):
        image = self.pipe(prompt + system_prompt, height=512, width=768).images[0]
        return image
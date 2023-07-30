import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

model_id = "/data/stable-diffusion-2-1"

class PicGenerator:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16
        )
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe = self.pipe.to("cuda")

    def generate(self, prompt):
        image = self.pipe(prompt).images[0]
        return image

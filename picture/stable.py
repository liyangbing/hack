import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

model_id = "/data/stable-diffusion-2-1"

system_prompt = ', for chidren'


class PicGenerator:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16
        )
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config)
        self.pipe = self.pipe.to("cuda")

    def generate(self, prompt):
        image = self.pipe(prompt + system_prompt, height=512, width=768).images[0]
        return image


picGenerator = PicGenerator()
image = picGenerator.generate(
    "A forest with tall trees. for chidren,Size: 1024x1024")
image.save("astronaut_rides_horse.png")

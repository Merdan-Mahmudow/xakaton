# import torch
# from diffusers import StableDiffusionInpaintPipeline
# pipe = StableDiffusionInpaintPipeline.from_pretrained(
#     "stabilityai/stable-diffusion-2-inpainting",
#     torch_dtype=torch.float16,
# )
# pipe.to("cuda")
# prompt = "Face of a yellow cat, high resolution, sitting on a park bench"

# image = pipe(prompt=prompt, image=image, mask_image=mask_image).images[0]
# image.save("./yellow_cat_on_park_bench.png")


# import torch
# from diffusers import StableDiffusionXLImg2ImgPipeline
# from diffusers.utils import load_image

# pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
#     "stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
# )
# pipe = pipe.to("cuda")
# url = "https://huggingface.co/datasets/patrickvonplaten/images/resolve/main/aa_xl/000000009.png"

# init_image = load_image(url).convert("RGB")
# prompt = "a photo of an astronaut riding a horse on mars"
# image = pipe(prompt, image=init_image).images
# image.save("./astronaut_rides_horse.png")

from gradio_client import Client

client = Client("stabilityai/stable-diffusion-3.5-large")
result = client.predict(
		prompt="Hello!!",
		negative_prompt="Hello!!",
		seed=0,
		randomize_seed=True,
		width=1024,
		height=1024,
		guidance_scale=4.5,
		num_inference_steps=40,
		api_name="/infer"
)
print(result)
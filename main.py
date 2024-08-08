from PIL import Image

img_url = "monro.jpg"
offset = 50

image = Image.open(img_url)
image_init_red, image_init_green, image_init_blue = image.split()

image_left_red = image_init_red.crop(
    (offset, 0, image_init_red.width, image_init_red.height))
image_mid_red = image_init_red.crop(
    (offset / 2, 0, image_init_red.width - offset / 2, image_init_red.height))
image_red = Image.blend(image_left_red, image_mid_red, 0.4)

image_left_blue = image_init_blue.crop(
    (0, 0, image_init_blue.width - offset, image_init_blue.height))
image_mid_blue = image_init_blue.crop(
    (offset / 2, 0, image_init_blue.width - offset / 2,
     image_init_blue.height))
image_blue = Image.blend(image_left_blue, image_mid_blue, 0.4)

image_green = image_init_green.crop(
    (offset / 2, 0, image_init_green.width - offset / 2,
     image_init_green.height))

image_final = Image.merge("RGB", (image_red, image_green, image_blue))
image_final.save("final.jpg")
image_final.thumbnail((80, 80))
image_final.save("final_icon.jpg")

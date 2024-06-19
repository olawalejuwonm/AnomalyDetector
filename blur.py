from PIL import Image, ImageFilter

before = Image.open("auto.png")
after = before.filter(ImageFilter.FIND_EDGES)
after.save("out.png")
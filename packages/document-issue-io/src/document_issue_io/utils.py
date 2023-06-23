from PIL import Image


def make_disclaimer_spacer(fdir):
    width = 546
    height = 48

    img = Image.new(mode="RGB", size=(width, height), color="white")
    path = fdir / "disclaimer_spacer.png"
    img.save(path)
    return path

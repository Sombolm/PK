import random

from PIL import Image

class VisualSecret:
    def __init__(self):
        self.whitePatterns = [
                (0, 255, 0, 255),
                (255,0, 255, 0),
        ]

        self.blackPatterns = [
                (0, 255, 255, 0),
                (255, 0, 0, 255),
        ]

    def encrypt(self, imagePath):

        def saveShares(share1, share2):
            share1.save("share1.png")
            share2.save("share2.png")

        def splitPixel(x,y, image, share1, share2):

            def putPixels(x, y, pattern, share1, share2):
                share1.putpixel((x * 2, y), pattern[0])
                share1.putpixel((x * 2 + 1, y), pattern[1])
                share2.putpixel((x * 2, y), pattern[2])
                share2.putpixel((x * 2 + 1, y), pattern[3])

            pixel = image.getpixel((x, y))

            pattern = random.choice(self.blackPatterns) if pixel == 255 else random.choice(self.whitePatterns)
            putPixels(x, y, pattern, share1, share2)

        image = Image.open(imagePath)
        image = image.convert("1")
        share1 = Image.new("1", (image.width * 2, image.height))
        share2 = Image.new("1", (image.width * 2, image.height))

        for x in range(image.width):
            for y in range(image.height):
                splitPixel(x, y, image, share1, share2)

        saveShares(share1, share2)

        return "share1.png", "share2.png"

    def overlayShares(self, share1, share2):

        share1 = Image.open(share1)
        share2 = Image.open(share2)

        combined = Image.new("1", (share1.width, share1.height))
        for x in range(share1.width):
            for y in range(share1.height):
                pixel1 = share1.getpixel((x, y))
                pixel2 = share2.getpixel((x, y))
                combined.putpixel((x, y), pixel1 ^ pixel2)

        combined.save("combined.png")

def main():

    visualSecret = VisualSecret()
    share1, share2 = visualSecret.encrypt("ghost.png")
    visualSecret.overlayShares(share1, share2)

if __name__ == "__main__":
    main()
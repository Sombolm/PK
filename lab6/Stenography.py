from PIL import Image

class Stenography:

    def __init__(self):
        pass

    def embedMessage(self, message: str, imagePath: str, outputPath: str):
        def messageToBinary(message: str) -> str:
            return ''.join(format(byte, '08b') for byte in message.encode('utf-8'))


        image = Image.open(imagePath)
        image = image.convert("RGB")
        binaryMessage = messageToBinary("Start" + message + "End")

        if len(binaryMessage) > image.width * image.height * 3:
            raise ValueError("Message is too long to embed in the image.")

        bitIndex = 0
        for y in range(image.height):
            for x in range(image.width):
                if bitIndex >= len(binaryMessage):
                    break

                r, g, b = image.getpixel((x, y))

                r = (r & ~1) | int(binaryMessage[bitIndex])
                g = (g & ~1) | int(binaryMessage[bitIndex + 1])
                b = (b & ~1) | int(binaryMessage[bitIndex + 2])

                image.putpixel((x, y), (r, g, b))
                bitIndex += 3

        image.save(outputPath)

    def extractMessage(self, imagePath: str) -> str:
        def messageFromBinary(binaryMessage: str) -> str:
            binaryMessage = binaryMessage[:len(binaryMessage) - (len(binaryMessage) % 8)]

            byteArray = bytearray()
            for i in range(0, len(binaryMessage), 8):
                byte = binaryMessage[i:i + 8]
                byteArray.append(int(byte, 2))

            return byteArray.decode('utf-8', errors='ignore')

        image = Image.open(imagePath)
        image = image.convert("RGB")
        binaryMessage = ""

        for i in range(image.width * image.height):
            pixel = image.getpixel((i % image.width, i // image.width))
            r, g, b = pixel

            binaryMessage += str(r & 1)
            binaryMessage += str(g & 1)
            binaryMessage += str(b & 1)

        readableMessage = messageFromBinary(binaryMessage)
        return readableMessage

def main():

    stenography = Stenography()

    stenography.embedMessage("Hello, World!", "ghost.png", "out.png")
    message = stenography.extractMessage("out.png")
    print(message)

if __name__ == "__main__":
    main()
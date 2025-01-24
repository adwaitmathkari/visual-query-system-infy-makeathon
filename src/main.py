import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def main():
    image = Image.open("/home/adwait/myFolder/visualQuerySystem/PSData/basic-flowchart1.png")
    
    text1 = pytesseract.image_to_string(image)

    print(text1)

    print("-------------------------------------------------")

    processed_image = preprocess_image("/home/adwait/myFolder/visualQuerySystem/PSData/basic-flowchart1.png")
    text2 = pytesseract.image_to_string(processed_image)

    print(text2)

    # bw_image = image.convert("L")

    # # Save the black-and-white image
    # bw_image.save("black_and_white_image.jpg")
    # text2 = pytesseract.image_to_string(bw_image)
    # print(text2)
    


def preprocess_image(image_path):
    # Open the image with PIL
    image = Image.open(image_path)
    
    # Convert to grayscale
    image = image.convert("L")  # Grayscale mode

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast by a factor of 2

    # Apply a filter to sharpen the image
    image = image.filter(ImageFilter.SHARPEN)

    image.save("high_contrast_image.jpg")
    
    return image

if __name__ == "__main__":
    main()
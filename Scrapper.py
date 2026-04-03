import requests as request
#import string 
import re 

def ScrapeWebpage(url):
    webResponse = request.get(url)

    #Check if the webpage is responding and accessible
    if webResponse.status_code != 200:
        print("Error while connecting to the webpage! Status code: " + str(webResponse.status_code))
        return

    print("Scrapping webpage...")

    html = webResponse.text
    pattern1 = r">\d+<" #regex pattern to find all numeric coordinates
    pattern2 = r"█|░" #regex pattern to collect all pixel values
    pixelCoordinates = re.findall(pattern1, html) #Find all pixel coordinates, storing them in an array as strings, in order provided. Formated as ">X<" and ">Y<"
    pixelValues = re.findall(pattern2, html) #Finds all pixel values, storing them in an array, in order provided
    drawGrid = []
    maxXIndex = 0
    maxYIndex = 0
    secretCode = ""

    #Remove the ">" and "<" characters and convert all pixel coordinates from strings to integers
    for rawCordIndex in range(0, len(pixelCoordinates)):
        pixelCoordinates[rawCordIndex] = int(pixelCoordinates[rawCordIndex].replace("<", "").replace(">", ""))

    print("Webpage scrapped successfully! Processing data now...")

    #Find the maximum X and Y coordinates to determine the required dimension of the draw grid
    for cordIndex in range(0, int(len(pixelCoordinates)/2)):
        if pixelCoordinates[cordIndex*2+1] > maxYIndex:
            maxYIndex = pixelCoordinates[cordIndex*2+1]

        if pixelCoordinates[cordIndex*2] > maxXIndex:
            maxXIndex = pixelCoordinates[cordIndex*2]


    #Initialize the draw grid with empty spaces, with dimensions based on the maximum X and Y coordinates found above
    drawGrid = [[" " for _ in range(maxXIndex + 1)] for _ in range(maxYIndex + 1)]

    #Using each pair of x and y coordinates, write the corresponding pixel value to the draw grid at those coordinates.
    for cordIndex in range(0, int(len(pixelCoordinates)/2)):
        x = pixelCoordinates[cordIndex*2]
        y = pixelCoordinates[cordIndex*2+1]
        if (0 <= y < len(drawGrid)) and (0 <= x < len(drawGrid[0])):
            drawGrid[y][x] = pixelValues[cordIndex]
        else:
            print(f"Error: Coordinates out of bounds, skipping coordinate value ({x}, {y}) with pixel value(\"{pixelValues[cordIndex]}\")")

    #Convert the draw grid into a multiline string, with each row being one line. Done to make the secret code easier to read when printed
    for drawColumn in drawGrid:
        for pixel in drawColumn:
            secretCode += pixel
        secretCode += "\n"

    print("Secret code found!\n\nPrinting Secret Code...")
    print(secretCode)
    return(secretCode)


ScrapeWebpage("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")
#HCWIDBO
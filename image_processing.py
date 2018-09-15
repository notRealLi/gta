import cv2
import numpy as np

def process_image(image):
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=150, threshold2=200) # TODO: learn; tweak min and max
    processed_image = cv2.GaussianBlur(processed_image, (3,3), 0)
    
    vertices = np.array([[0,600], 
                         #[180,470], [620,470], 
                         [800,600], [800,250], [570,200], [230,200], [0,250]])
    processed_image = religion_of_interest(image=processed_image, vertices=[vertices])

    lines = cv2.HoughLinesP(image=processed_image, rho=1, theta=np.pi/180, threshold=180, minLineLength=170, maxLineGap=5)
    try:
        for line in lines:
            coords = line[0]
            if abs((coords[3]-coords[1])/(coords[2]-coords[0])) > 0.3:
                cv2.line(processed_image, (coords[0], coords[1]), (coords[2], coords[3]), 255, 3)
    except Exception as e:
        print(e)
        pass

    return processed_image

def religion_of_interest(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    
    return cv2.bitwise_and(mask, image)

# def find_lanes(lines):
#     indexes = []

#     for line in lines:
#         coords = line[0]
#         x1 = coords[0]
#         y1 = coords[1]
#         x2 = coords[2]
#         y2 = coords[3]

#         if abs((y2-y1)/(x2-x1)) < 0.5:
#             lines.remove(line) 
    
#     return lines



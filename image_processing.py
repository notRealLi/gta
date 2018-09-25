import cv2
import numpy as np

def process_image(image):
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = edge_detection(processed_image)
    processed_image = cv2.GaussianBlur(processed_image, (3,3), 0)
    
    vertices = np.array([[0,600], 
                         #[180,470], [620,470], 
                         [800,600], [800,250], [570,200], [230,200], [0,250]])
    processed_image = religion_of_interest(image=processed_image, vertices=[vertices])

    lines = cv2.HoughLinesP(image=processed_image, rho=1, theta=np.pi/180, threshold=180, minLineLength=80, maxLineGap=5)
    lines = find_lanes(lines)
    try:
        for line in lines:
            # line = line[0]

            # A = np.vstack([(line[0], line[2]), np.ones(2)]).T
            # m, b = np.linalg.lstsq(A, (line[1], line[3]))[0]
        
            # if abs(m) < 2.5 and abs(m) > 0.3:
            #     cv2.line(processed_image, (line[0], line[1]), (line[2], line[3]), 255, 3)
            cv2.line(processed_image, (line[0], line[1]), (line[2], line[3]), 255, 3)
    except Exception as e:
        print(e)
        pass

    return processed_image


def contrast_enchancing(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def edge_detection(image, sigma=0.5):
    avg_pixel = np.mean(image)

    lower = int(max(0, avg_pixel * (1 - sigma)))
    upper = int(min(255, avg_pixel * (1 + sigma)))

    return cv2.Canny(image, threshold1=lower, threshold2=upper) # TODO: learn; tweak min and max


def religion_of_interest(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    
    return cv2.bitwise_and(mask, image)


def find_lanes(lines, min_y=250, max_y=600):
    
    ####################### Helper functions #######################    
    def average_regression(regressions):
        if len(regressions) == 0:
            return

        m_avg = 0
        b_avg = 0

        for regression in regressions:
            m_avg += regression[0]
            b_avg += regression[1]
        
        m_avg /= len(regressions)
        b_avg /= len(regressions)

        return [m_avg, b_avg]


    def draw_line(regression, y1, y2):
        m = regression[0]
        b = regression[1]
        x1 = (y1 - b) / m
        x2 = (y2 - b) / m

        return [int(x1), int(y1), int(x2), int(y2)]
        
    ####################### Main Logic #######################
    if lines is None:
        print('no lines')
        return       
    regression_dict = {'right': [], 'left': []}
    max_y = 600 
    min_y = 999

    for line in lines:
        coords = line[0]
        x1 = coords[0]
        y1 = coords[1]
        x2 = coords[2]
        y2 = coords[3]

        if y1 < min_y:
            min_y = y1
        if y2 < min_y:
            min_y = y2

        A = np.vstack([(x1, x2), np.ones(2)]).T
        m, b = np.linalg.lstsq(A, (y1, y2))[0]
        
        if abs(m) > 6 or abs(m) < 0.2: # here
            continue

        if m > 0:
            regression_dict['right'].append([m, b])
        else:
            regression_dict['left'].append([m, b])
    
    regressions = []
    regressions.append(average_regression(regression_dict['right']))
    regressions.append(average_regression(regression_dict['left']))

    lanes = []
    for regression in regressions:
        if regression is not None:
            lanes.append(draw_line(regression, min_y, max_y))

    return lanes



import cv2
import numpy as np
from skimage.filters import prewitt, roberts

# =========================
# Helper: generate code
# =========================
def gen_code(name, body):
    return f"""# {name} filter
import cv2
import numpy as np
from skimage.filters import prewitt, roberts

img = cv2.imread("Saida.png")

{body}

cv2.imwrite("output.png", result)
"""

# =========================
# Main function
# =========================
def apply_filter(img, filter_name):
    f = filter_name.lower()

    # ---------- BASIC ----------
    if f == "origin":
        return img, gen_code("origin", "result = img")

    if f == "gray":
        result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return result, gen_code("gray", "result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)")

    if f == "invert":
        result = cv2.bitwise_not(img)
        return result, gen_code("invert", "result = cv2.bitwise_not(img)")

    if f == "sepia":
        kernel = np.array([[0.272,0.534,0.131],
                           [0.349,0.686,0.168],
                           [0.393,0.769,0.189]])
        result = cv2.transform(img, kernel)
        result = np.clip(result,0,255).astype(np.uint8)
        return result, gen_code("sepia", "kernel=np.array([[0.272,0.534,0.131],[0.349,0.686,0.168],[0.393,0.769,0.189]])\nresult=cv2.transform(img,kernel)")

    if f == "hsv":
        result = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return result, gen_code("hsv", "result = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)")

    # ---------- CHANNELS ----------
    if f == "red_channel":
        result = img.copy()
        result[:,:,0] = 0
        result[:,:,1] = 0
        return result, gen_code("red_channel", "result=img.copy(); result[:,:,0]=0; result[:,:,1]=0")

    if f == "green_channel":
        result = img.copy()
        result[:,:,0] = 0
        result[:,:,2] = 0
        return result, gen_code("green_channel", "result=img.copy(); result[:,:,0]=0; result[:,:,2]=0")

    if f == "blue_channel":
        result = img.copy()
        result[:,:,1] = 0
        result[:,:,2] = 0
        return result, gen_code("blue_channel", "result=img.copy(); result[:,:,1]=0; result[:,:,2]=0")

    # ---------- BRIGHTNESS / CONTRAST ----------
    if f == "brightness_up":
        result = cv2.convertScaleAbs(img, alpha=1, beta=40)
        return result, gen_code("brightness_up", "result=cv2.convertScaleAbs(img,alpha=1,beta=40)")

    if f == "brightness_down":
        result = cv2.convertScaleAbs(img, alpha=1, beta=-40)
        return result, gen_code("brightness_down", "result=cv2.convertScaleAbs(img,alpha=1,beta=-40)")

    if f == "contrast_up":
        result = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
        return result, gen_code("contrast_up", "result=cv2.convertScaleAbs(img,alpha=1.5,beta=0)")

    if f == "contrast_down":
        result = cv2.convertScaleAbs(img, alpha=0.7, beta=0)
        return result, gen_code("contrast_down", "result=cv2.convertScaleAbs(img,alpha=0.7,beta=0)")

    # ---------- SATURATION ----------
    if f == "saturation_up":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = np.clip(hsv[:,:,1]*1.5,0,255)
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return result, gen_code("saturation_up", "hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV); hsv[:,:,1]*=1.5; result=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)")

    if f == "saturation_down":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = np.clip(hsv[:,:,1]*0.5,0,255)
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return result, gen_code("saturation_down", "hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV); hsv[:,:,1]*=0.5; result=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)")

    # ---------- GAMMA ----------
    if f == "gamma_correction":
        gamma = 1.5
        table = np.array([(i/255.0)**gamma*255 for i in range(256)]).astype("uint8")
        result = cv2.LUT(img, table)
        return result, gen_code("gamma_correction", "gamma=1.5; table=np.array([(i/255.0)**gamma*255 for i in range(256)]).astype('uint8'); result=cv2.LUT(img,table)")

    # ---------- BLUR ----------
    if f in ["blur","average_blur","box_blur"]:
        result = cv2.blur(img,(5,5))
        return result, gen_code(f, "result=cv2.blur(img,(5,5))")

    if f == "gaussian_blur":
        result = cv2.GaussianBlur(img,(5,5),0)
        return result, gen_code("gaussian_blur", "result=cv2.GaussianBlur(img,(5,5),0)")

    if f == "median_blur":
        result = cv2.medianBlur(img,5)
        return result, gen_code("median_blur", "result=cv2.medianBlur(img,5)")

    if f == "bilateral_blur":
        result = cv2.bilateralFilter(img,9,75,75)
        return result, gen_code("bilateral_blur", "result=cv2.bilateralFilter(img,9,75,75)")

    if f == "motion_blur":
        kernel = np.zeros((9,9))
        kernel[4,:] = 1/9
        result = cv2.filter2D(img,-1,kernel)
        return result, gen_code("motion_blur", "kernel=np.zeros((9,9)); kernel[4,:]=1/9; result=cv2.filter2D(img,-1,kernel)")

    # ---------- CARTOON / ART ----------
    if f == "cartoon":
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray,5)
        edges = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
        color = cv2.bilateralFilter(img,9,250,250)
        result = cv2.bitwise_and(color,color,mask=edges)
        return result, gen_code("cartoon", "gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); blur=cv2.medianBlur(gray,5); edges=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9); color=cv2.bilateralFilter(img,9,250,250); result=cv2.bitwise_and(color,color,mask=edges)")

    if f == "pencil":
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        inv = cv2.bitwise_not(gray)
        blur = cv2.GaussianBlur(inv,(21,21),0)
        result = cv2.divide(gray,255-blur,scale=256)
        return result, gen_code("pencil", "gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); inv=cv2.bitwise_not(gray); blur=cv2.GaussianBlur(inv,(21,21),0); result=cv2.divide(gray,255-blur,scale=256)")

    # ---------- EDGES ----------
    if f == "canny":
        result = cv2.Canny(img,100,200)
        return result, gen_code("canny", "result=cv2.Canny(img,100,200)")

    if f == "sobelx":
        g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        result=cv2.convertScaleAbs(cv2.Sobel(g,cv2.CV_64F,1,0))
        return result, gen_code("sobelx","g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); result=cv2.Sobel(g,cv2.CV_64F,1,0)")

    if f == "sobely":
        g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        result=cv2.convertScaleAbs(cv2.Sobel(g,cv2.CV_64F,0,1))
        return result, gen_code("sobely","g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); result=cv2.Sobel(g,cv2.CV_64F,0,1)")

    if f == "laplacian":
        g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        result=cv2.convertScaleAbs(cv2.Laplacian(g,cv2.CV_64F))
        return result, gen_code("laplacian","g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); result=cv2.Laplacian(g,cv2.CV_64F)")

    if f == "prewitt":
        g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        result=(prewitt(g)*255).astype(np.uint8)
        return result, gen_code("prewitt","g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); result=prewitt(g)*255")

    if f == "roberts":
        g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        result=(roberts(g)*255).astype(np.uint8)
        return result, gen_code("roberts","g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); result=roberts(g)*255")

    # ---------- MORPH ----------
    if f == "erode":
        k=np.ones((5,5),np.uint8)
        result=cv2.erode(img,k)
        return result, gen_code("erode","k=np.ones((5,5),np.uint8); result=cv2.erode(img,k)")

    if f == "dilate":
        k=np.ones((5,5),np.uint8)
        result=cv2.dilate(img,k)
        return result, gen_code("dilate","k=np.ones((5,5),np.uint8); result=cv2.dilate(img,k)")

    # ---------- NOISE ----------
    if f == "gaussian_noise":
        noise = np.random.normal(0,25,img.shape).astype(np.uint8)
        result = cv2.add(img,noise)
        return result, gen_code("gaussian_noise","noise=np.random.normal(0,25,img.shape).astype(np.uint8); result=cv2.add(img,noise)")

    if f == "salt_pepper_noise":
        result = img.copy()
        prob=0.02
        rnd=np.random.rand(*img.shape[:2])
        result[rnd<prob]=0
        result[rnd>1-prob]=255
        return result, gen_code("salt_pepper_noise","prob=0.02; rnd=np.random.rand(*img.shape[:2]); result[rnd<prob]=0; result[rnd>1-prob]=255")

    # ---------- DEFAULT ----------
    return img, gen_code("unknown", "result = img")

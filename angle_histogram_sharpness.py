import cv2
import numpy as np

# Rotates an image
def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    mean_pixel = np.median(np.median(image, axis=0), axis=0)
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=mean_pixel)
    return result

# Returns a small value if the horizontal histogram is sharp.
# Returns a large value if the horizontal histogram is blurry.
def eval_image(image: np.ndarray) -> float:
    hist = np.sum(np.mean(image, axis=1), axis=1)
    bef = 0
    aft = 0
    err = 0.
    assert(hist.shape[0] > 0)
    for pos in range(hist.shape[0]):
        if pos == aft:
            bef = pos
            while aft + 1 < hist.shape[0] and abs(hist[aft + 1] - hist[pos]) >= abs(hist[aft] - hist[pos]):
                aft += 1
        err += min(abs(hist[bef] - hist[pos]), abs(hist[aft] - hist[pos]))
    assert(err > 0)
    return err

# Measures horizontal histogram sharpness across many angles
def sweep_angles(image: np.ndarray) -> np.ndarray:
    results = np.empty((81, 2))
    for i in range(81):
        angle = (i - results.shape[0] // 2) / 4.
        rotated = rotate_image(image, angle)
        err = eval_image(rotated)
        results[i, 0] = angle
        results[i, 1] = err
    return results

# Find an angle that is a lot better than its neighbors
def find_alignment_angle(image: np.ndarray) -> float:
    best_gain = 0
    best_angle = 0.
    results = sweep_angles(image)
    for i in range(2, results.shape[0] - 2):
        ave = np.mean(results[i-2:i+3, 1])
        gain = ave - results[i, 1]
        # print('angle=' + str(results[i, 0]) + ', gain=' + str(gain))
        if gain > best_gain:
            best_gain = gain
            best_angle = results[i, 0]
    return best_angle

# input: an image that needs aligning
# output: the aligned image
def align_image(image: np.ndarray) -> np.ndarray:
    angle = find_alignment_angle(image)
    return rotate_image(image, angle)

# Do it
filePath= r"C:\Users\anass\Programmation\PDF\t.PNG"

fixme: np.ndarray = cv2.imread(filePath)
cv2.imwrite(filePath, align_image(fixme))

from PIL import Image

def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return width, height

def get_quadrants(width, height):
    y = width//2
    x = height//2
    return x, y

def locate_object(upper_left, bottom_right, x, y):
    if upper_left[0] in range(0, y) and bottom_right[0] in range(0, y): # check if object located on left
        if upper_left[1] in range(0, x) and bottom_right[1] in range(0, x): # check if object located on top half
            print("Object located in upper left quadrant.")
        elif upper_left[1] in range(0, x) and bottom_right[1] in range(x, x*2):
            print("Object located left of centre point.")
        else:
            print("Object located in bottom left quadrant.")
    elif upper_left[0] in range(0, y) and bottom_right[0] in range(y, y*2): # check if object located in centre
        if upper_left[1] in range(0, x) and bottom_right[1] in range(x, x*):
            print("Object located above centre point.")
        elif upper_left[1] in range(0, x) and bottom_right[1] in range(x, x*2):
            #  and here I got rlly tired
    
w, h = get_num_pixels("test_img.png")
print(get_quadrants(w,h))
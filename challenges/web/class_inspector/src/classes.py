import argparse

def lookup_class(input):
    if (input == 'chiu'):
        class_list = "110, 198c, 230"
    elif (input == 'parvini'):
        class_list = "110, 240, 311"
    elif (input == 'davila'):
        class_list = "160, 320, 429"
    elif (input == 'minea'):
        class_list = "220, H311"
    elif (input == 'barrington'):
        class_list = "250, 150"
    elif (input == 'richards'):
        class_list = "210, 198c, 326"
    else:
        class_list = "Sorry, the professor you're looking up does not exist in our system yet."

    print(class_list)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    lookup_class(args.input.lower())
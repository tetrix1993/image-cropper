import os
from PIL import Image


OUTPUT = 'out'
VALID_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']


CROP_START_POSITION_TOP_LEFT = 1
CROP_START_POSITION_BOTTOM_LEFT = 2
PROCESS_MODE_BASIC = 1
PROCESS_MODE_PARAM_RELATIVE = 2
PROCESS_MODE_PARAM_ABSOLUTE = 3


def run():
    process_mode = get_process_mode()
    if process_mode is None:
        return
    while True:
        dirfile = input('Enter directory or filepath of image: ').replace('\\', '/')
        if len(dirfile) == 0:
            return
        if os.path.isdir(dirfile):
            files = os.listdir(dirfile)
            file_list = []
            for file in files:
                filepath = dirfile + '/' + file
                if os.path.isfile(filepath) and has_valid_extension(file):
                    file_list.append(file)
            if len(file_list) == 0:
                print('[ERROR] Directory has no images.')
                continue
            process_file_choice(dirfile, file_list, process_mode)
        elif os.path.isfile(dirfile):
            if has_valid_extension(dirfile):
                file = dirfile.split('/')[-1]
                dir = dirfile[0:len(dirfile) - len(file) - 1]
                process_file(dir, file, process_mode)
            else:
                print('[ERROR] Expecting the file to have one of the extensions: ' + get_all_extensions())
        else:
            print('[ERROR] Directory or image does not exists')


def get_process_mode():
    print('[INFO] Select process mode')
    print('1: Basic')
    print('2: Parameter Relative')
    print('3: Parameter Absolute')
    process_mode = input('Enter choice: ')
    if process_mode.strip() in ['1', '2', '3']:
        return int(process_mode.strip())
    else:
        return None


def has_valid_extension(file):
    for ext in VALID_IMAGE_EXTENSIONS:
        if file.endswith(ext):
            return True
    return False


def get_all_extensions():
    output = ''
    for ext in VALID_IMAGE_EXTENSIONS:
        if len(output) == 0:
            output = ext
        else:
            output = output + ', ' + ext
    return output


def process_file_choice(dir, file_list, process_mode):
    while True:
        print('[INFO] Select file: ')
        for i in range(len(file_list)):
            print('%s - %s' % (str(i + 1), file_list[i]))
        choice = input('Enter choice: ')
        if len(choice) == 0:
            break
        if choice.isnumeric():
            choice_num = int(choice)
            if choice_num < 1 or choice_num > len(file_list):
                break
            else:
                process_file(dir, file_list[choice_num - 1], process_mode)
        else:
            print('[ERROR] Invalid choice.')


def process_file(dir, file, process_mode):
    while True:
        original_filepath = dir + '/' + file
        try:
            with Image.open(original_filepath) as im:
                if process_mode == PROCESS_MODE_BASIC:
                    original_width, original_height = im.size
                    print('[INFO] Image size: %sx%s' % (str(original_width), str(original_height)))
                    crop_start_pos = get_crop_from_choice()
                    if crop_start_pos is None:
                        return
                    pos_x = int(input('Enter start position X: '))
                    if pos_x > original_width:
                        print('[ERROR] Start position X exceeds original width.')
                        return
                    elif pos_x < 0:
                        print('[ERROR] Value must be 0 or more.')
                        return

                    temp_pos_y = int(input('Enter start position Y: '))
                    if temp_pos_y > original_height:
                        print('[ERROR] Start position Y exceeds original height.')
                        return
                    elif temp_pos_y < 0:
                        print('[ERROR] Value must be 0 or more.')
                        return

                    width = int(input('Enter width: '))
                    if width + pos_x > original_width:
                        width = original_width - pos_x

                    height = int(input('Enter height: '))
                    if crop_start_pos == CROP_START_POSITION_BOTTOM_LEFT:
                        pos_y = temp_pos_y - height
                        if pos_y < 0:
                            pos_y = 0
                    else:
                        pos_y = temp_pos_y

                    end_pos_x = pos_x + width
                    end_pos_y = pos_y + height

                    cropped_image = im.crop((pos_x, pos_y, end_pos_x, end_pos_y))
                    output_file(file, cropped_image)
                elif process_mode == PROCESS_MODE_PARAM_RELATIVE:
                    user_input = input('Enter param ({start_pos_x} {start_pos_y} {width} {height}): ')
                    if len(user_input) == 0:
                        return
                    params = user_input.split(' ')
                    if len(params) == 4:
                        pos_x = int(params[0])
                        pos_y = int(params[1])
                        end_pos_x = pos_x + int(params[2])
                        end_pos_y = pos_y + int(params[3])
                        cropped_image = im.crop((pos_x, pos_y, end_pos_x, end_pos_y))
                        output_file(file, cropped_image)
                elif process_mode == PROCESS_MODE_PARAM_ABSOLUTE:
                    user_input = input('Enter param ({start_pos_x} {start_pos_y} {end_pos_x} {end_pos_y}): ')
                    if len(user_input) == 0:
                        return
                    params = user_input.split(' ')
                    if len(params) == 4:
                        pos_x = int(params[0])
                        pos_y = int(params[1])
                        end_pos_x = int(params[2])
                        end_pos_y = int(params[3])
                        cropped_image = im.crop((pos_x, pos_y, end_pos_x, end_pos_y))
                        output_file(file, cropped_image)
                else:
                    return
        except Exception:
            print('[ERROR] Invalid input.')


def get_crop_from_choice():
    print('[INFO] Crop Start Position')
    print('1: Top Left')
    print('2: Bottom Left')
    result = input('Enter choice: ').strip()
    if result == '1' or result == '2':
        return int(result)
    return None


def output_file(file, image):
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    i = 0
    filename, extension = extract_filename_and_extension(file)
    while True:
        if i == 0:
            output_name = file
        else:
            output_name = filename + ' (' + str(i) + ')' + extension
        output_filepath = OUTPUT + '/' + output_name
        if not os.path.exists(output_filepath):
            image.save(output_filepath)
            print('[SUCCESS] Image saved as %s' % output_filepath)
            break
        i += 1


def extract_filename_and_extension(file_with_extension):
    for ext in VALID_IMAGE_EXTENSIONS:
        if file_with_extension.endswith(ext):
            filename = file_with_extension[0:len(file_with_extension) - len(ext)]
            extension = ext
            return filename, extension
    return file_with_extension, ''


if __name__ == '__main__':
    run()

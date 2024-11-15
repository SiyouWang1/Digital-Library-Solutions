import numpy as np
import random
import os
from faker import Faker
from PIL import Image, ImageDraw, ImageFont
import csv

# Important ranges / parameters
image_width_low = 1000
image_width_high = 2000
image_height_low = 1000
image_height_high = 2000
back_color_low = 0
back_color_high = 127
paper_width_multiplier = 0.577
paper_height_multiplier = 0.577
paper_color_low = 128
paper_color_high = 255
# remember, variable names with the suffix denominator_high does not
# mean the denominator, which is the variable itself, should be big
# instead, it is saying that the value of numerator / denominator
# will be high, meaning the denominator will be low
leftright_margin_denominator_low = 30
top_margin_denominator_low = 30
bottom_margin_denominator_low = 30
leftright_margin_denominator_high = 10 
top_margin_denominator_high = 7
bottom_margin_denominator_high = 7
paper_x_position_offset_denominator = 7
paper_y_position_offset_denominator = 7
possible_col_count = [1, 2, 4]
# the following two variables refers to the percentage of texts the
# paper should have in terms of width, after excluding the left/right margins
width_percentage_low = 0.98
width_percentage_high = 0.99
paragraph_per_col_low = 2 # this value has to be greater than 1
paragraph_per_col_high = 5
font_size_low = 12
font_size_high = 22
line_spacing_multiplier_low = 0.2
line_spacing_multiplier_high = 0.5
paragraph_spacing_multiplier_low = 3
paragraph_spacing_multiplier_high = 4
# language and font type changes need to be installed and changed by you
# no parameter can tune them for you
word_count_low = 2000
word_count_high = 4000
slight_rotation_low = -5
slight_rotation_high = 5
text_color_low = 0
text_color_high = 100
num_of_images = 20000
Tamil_word_len = [7, 5, 11, 10, 9, '.', 4, 10, ',', 12, ';', 8, 9, 5, 8, '.', 6, 8, 9, 9, 4, 9, '.', 9, 5, ':', 9, 12, 7, ';', 9, 14, '.', 9, 5, 13, 7, ',', 3, 6, 5, ',', 5, 11, 13, 10, '.', 6, 9, 4, 7, ',', 9, 4, 7, 11, '.', 8, 8, 5, 10, '.', 9, 5, ':', 8, 7, 3, 10, 12, ',', 3, 14, 8, 13, 7, '.', 5, 8, 9, ',', 16, 7, 11, ',', 12, 9, 10, 10, ';', 3, 8, 4, '.', 5, 11, 9, 5, 11, '.', 8, 14, 4, 8, 4, '.', 9, 5, ':', 9, 7, 7, 10, 10, ',', 5, 5, 12, 7, ';', 8, 7, '.', 6, 5, 7, 4, 5, 9, ';', 8, 13, 4, 4, 5, 10, ';', 3, 6, 5, 5, 7, '.', 9, 5, ':', 9, 10, ',', 8, 10, 12, ',', 4, 12, 8, 10, ',', 12, 16, 7, ';', 3, 8, 4, '.', 9, 10, ',', 4, 7, 8, 9, 10, 13, ',', 9, 5, 10, ',', 4, 7, 4, 13, 12, ';', 3, 6, 5, 6, 7, '.', 8, 15, 4, 8, 4, '.', 11, 5, ':', 8, 8, 13, 9, 10, 12, 9, ';', 3, 16, ',', 17, ',', 16, ',', 14, 12, '.', 2, 6, 6, 5, 10, 13, '.', 5, 9, 4, 6, ',', 7, 9, 4, 6, ':', 18, 13, '.', 11, 5, 12, 13, 11, ',', 10, 8, 6, ',', 11, 13, 11, ',', 7, 9, 10, 8, ';', 3, 6, 5, 5, 7, '.', 2, 8, 15, 4, 8, 4, '.', 11, 5, ':', 8, 7, 15, ',', 8, 4, 9, 14, 12, 11, 7, 11, 16, 7, '.', 2, 5, 5, 17, ',', 7, 3, 14, ',', 8, 10, ',', 7, 11, 12, ',', 8, 4, 7, 11, 9, ';', 3, 6, 5, 6, 7, '.', 2, 6, 6, 7, 12, ':', 7, 7, 6, ',', 9, 4, 7, 12, ',', 7, 8, 11, '.', 2, 8, 15, 4, 7, 4, '.', 11, 5, ':', 9, 7, 3, 15, ',', 14, ',', 7, 8, 13, ',', 8, 14, ',', 7, 13, 16, 7, ';', 3, 8, 4, '.', 2, 5, 8, 7, 3, 14, ',', 7, 3, 14, ',', 12, 7, 8, 13, 13, ';', 3, 6, 5, 5, 7, '.', 11, 5, ':', 8, 9, ',', 8, 9, 6, 14, ';', 7, 4, 4, ',', 10, 7, ',', 10, ',', 4, 11, 16, 7, '.', 8, 6, 7, 9, '.', 2, 4, 6, 8, 3, 7, 9, ',', 8, 7, 6, 9, '.', 5, 8, 9, 9, '.', 2, 5, 7, 14, ',', 6, 5, 7, 6, ':', 7, 7, 6, ',', 6, 7, ',', 5, 18, ';', 4, 7, ',', 10, 7, 7, 3, 10, 6, 5, 11, '.', 8, 4, 9, '.', 11, 5, ':', 3, ',', 12, 4, 9, 5, 7, 12, ',', 8, 5, 8, 6, 9, 5, 11, 12, 10, '.', 3, 10, 12, 9, '.', 2, 11, 3, 16, ',', 10, 3, 13, ',', 8, 6, 3, 14, ',', 3, 8, 13, 7, 10, ';', 3, 8, 8, '.', 2, 6, 4, 6, 11, 10, ',', 3, 7, 6, 8, '.', 8, 8, 5, 4, 4, '.']
Tamil_letters = 'ௐஅஆஇஈஉஊஎஏஐஒஓஔஃகஙசஞடணதநபமயரலவழளறனஜஶஷஸஹ௳௴௵௶௷௸௺௹'

# Paths
upright = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\Generated Tamil Pages\\upright'
upside_down = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\Generated Tamil Pages\\upside-down'


# Utility function to generate random color
def random_color(low, high):
    return (np.random.randint(low, high), 255)

# Function to generate the background with a shape a color
def generate_background(image_size):
    color = random_color(back_color_low, back_color_high)
    background = Image.new('LA', image_size, color)
    # You can add more patterns if needed
    return background, color

# Function to create the paper size and color
def create_paper(image_size):
    background_width, background_height = image_size

    # Ensure paper is at least 33% of the background
    paper_width = random.randint(int(background_width * paper_width_multiplier), background_width)
    paper_height = random.randint(int(background_height * paper_height_multiplier), background_height)
    
    # Create paper
    color = random_color(paper_color_low, paper_color_high)
    paper = Image.new('LA', (paper_width, paper_height), color)
    
    return paper, color

# Function to generate margins to paper
def get_margins(paper_size):
    paper_width, paper_height = paper_size
    margins = {
        "left_right": random.randint(paper_width // leftright_margin_denominator_low, paper_width // leftright_margin_denominator_high),
        "top": random.randint(paper_height // top_margin_denominator_low, paper_height // top_margin_denominator_high),
        "bottom": random.randint(paper_height // bottom_margin_denominator_low, paper_height // bottom_margin_denominator_high)
    }
    return margins

# Function to determine the number of columns
def get_columns():
    return random.choice(possible_col_count)

# Function to select font size
def get_font_size():
    return random.randint(font_size_low, font_size_high)

# Function to select line spacing
def get_line_spacing(font_size):
    return random.uniform(int(font_size * line_spacing_multiplier_low), int(font_size * line_spacing_multiplier_high))

# Function to select paragraph spacing
def get_paragraph_spacing(line_spacing):
    return random.uniform(int(line_spacing * paragraph_spacing_multiplier_low), int(line_spacing * paragraph_spacing_multiplier_high))

# Function to generate a paragraph of Tamil words
def tamil_paragraph(count):
    result = ''
    while count != 0:
        word_len = random.choice(Tamil_word_len)
        if type(word_len) == int:
            i = 0
            result += ' '
            while i < word_len:
                result += random.choice(Tamil_letters)
                i += 1
        else:
            result += word_len
        count -= 1
    return result

# Function to select language, the supported languages are ["english", "arabic", "latin", 'Tamil']
def get_language():
    return random.choice(["english", 'Tamil', 'Tamil'])

# Function to select font based on language
def get_font(language):
    if language == "english":
        return random.choice(['SCRIPTIN.ttf', 'ChopinScript.ttf', 'GreatVibes-Regular.ttf'])
    elif language == "arabic":
        return random.choice(['ScheherazadeRegOT.ttf', 'KfgqpcHafsUthmanicScriptRegular-1jGEe.ttf', 'NotoSansArabic-VariableFont_wdth,wght.ttf'])
    elif language == "latin":
        return random.choice(['SCRIPTIN.ttf', 'ChopinScript.ttf', 'GreatVibes-Regular.ttf'])
    elif language == "Tamil":
        return random.choice(['Tamil Bold Serif.ttf', 'Tamil Thin Serif.ttf'])
    else:
        return "arial.ttf"

# Function to generate text content
def generate_text_content(language, word_count):
    if language == "english":
        fake = Faker('en')
        paragraph = fake.text(max_nb_chars=word_count)
        return paragraph
    elif language == "arabic":
        fake = Faker('ar_AA')
        paragraph = fake.text(max_nb_chars=word_count)
        return paragraph
    elif language == "latin":
        fake = Faker('fr_FR')
        paragraph = fake.text(max_nb_chars=word_count)
        return paragraph
    elif language == "Tamil":
        return tamil_paragraph(word_count)


# Function to print the text on the paper
def print_text_on_paper(paper, text, font_path, font_size, columns, column_spacing, paragraph_per_col, margins, line_spacing, paragraph_spacing):
    draw = ImageDraw.Draw(paper)
    font = ImageFont.truetype(font_path, font_size)
    
    # Calculate text area based on margins
    paper_width, paper_height = paper.size
    text_area_width = paper_width - 2 * margins["left_right"]
    text_area_height = paper_height - margins["top"] - margins["bottom"]

    column_spacing = column_spacing  # Define the horizontal spacing between columns
    # Calculate width per column
    column_width = (text_area_width - column_spacing * (columns - 1)) // columns

    # Split text into lines based on pixel width (using textbbox)
    wrapped_lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)

        if bbox[2] <= column_width:  # If the line width is within the column width
            current_line = test_line # add the word to this line
        else: # if adding a new word results in exceeding the width
            wrapped_lines.append(current_line)  # write it to the finalized lines
            if current_line != '': # if something is already determined to exist on this line
                if draw.textbbox((0, 0), word, font=font)[2] <= column_width: # if pushing the new word to the next line does not result in immediate width violation
                    current_line = word  # Start a new line
                else:
                    current_line = word[:6] # only write the first 6 letters of the word
            else: # if nothing is written, and adding this one word results in width violation
                current_line = word[:6] # only write the first 6 letters of the word
    
    if current_line:
        wrapped_lines.append(current_line)  # Deal with the last line of the text

    # Start printing the wrapped lines column by column
    current_y = margins["top"]
    current_x = margins["left_right"]
    column_counter = 1  # Track the current column number
    fill = random_color(text_color_low, text_color_high)
    actual_paragraphs = random.randint(paragraph_per_col - 2, paragraph_per_col + 2)

    # find out how many lines of texts together with line spacing and paragraph spacing
    # can exist on one column
    line_count = 0
    y = current_y + actual_paragraphs * (paragraph_spacing - line_spacing)
    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        
        # Check if the current column exceeds the text area height
        if y + line_height > text_area_height:
            break
            
        line_count += 1
        # Draw the text line at the current position
        y += line_height + line_spacing
    if actual_paragraphs >= 1:
        avg_line_per_paragraph = line_count // actual_paragraphs
    else: 
        avg_line_per_paragraph = 999 # just a randomly large number
        
    actual_line_per_paragraph = random.randint(avg_line_per_paragraph - 2, avg_line_per_paragraph + 2)
    last_paragraph_line = 1
    current_line = 1

    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        
        # Check if the current column exceeds the text area height
        if current_y + line_height > text_area_height:
            # Move to the next column
            column_counter += 1
            if column_counter > columns:
                break  # No more columns, stop drawing
            
            current_x = margins["left_right"] + (column_width + column_spacing) * (column_counter - 1)
            current_y = margins["top"]  # Reset Y position for the new column
            last_paragraph_line = 1
            current_line = 1

        current_line += 1
        if current_line - last_paragraph_line == actual_line_per_paragraph:
            draw.text((current_x, current_y), line, font=font, fill=fill)
            current_y += line_height + paragraph_spacing
            actual_line_per_paragraph = random.randint(avg_line_per_paragraph - 2, avg_line_per_paragraph + 2)
            last_paragraph_line = current_line
        else:
            # Draw the text line at the current position
            draw.text((current_x, current_y), line, font=font, fill=fill)
            current_y += line_height + line_spacing

    return paper, fill

# Main function to generate the image
def generate_image(amount):
    image_specs = []
    up = True
    name = ''
    while amount > 0:
        print(amount)
        # Step 1: Image size (background)
        image_width = random.randint(image_width_low, image_width_high)
        image_height = random.randint(image_height_low, image_height_high)
        background, bg_color = generate_background((image_width, image_height))
        
        # Step 2: Paper color and shape
        paper, ppr_color = create_paper((image_width, image_height))
        
        # Step 3: Paper margins
        margins = get_margins(paper.size)
        
        # Step 4: Number of columns
        columns = get_columns()
        
        # Step 5: Font size and spacing
        font_size = get_font_size()
        line_spacing = get_line_spacing(font_size)
        paragraph_spacing = get_paragraph_spacing(line_spacing)
        
        # Step 6: Language and font
        language = get_language()
        font_path = get_font(language)
        
        # Step 7: Text content and fit into the margins
        word_count = random.randint(word_count_low, word_count_high)
        text_content = generate_text_content(language, word_count)

        # text area width refers to the width of text after substracting the left and right margins
        text_area_width = random.randint(int((paper.size[0] - 2 * margins['left_right']) * width_percentage_low), int((paper.size[0] - 2 * margins['left_right']) * width_percentage_high))
        if columns != 1:
            column_spacing = (paper.size[0] - text_area_width) // (columns - 1)
        else:
            column_spacing = 0

        # average number of paragraphs per column for the whole image
        paragraph_per_col = random.randint(paragraph_per_col_low, paragraph_per_col_high)

        # Step 8: Print text on the paper
        paper_with_text, text_color = print_text_on_paper(paper, text_content, font_path, font_size, columns, column_spacing, paragraph_per_col, margins, line_spacing, paragraph_spacing)
        
        # Rotate the paper randomly between 0 and 5 degrees
        angle = random.uniform(slight_rotation_low, slight_rotation_high)
        paper_with_text = paper_with_text.rotate(angle, expand=True)

        # Step 9: Overlay the paper on the background with slight offsets
        x_offset = np.random.randint(-paper.size[1] // paper_x_position_offset_denominator, paper.size[1] // paper_x_position_offset_denominator)
        y_offset = np.random.randint(-paper.size[0] // paper_y_position_offset_denominator, paper.size[0] // paper_y_position_offset_denominator)
        paper_x = (image_width - paper_with_text.width) // 2 + x_offset
        paper_y = (image_height - paper_with_text.height) // 2 + y_offset
        background.paste(paper_with_text, (paper_x, paper_y), paper_with_text)
        
        # Step 10: Random 50-50 chance to rotate the entire image 180 degrees and save them in a path
        if amount % 2 == 0:
            background = background.rotate(180)
            # Save the image
            name = f"{amount}.png"
            path = os.path.join(upside_down, name)
            background.save(path)
            amount -= 1
            up = False
        else:
            # Save the image
            name = f"{amount}.png"
            path = os.path.join(upright, name)
            background.save(path)
            amount -= 1
            up = True
        image_specs.append({'name': name,
                        'image width': image_width,
                        'image height': image_height,
                        'image height:width': image_height / image_width,
                        'paper width': np.shape(paper)[1],
                        'paper height': np.shape(paper)[0],
                        'paper height:width': np.shape(paper)[0] / np.shape(paper)[1],
                        'width paper:image': np.shape(paper)[1] / image_width,
                        'height paper:image': np.shape(paper)[0] / image_height,
                        'background color': bg_color[0],
                        'paper color': ppr_color[0],
                        'text color': text_color[0],
                        'color background:paper': bg_color[0] / ppr_color[0],
                        'color text:paper': text_color[0] / ppr_color[0],
                        'left/right margins': margins["left_right"],
                        'top margin': margins["top"],
                        'bottom margin': margins["bottom"],
                        'column count': columns,
                        'font size': font_size,
                        'line spacing': line_spacing,
                        'paragraph spacing': paragraph_spacing,
                        'language': language,
                        'font type': font_path,
                        'word count': word_count,
                        # 'word percentage': ,
                        'slight rotation (in degrees)': angle,
                        'paper x offset': x_offset,
                        'paper y offset': y_offset,
                        'upright?': up 
                        })
    return image_specs

# Call the function to generate the image
image_specs = generate_image(num_of_images)
csv_file = 'image_specs.csv'

# Writing to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=image_specs[0].keys())
    writer.writeheader()
    writer.writerows(image_specs)
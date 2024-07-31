import matplotlib.pyplot as plt
import random
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar, LTAnno


def plot_word_boxes(file, num_pages_to_display):
    laparams = LAParams()
    pages = list(extract_pages(file, laparams=laparams))

    if num_pages_to_display > len(pages):
        num_pages_to_display = len(pages)

    for page_num in range(num_pages_to_display):
        page = pages[page_num]
        page_height = page.height
        page_width = page.width

        fig, ax = plt.subplots()
        ax.set_xlim(0, page_width / 72)
        ax.set_ylim(0, page_height / 72)
        ax.invert_yaxis()

        for element in page:
            if isinstance(element, LTTextBox):
                for text_line in element:
                    if isinstance(text_line, LTTextLine):
                        line_words = []
                        for character in text_line:
                            if isinstance(character, LTChar):
                                line_words.append(character)
                            elif isinstance(character, LTAnno) and character.get_text() == " ":
                                if line_words:
                                    x0, y0 = line_words[0].x0 / 72, (page_height - line_words[0].y0) / 72
                                    x1, y1 = line_words[-1].x1 / 72, (page_height - line_words[-1].y1) / 72
                                    word = "".join([char.get_text() for char in line_words])
                                    bbox = [
                                        [x0, y0],  # bottom-left
                                        [x1, y0],  # bottom-right
                                        [x1, y1],  # top-right
                                        [x0, y1],  # top-left
                                        [x0, y0]   # close the box
                                    ]
                                    color = (random.random(), random.random(), random.random())
                                    ax.plot(*zip(*bbox), color=color)
                                    ax.text((x0 + x1) / 2, (y0 + y1) / 2, word, ha='center', va='center', color=color)
                                    line_words = []
                        if line_words:
                            x0, y0 = line_words[0].x0 / 72, (page_height - line_words[0].y0) / 72
                            x1, y1 = line_words[-1].x1 / 72, (page_height - line_words[-1].y1) / 72
                            word = "".join([char.get_text() for char in line_words])
                            bbox = [
                                [x0, y0],  # bottom-left
                                [x1, y0],  # bottom-right
                                [x1, y1],  # top-right
                                [x0, y1],  # top-left
                                [x0, y0]   # close the box
                            ]
                            color = (random.random(), random.random(), random.random())
                            ax.plot(*zip(*bbox), color=color)
                            ax.text((x0 + x1) / 2, (y0 + y1) / 2, word, ha='center', va='center', color=color)

        ax.set_title(f'Page {page_num + 1}')
        plt.show()

plot_word_boxes(r'EKR_watcher\kozbeszerzesek\EKR001202872024_done\EKR001202872024_Nemzeti Ajánlati  részvételi felhívás_2024_07_21.pdf', 1)


import tkinter
import json
import PIL.Image
import tkinter.scrolledtext as scrolltxt
from PIL import ImageTk
from user import User
from data_parser import DataParsed
from tkinter import *
from html2image import Html2Image

index = 0
quiz_score = 0
user_info = [None] * 6
user = None
CELEBRITY_MODE = False
QUIZ_MODE = False
END = 0
pimg = None
answers_dict = {
    "Q1": "",
    "Q2": "",
    "Q3": "",
    "Q4": "",
    "Q5": "",
    "Q6": "",
    "Q7": ""
}

BG_COLOR = "white"
FONT_NAME = "Unispace"
CHAT_BG = "#e6fcec"
ENTRY_BG = "#cfe3d4"

window = Tk()
window.title("Astrology Guide Bot")
window.minsize(width=1200, height=650)
window.maxsize(width=1200, height=650)
window.config(bg=BG_COLOR)


def process_input():
    global index, user_info, user, CELEBRITY_MODE, QUIZ_MODE, quiz_score, answers_dict
    chat_log_scroll.config(state=NORMAL)
    chat_log_scroll.insert(tkinter.END, "User: " + user_entry.get() + "\n", "user_txt")

    if user_entry.get().lower() == "quiz" or QUIZ_MODE:
        QUIZ_MODE = True
        if index == 0:
            if answers_dict["Q1"] or "first" or "1st" in user_entry.get().lower():
                quiz_score += 1
                chat_log_scroll.insert(tkinter.END, "Bot: Correct!\n")
            else:
                chat_log_scroll.insert(tkinter.END, f"Bot: Unfortunately, you are incorrect :(\n"
                                                    f"The answer is {answers_dict['Q1']}\n")
            chat_log_scroll.insert(tkinter.END, "Bot: Is your chart a day or night chart?\n")
        elif index == 1:
            if answers_dict["Q2"] in user_entry.get().lower():
                quiz_score += 1
                chat_log_scroll.insert(tkinter.END, "Bot: Correct!\n")
            else:
                chat_log_scroll.insert(tkinter.END, f"Bot: Unfortunately, you are incorrect :(\n"
                                                    f"The answer is {answers_dict['Q2']}\n")
            chat_log_scroll.insert(tkinter.END, "Bot: What is the ruler of your Ascendant?\n")
        elif index == 2:
            if answers_dict["Q3"] in user_entry.get().lower():
                quiz_score += 1
                chat_log_scroll.insert(tkinter.END, "Bot: Correct!\n")
            else:
                chat_log_scroll.insert(tkinter.END, f"Bot: Unfortunately, you are incorrect :(\n"
                                                    f"The answer is {answers_dict['Q3']}\n")
            chat_log_scroll.insert(tkinter.END, "Bot: If you have a day chart, your most positive planet is Jupiter.\n"
                                                "If you have a night chart, your most positive planet is Venus.\n")
            chat_log_scroll.insert(tkinter.END, "Bot: Which house has your most positive planet?\n")
        elif index == 3:
            if answers_dict["Q4"] in user_entry.get().lower():
                quiz_score += 1
                chat_log_scroll.insert(tkinter.END, "Bot: Correct!\n")
            else:
                chat_log_scroll.insert(tkinter.END, f"Bot: Unfortunately, you are incorrect :(\n"
                                                    f"The answer is {answers_dict['Q4']}\n")
            chat_log_scroll.insert(tkinter.END, "Bot: If you have a day chart, your most challenging\n"
                                                "planet is Mars. If you have a night chart, \nyour most\n"
                                                "challenging planet is Saturn.\n")
            chat_log_scroll.insert(tkinter.END, "Bot: Which house has your most challenging/negative planet?\n")
        elif index == 4:
            if answers_dict["Q5"] in user_entry.get().lower():
                quiz_score += 1
                chat_log_scroll.insert(tkinter.END, "Bot: Correct!\n")
            else:
                chat_log_scroll.insert(tkinter.END, f"Bot: Unfortunately, you are incorrect :(\n"
                                                    f"The answer is {answers_dict['Q5']}\n")
            chat_log_scroll.insert(tkinter.END, f"Bot: You scored a {quiz_score}/5 !\n"
                                                f"Bot: Would you like to do another person\n(type \"Me\" or a "
                                                f"celebrity's "
                                                " name\n(\"Brad Pitt\"))\n")
            index = -1
            QUIZ_MODE = False
        index += 1
        user_entry.delete(0, tkinter.END)
        return

    if user_entry.get() == "":
        return False
    else:
        if user_entry.get().lower() == "me" or index > 0:
            CELEBRITY_MODE = False
        else:
            CELEBRITY_MODE = True

        if not CELEBRITY_MODE:
            if index == 0:
                tutorial_bot("NAME")
            elif index == 1:
                user_info[index - 1] = user_entry.get()
                tutorial_bot("DOB", user_info[0])
            elif index == 2:
                user_info[index - 1] = user_entry.get()
                tutorial_bot("HOUR", user_info[0])
            elif index == 3:
                user_info[index - 1] = user_entry.get()
                tutorial_bot("MINUTE", user_info[0])
            elif index == 4:
                user_info[index - 1] = user_entry.get()
                tutorial_bot("CITY", user_info[0])
            elif index == 5:
                user_info[index - 1] = user_entry.get()
                tutorial_bot("COUNTRY", user_info[0])
            elif index == 6:
                user_info[index - 1] = user_entry.get()
                user = User(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5])
                create_data(user)
                display_birth_chart()
                QUIZ_MODE = True
                index = -1
                chat_log_scroll.insert(tkinter.END, "Bot: Alright! Let's take a quiz on the person's chart you've "
                                                    "created!\n "
                                                    "Let's begin with finding your Ascendant\n"
                                                    "(As). Which house is your Ascendant located in? \n")
            index += 1
        else:
            celebrity = DataParsed(user_entry.get())
            user = User(celebrity.name.lower(), celebrity.dob, celebrity.hour, celebrity.minute,
                        celebrity.city, celebrity.country)
            create_data(user)
            display_birth_chart()
            QUIZ_MODE = True
            index = 0
            chat_log_scroll.insert(tkinter.END, "Bot: Alright! Let's take a quiz on the person's chart you've "
                                                "created!\n "
                                                "Let's begin with finding your Ascendant\n"
                                                "(As). Which house is your Ascendant located in? \n")

    user_entry.delete(0, tkinter.END)
    return True


def create_data(user_data):
    json_str = "" + user_data.astro_data.json()

    planets_and_cusps = json.loads(json_str)
    sign_key = planets_and_cusps["first_house"]["sign_num"] if planets_and_cusps["first_house"]["sign_num"] > 0 else 1
    planet_asc_ruler = ""

    data_poi = {
        "Ds": [planets_and_cusps["first_house"]["abs_pos"]],
        "Ic": [planets_and_cusps["fourth_house"]["abs_pos"]],
        "As": [planets_and_cusps["seventh_house"]["abs_pos"]],
        "Mc": [planets_and_cusps["eleventh_house"]["abs_pos"]]
    }

    data = {
        "planets": {
            "Pluto": [planets_and_cusps["pluto"]["abs_pos"]],
            "Neptune": [planets_and_cusps["neptune"]["abs_pos"]],
            "Jupiter": [planets_and_cusps["jupiter"]["abs_pos"]],
            "Mars": [planets_and_cusps["mars"]["abs_pos"]],
            "Moon": [planets_and_cusps["moon"]["abs_pos"]],
            "Sun": [planets_and_cusps["sun"]["abs_pos"]],
            "Mercury": [planets_and_cusps["mercury"]["abs_pos"]],
            "Venus": [planets_and_cusps["venus"]["abs_pos"]],
            "Saturn": [planets_and_cusps["saturn"]["abs_pos"]],
            "Uranus": [planets_and_cusps["uranus"]["abs_pos"]],
            "NNode": [planets_and_cusps["mean_node"]["abs_pos"]]
        },
        "cusps": [
            sign_key * 30,
            (sign_key + 1 if sign_key + 1 <= 12 else sign_key - 11) * 30,
            (sign_key + 2 if sign_key + 2 <= 12 else sign_key - 10) * 30,
            (sign_key + 3 if sign_key + 3 <= 12 else sign_key - 9) * 30,
            (sign_key + 4 if sign_key + 4 <= 12 else sign_key - 8) * 30,
            (sign_key + 5 if sign_key + 5 <= 12 else sign_key - 7) * 30,
            (sign_key + 6 if sign_key + 6 <= 12 else sign_key - 6) * 30,
            (sign_key + 7 if sign_key + 7 <= 12 else sign_key - 5) * 30,
            (sign_key + 8 if sign_key + 8 <= 12 else sign_key - 4) * 30,
            (sign_key + 9 if sign_key + 9 <= 12 else sign_key - 3) * 30,
            (sign_key + 10 if sign_key + 10 <= 12 else sign_key - 2) * 30,
            (sign_key + 11 if sign_key + 11 <= 12 else sign_key - 1) * 30
        ],
        "poi": data_poi
    }

    if data["cusps"][0] == 180:
        planet_asc_ruler = "venus"
    elif data["cusps"][0] == 210:
        planet_asc_ruler = "mars"
    elif data["cusps"][0] == 240:
        planet_asc_ruler = "jupiter"
    elif data["cusps"][0] == 270:
        planet_asc_ruler = "saturn"
    elif data["cusps"][0] == 300:
        planet_asc_ruler = "saturn"
    elif data["cusps"][0] == 330:
        planet_asc_ruler = "jupiter"
    elif data["cusps"][0] == 360:
        planet_asc_ruler = "mars"
    elif data["cusps"][0] == 30:
        planet_asc_ruler = "venus"
    elif data["cusps"][0] == 60:
        planet_asc_ruler = "mercury"
    elif data["cusps"][0] == 90:
        planet_asc_ruler = "moon"
    elif data["cusps"][0] == 120:
        planet_asc_ruler = "sun"
    elif data["cusps"][0] == 150:
        planet_asc_ruler = "mercury"

    answers_dict["Q1"] = str(int((planets_and_cusps["seventh_house"]["abs_pos"] // 30) + 1))
    answers_dict["Q2"] = str("day" if 360 - planets_and_cusps["sun"]["abs_pos"] > 180 else "night")
    answers_dict["Q3"] = str(planet_asc_ruler)
    answers_dict["Q4"] = str("jupiter" if answers_dict["Q2"] == "day" else "venus")
    answers_dict["Q5"] = str("mars" if answers_dict["Q2"] == "day" else "saturn")

    placeholder = "var data = {};"
    placeholder_poi = "var poi = {};"
    lines = []
    with open("radix.html", "r") as file:
        for line in file:
            if placeholder in line:
                line = placeholder.replace(placeholder, "\t\t\tvar data = " + str(data) + ";\n")
                print(line)
            elif placeholder_poi in line:
                line = placeholder_poi.replace(placeholder_poi, "\t\t\tvar poi = " + str(data_poi) + ";\n")
                print(line)
            lines.append(line)

    with open("temp.html", "w") as file:
        file.writelines(lines)



def tutorial_bot(step, name_inp=""):
    chat_log_scroll.config(state=NORMAL)
    if step == "NAME":
        chat_log_scroll.insert(tkinter.END, "Bot: What is your name?\n")
    elif step == "DOB":
        chat_log_scroll.insert(tkinter.END,
                               f"Bot: {name_inp}... What an interesting name. \nI'll be your Astro Teacher. Nice to "
                               f"meet you!\n")
        chat_log_scroll.insert(tkinter.END, "Bot: Let's cast your chart step-by-step.\n")
        chat_log_scroll.insert(tkinter.END, "Bot: What is your date of birth (MM/DD/YYYY)?\n")
    elif step == "HOUR":
        chat_log_scroll.insert(tkinter.END, "Bot: At what hour (this is needed for exact calculations)?\n")
    elif step == "MINUTE":
        chat_log_scroll.insert(tkinter.END, "Bot: At what minute?\n")
    elif step == "CITY":
        chat_log_scroll.insert(tkinter.END, "Bot: Which city were you born in?\n")
    elif step == "COUNTRY":
        chat_log_scroll.insert(tkinter.END, "Bot: What country were you born in?\n")
    chat_log_scroll.config(state=DISABLED)


def initiator():
    chat_log_scroll.config(state=NORMAL)
    chat_log_scroll.insert(tkinter.END, "Bot: Welcome to the Unfold Chat Bot!\nWould you like to find your\n"
                                        "own astrology birth chart (type \"Me\")"
                                        "\nor a celebrity's (type celebrity's full name\n(\"Brad Pitt\"))?\n")
    chat_log_scroll.config(state=DISABLED)


# Astrology Birth Chart
def display_birth_chart():
    global pimg
    hti = Html2Image()
    hti.screenshot(html_file="temp.html", save_as="out.png")
    area = (0, 0, 600, 680)
    img_bc = PIL.Image.open("out.png")
    img_crop = img_bc.crop(area)
    pimg = ImageTk.PhotoImage(img_crop)
    chart_canvas.itemconfig(chart_img, image=pimg)


# User input text box
user_entry = Entry(width=50, text="Enter Message Here...", bg=CHAT_BG)
send_button = Button(width=15, command=lambda: process_input(), text="Send")
# Waits until user hits the enter key before processing input
user_entry.bind("<Return>", lambda event: process_input())
user_entry.grid(column=1, row=1, pady=10)
send_button.grid(column=1, row=2, pady=10)

# Chat Log / Response Log
chat_log_scroll = scrolltxt.ScrolledText(width=50, height=34, state=DISABLED, bg=ENTRY_BG, foreground="black")
chat_log_scroll.tag_config('user_txt', foreground="red")
chat_log_scroll.grid(column=1, row=0)

# Astrology Birth Chart
default_img = PhotoImage(file="default_ing.png")
chart_canvas = Canvas(width=740, height=555, highlightthickness=0, bg="white")
chart_img = chart_canvas.create_image(390, 293, image=default_img)
chart_canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

initiator()

window.mainloop()

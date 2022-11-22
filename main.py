from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime
from Nutritionix import GetAnswer
from GoogleSheet import SpreadSheetDealer

WIDTH = 12
FONT = ("Helvetica", 11, "normal")
VALUES = ("Male", "Female")


class WorkoutTracker:
    def __init__(self, window):
        self.window = window
        self.window.title("Workout Tracker Application")
        self.window.geometry("600x600")
        # extra variables:
        self.today = datetime.now()
        self.current_workout = StringVar()
        self.current_gender = StringVar()
        self.current_weight = StringVar()
        self.current_height = StringVar()
        self.current_age = StringVar()
        self.current_date = StringVar()
        self.current_id = StringVar()
        self.workout_name = None
        self.duration = None
        self.calories = None

        # top frame:
        self.top_frame = Frame(self.window, bd=2, highlightthickness=2, relief=RIDGE, bg="white")
        self.top_frame.place(x=10, y=10, width=580, height=120)

        used_image = Image.open("./IMG/workout.jpg")
        used_photo = ImageTk.PhotoImage(used_image)
        self.image_label = Label(self.top_frame, image=used_photo, bg="white")
        self.image_label.image = used_photo
        self.image_label.pack()

        # personal info frame:
        self.info_frame = Frame(self.window, bd=2, highlightthickness=2, relief=RIDGE, pady=7)
        self.info_frame.place(x=10, y=130, width=300, height=200)

        self.workout = Label(self.info_frame, text="Workout Type", font=FONT, bd=1, highlightthickness=1, relief=RIDGE)
        self.workout.place(x=5, y=5, width=100, height=20)

        self.workout_entry = Entry(self.info_frame, font=FONT, justify="center", bd=1, highlightthickness=1,
                                   relief=RIDGE, textvariable=self.current_workout)
        self.workout_entry.place(x=110, y=5, width=180, height=20)

        self.gender = Label(self.info_frame, text="Gender", font=FONT, bd=1, highlightthickness=1, relief=RIDGE)
        self.gender.place(x=5, y=35, width=100, height=20)

        self.gender_entry = ttk.Combobox(self.info_frame, font=FONT, justify="center", textvariable=self.current_gender)
        self.gender_entry["values"] = VALUES
        self.gender_entry.current(0)
        self.gender_entry.place(x=110, y=35, width=180, height=20)

        self.weight = Label(self.info_frame, text="Weight-Kg", font=FONT, bd=1, highlightthickness=1, relief=RIDGE)
        self.weight.place(x=5, y=65, width=100, height=20)

        self.weight_entry = Entry(self.info_frame, font=FONT, justify="center", bd=1, highlightthickness=1,
                                  relief=RIDGE, textvariable=self.current_weight)
        self.weight_entry.place(x=110, y=65, width=180, height=20)

        self.height = Label(self.info_frame, text="Height-cm", font=FONT, bd=1, highlightthickness=1, relief=RIDGE)
        self.height.place(x=5, y=95, width=100, height=20)

        self.height_entry = Entry(self.info_frame, font=FONT, justify="center", bd=1, highlightthickness=1,
                                  relief=RIDGE, textvariable=self.current_height)
        self.height_entry.place(x=110, y=95, width=180, height=20)

        self.age = Label(self.info_frame, text="Age", font=FONT, bd=1, highlightthickness=1, relief=RIDGE)
        self.age.place(x=5, y=125, width=100, height=20)

        self.age_entry = Entry(self.info_frame, font=FONT, justify="center", bd=1, highlightthickness=1, relief=RIDGE,
                               textvariable=self.current_age)
        self.age_entry.place(x=110, y=125, width=180, height=20)

        self.id = Label(self.info_frame, text="Object ID", font=FONT, bd=1, highlightthickness=1, relief=RIDGE)
        self.id.place(x=5, y=155, width=100, height=20)

        self.id_entry = Entry(self.info_frame, font=FONT, justify="center", bd=1, highlightthickness=1, relief=RIDGE,
                              textvariable=self.current_id)
        self.id_entry.place(x=110, y=155, width=180, height=20)

        # calendar frame:
        self.calendar_frame = Frame(self.window, bd=2, highlightthickness=2, relief=RIDGE, pady=2, padx=2)
        self.calendar_frame.place(x=310, y=130, width=280, height=200)

        self.calendar_object = Calendar(self.calendar_frame, selectmode="day", year=self.today.year,
                                        month=self.today.month, day=self.today.day)
        self.calendar_object.place(x=0, y=0, width=268, height=188)

        # button frame:
        self.button_frame = Frame(self.window, bd=2, highlightthickness=2, relief=RIDGE, pady=1)
        self.button_frame.place(x=10, y=330, width=580, height=40)

        self.add_button = Button(self.button_frame, text="Calculate", font=FONT, width=WIDTH, bg="lime green",
                                 command=self.calculate_method)
        self.add_button.grid(row=0, column=0)

        self.update_button = Button(self.button_frame, text="Update", font=FONT, width=WIDTH,
                                    bg="deep sky blue", command=self.update_table)
        self.update_button.grid(row=0, column=1)

        self.delete_button = Button(self.button_frame, text="Delete", font=FONT, width=WIDTH, bg="orange",
                                    command=self.delete_from_table)
        self.delete_button.grid(row=0, column=2)

        self.refresh_button = Button(self.button_frame, text="Refresh", font=FONT, width=11, bg="cornflower blue",
                                     command=self.refresh_method)
        self.refresh_button.grid(row=0, column=3)

        self.close_button = Button(self.button_frame, text="Close", font=FONT, width=11, bg="tan",
                                   command=self.close_method)
        self.close_button.grid(row=0, column=4)

        # table frame:
        self.table_frame = Frame(self.window, bd=2, highlightthickness=2, relief=RIDGE)
        self.table_frame.place(x=10, y=370, width=580, height=220)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", backgroung="silver", foreground="black", rowheight=25, fieldbackground="silver")
        style.map("Treeview", background=[("selected", "medium sea green")])
        style.configure("Treeview.Heading", background="light steel blue", font=("Arial", 10, "bold"))

        self.table_object = ttk.Treeview(self.table_frame)

    # ================================ FUNCTIONALITY ===================================== #
    def close_method(self):
        self.window.destroy()

    def calculate_method(self):
        # communicate with nutritionix api:
        tool = GetAnswer()
        answer = tool.get_answer(workout=f"{self.current_workout.get()}", gender=f"{self.current_gender.get()}",
                                 weight=f"{self.current_weight.get()}", height=f"{self.current_height.get()}",
                                 age=f"{self.current_age.get()}")
        self.workout_name = answer["name"].title()
        self.duration = answer["duration_min"]
        self.calories = answer["nf_calories"]
        # communicate with Google sheet:
        hand = SpreadSheetDealer()
        hand.post_method(current_date=f"{self.today.date()}", exercise_type=f"{self.workout_name}",
                         duration_min=f"{self.duration}", calories=f"{self.calories}")

        messagebox.showinfo(title="Confirm", message="Calculation has completed Successfully, Refresh Data!")

    def clean_table(self):
        self.table_object.delete(*self.table_object.get_children())

    def refresh_method(self):
        self.clean_table()
        tool = SpreadSheetDealer()
        data = tool.get_method()
        self.table_object["column"] = list(data.columns)
        self.table_object["show"] = "headings"
        for column in self.table_object["column"]:
            self.table_object.heading(column, text=column)
        for column_name in self.table_object["column"]:
            self.table_object.column(column_name, width=110)
        old_row = data.to_numpy()
        new_row = [list(item) for item in old_row]
        for row in new_row:
            self.table_object.insert("", "end", values=row)
        self.table_object.pack(fill="both", expand=True)

    def delete_from_table(self):
        tool = SpreadSheetDealer()
        tool.delete_method(self.current_id.get())
        messagebox.showinfo(title="Confirm", message="Record has been deleted - Successfully, Refresh Data!")

    def update_table(self):
        # communicate with nutritionix api:
        tool = GetAnswer()
        answer = tool.get_answer(workout=f"{self.current_workout.get()}", gender=f"{self.current_gender.get()}",
                                 weight=f"{self.current_weight.get()}", height=f"{self.current_height.get()}",
                                 age=f"{self.current_age.get()}")
        self.workout_name = answer["name"].title()
        self.duration = answer["duration_min"]
        self.calories = answer["nf_calories"]

        hand = SpreadSheetDealer()
        hand.update_method(object_id=f"{self.current_id.get()}", new_current_date=f"{self.today.date()}",
                           new_exercise_type=f"{self.workout_name}", new_duration_min=f"{self.duration}",
                           new_calories=f"{self.calories}")
        messagebox.showinfo(title="Confirm", message="Record has been updated - Successfully, Refresh Data!")


def launch_program():
    app = Tk()
    WorkoutTracker(app)
    app.mainloop()


if __name__ == "__main__":
    launch_program()

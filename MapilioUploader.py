from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo, showerror
import sys
import tkinter as tk
import os.path
from export import export
from mapilio_kit.commands.process import Command as ProcessCommand
from mapilio_kit.commands.upload import Command as UploadCommand
from mapilio_kit.commands.sample_video import Command as SampleCommand
from mapilio_kit.commands.authenticate import Command as AuthCommand
from mapilio_kit.commands.gopro_360max import Command as GoPro360Command
from mapilio_kit.commands.process_csv import Command as ProcessCSV


list_tab = ["Login", "Uploader"]
tab_dict = {}


class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text + '\n')  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass


class MapilioKit(Tk):
    image_dict = {}

    def __init__(self):
        super().__init__()
        self.geometry("910x650")
        self.title("Mapilio Kit")
        self.resizable(False, False)

    def label(self, frame, selection):
        my_font = Font(
            family='Liberation Mono',
            weight='bold',
            slant='roman'
        )

        if not frame == tab_dict["Login"]:
            if selection in ["GoProMP4", "GoProMAX", "Time Laps", "Panoramic"]:
                self.path_s = Label(frame, text="Select or copy data directory", font=my_font, fg="black")
                self.path_s.place(x=150, y=150)

            self.path = Label(frame, text="Select data type", font=my_font, fg="black")
            self.path.place(x=150, y=80)
            if selection == "Panoramic":
                self.path_s = Label(frame, text="Select or copy csv data directory", font=my_font, fg="black")
                self.path_s.place(x=150, y=210)
    def canvas_(self, frame):
        if frame == tab_dict["Login"]:
            pass
        else:
            self.canvas = Canvas(frame, width=700, height=500)
            self.canvas.place(x=110, y=60)

    def back_ground(self, frame):
        name = f"{frame}-label"
        if frame == tab_dict["Login"]:
            self.back_ground_image = PhotoImage(file="images/background_login.png")
        else:
            self.back_ground_image = PhotoImage(file="images/background.png")

        self.image_dict[name] = self.back_ground_image
        self.back_ground_image_label = Label(frame, image=self.image_dict[name])
        self.back_ground_image_label.place(x=-2, y=-10)

    def entry(self, frame, selection):
        if frame == tab_dict["Login"]:
            self.e2 = Entry(frame, width=35, borderwidth=4)
            self.e2.place(x=365, y=263)
            self.e3 = Entry(frame, width=35, borderwidth=4, show='*')
            self.e3.place(x=365, y=310)
            self.e4 = Entry(frame, width=22, borderwidth=4)
            self.e4.place(x=468, y=359)
            self.e5 = Entry(frame, width=22, borderwidth=4)
            self.e5.place(x=468, y=404)
        else:
            if selection in ["GoProMP4", "GoProMAX", "Time Laps", "Panoramic"]:
                self.e1 = Entry(frame, width=60, borderwidth=4)
                self.e1.place(x=150, y=175)
            if selection == "Panoramic":
                self.e6 = Entry(frame, width=60, borderwidth=4)
                self.e6.place(x=150, y=235)


    def button(self, frame, selection):
        if frame == tab_dict["Login"]:
            self.path_button = Button(frame, text="Authenticate", border=0, command=lambda: MapilioKit.login(self))
            self.path_button.place(x=450, y=485)

        else:
            if selection in ["GoProMP4", "GoProMAX", "Time Laps", "Panoramic"]:
                name = f"{frame}-button"
                self.file_button_image = PhotoImage(file="images/file_button.png")
                self.image_dict[name] = self.file_button_image
                if selection == "Time Laps" or selection == "Panoramic":
                    self.path_button_s = Button(frame, image=self.image_dict[name], border=0,
                                                command=lambda: [MapilioKit.clear_entry(entry=self.e1),
                                                                 MapilioKit.get_path(entry=self.e1, operation="folder")])
                    self.path_button_s.place(x=648, y=172)

                else:
                    self.path_button_s = Button(frame, image=self.image_dict[name], border=0,
                                                command=lambda: [MapilioKit.clear_entry(entry=self.e1),
                                                                 MapilioKit.get_path(entry=self.e1, operation="file")])
                    self.path_button_s.place(x=648, y=172)
            if selection == "Panoramic":
                self.path_button_s = Button(frame, image=self.image_dict[name], border=0,
                                            command=lambda: [MapilioKit.clear_entry(entry=self.e6),
                                                             MapilioKit.get_path(entry=self.e6, operation="file")])

                self.path_button_s.place(x=648, y=233)
            self.button_upload = Button(frame, text="Upload", bg="light blue",
                                        command=lambda : MapilioKit.process_and_upload(self))
            self.button_upload.place(x=400, y=515)

    def selection(self, frame):
        if frame == tab_dict["Login"]:
            pass
        else:
            self.variable = StringVar(self)
            self.variable.set("Data Type")  # default value
            self.operation = OptionMenu(frame, self.variable, "GoProMP4", "GoProMAX", "Time Laps", "Panoramic",
                                        command=lambda x: [MapilioKit.destroy_widgets(self),
                                                           MapilioKit.button(self,
                                                                             frame=frame,
                                                                             selection=self.variable.get()),
                                                           MapilioKit.entry(self, frame=frame,
                                                                            selection=self.variable.get()),
                                                           MapilioKit.label(self, frame=frame,
                                                                            selection=self.variable.get())])
            self.operation.config(width=72, bg="light blue")
            self.operation.place(x=150, y=105)

    def terminal_out(self, frame):
        if frame == tab_dict["Login"]:
            pass
        else:
            self.log_widget = ScrolledText(frame, height=15, width=100, font=("consolas", "8", "normal"))
            self.log_widget.place(x=150, y=300)
            logger = PrintLogger(self.log_widget)
            sys.stdout = logger
            sys.stderr = logger

    @staticmethod
    def get_path(entry, operation):
        if operation == "file":
            filepath = filedialog.askopenfilename()
        if operation == "folder":
            filepath = filedialog.askdirectory()
        entry.insert(0, string=filepath)

    @staticmethod
    def clear_entry(entry):
        entry.delete(0, END)

    def destroy_widgets(self):
        try:
            if self.e1:
                self.e1.destroy()
                self.e6.destroy()
                self.path_button_s.destroy()
                self.path_s.destroy()
        except:
            pass

    def login(self):
        auth = AuthCommand()
        try:
            login = auth.run(
                vars_args={
                    "user_name": self.e2.get(),
                    "user_email": self.e2.get(),
                    "user_password": self.e3.get(),
                    "force_overwrite": True,
                }
            )
            if login:
                showinfo("Login", message="Authenticate is successful")
        except:
            showerror("Login", message="Please check your email and password")

    def process_and_upload(self):
        org_key = None if self.e5.get() == "" else self.e5.get()
        project_key = None if self.e4.get() == "" else self.e4.get()

        processing = ProcessCommand()
        uploading = UploadCommand()
        sampling = SampleCommand()
        gopro360max = GoPro360Command()

        output_dir = os.path.join(os.path.dirname(self.e1.get()), "Export")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if self.variable.get() == "GoProMP4":
            sampling.run(
                vars_args={
                    "video_import_path": os.path.join(self.e1.get()),
                    "import_path": os.path.join(output_dir),
                    "video_sample_interval": 1,
                    "force_overwrite": True
                }
            )
            processing.run(
                vars_args={
                    "import_path": os.path.join(output_dir),
                    "interpolate_directions": True,
                    "geotag_source": "gopro_videos",
                    "geotag_source_path": os.path.join(self.e1.get()),
                }
            )

            uploading.run(
                vars_args={
                    "import_path": os.path.join(output_dir),
                    "user_name": self.e2.get(),
                    "organization_key": org_key,
                    "project_key": project_key,
                }
            )

            showinfo("Upload", message="Upload is successful")
        if self.variable.get() == "Time Laps":
            processing.run(vars_args={"import_path": os.path.join(self.e1.get())})
            uploading.run(
                vars_args={
                    "import_path": os.path.join(self.e1.get()),
                    "user_name": self.e2.get(),
                    "organization_key": org_key,
                    "project_key": project_key,
                }
            )
        if self.variable.get() == "Panoramic":
            export(csv_path=os.path.join(self.e6.get()),
                   images_dir=os.path.join(self.e1.get()),
                   output_geojson_name=os.path.join(os.path.join(self.e1.get(), "out_geojson")),
                   output_csv_name=os.path.join(os.path.join(self.e1.get(), "out_csv.csv")))

            laydbugPanoroma = ProcessCSV()

            laydbugPanoroma.run(
                vars_args={
                    'import_path': os.path.join(self.e1.get()),
                    'csv_path': os.path.join(os.path.join(self.e1.get(), "out_csv.csv"))
                }
            )
            uploading.run(
                vars_args={
                    "import_path": os.path.join(self.e1.get()),
                    "user_name": self.e2.get(),
                    "organization_key": org_key,
                    "project_key": project_key,
                }
            )
        if self.variable.get() == "GoProMAX":
            gopro360max.run(
                vars_args={
                    'video_file': os.path.join(self.e1.get()),
                    'frame_rate': 1,
                    'output_folder': output_dir,
                    'quality': "1",
                    'bin_dir': os.path.join(os.getcwd(), 'bin')
                }
            )
            processing.run(
                vars_args={"import_path": os.path.join(output_dir, "frames")}
            )

            uploading.run(
                vars_args={
                    "import_path": os.path.join(output_dir, "frames"),
                    "user_name": self.e2.get(),
                    "organization_key": org_key,
                    "project_key": project_key,
                }
            )


if __name__ == "__main__":
    root = MapilioKit()

    # add tab controller
    tabControl = ttk.Notebook(root)

    # add tabs
    for tab in list_tab:
        tab_dict[tab] = tk.Frame(tabControl)
        tabControl.add(tab_dict[tab], text=tab)

    # pack tabs
    for tab in list_tab:
        root.back_ground(frame=tab_dict[tab])
        root.canvas_(frame=tab_dict[tab])
        root.selection(frame=tab_dict[tab])
        root.label(frame=tab_dict[tab], selection=False)
        root.entry(frame=tab_dict[tab], selection=False)
        root.button(frame=tab_dict[tab], selection=False)
        root.terminal_out(frame=tab_dict[tab])

    # pack tabcontrol
    tabControl.pack(expand=1, fill="both")

    # main loop
    root.mainloop()

## self.e1.get() ile path alıcaz
## self.e2.get()  ve  self.e3.get() ile username ve password alıcaz

import os

import wx
import subprocess
from PIL import Image
#to be added: navigation with arrows!!!!

class MangaListFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Manga List", size=(500, 400))




        # Create a panel to hold the controls
        panel = wx.Panel(self)



        # Create a list control to display the manga titles and their details
        self.manga_list = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.manga_list.InsertColumn(0, "Manga")
        self.manga_list.InsertColumn(1, "Last Chapter")
        self.manga_list.InsertColumn(2, "Notes")
        for i in range(10):
            self.manga_list.Append(["Manga "+str(i), "Chapter 10", "Some notes about Manga "+str(i)])

        self.manga_list.SetColumnWidth(2, 200)

        # Create a search box to filter the manga titles
        self.search_box = wx.SearchCtrl(panel)
        self.search_box.ShowCancelButton(True)
        self.search_box.Bind(wx.EVT_TEXT, self.on_search)

        # Bind an event for activating a manga item
        self.manga_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_manga_activated)

        # Add the controls to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.search_box, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.manga_list, 1, wx.EXPAND | wx.ALL, 5)

        # Set the sizer for the panel
        panel.SetSizer(sizer)

    def on_arrow_clicked(self, event):
        print("Yikes!")

    def on_manga_activated(self, event):
        # Get the index of the activated item
        index = event.GetIndex()

        # Get the text of the activated item (manga name)
        manga_name = self.manga_list.GetItemText(index)
        print(manga_name)

        # Close the current frame
        self.Close()

        # Launch a new Python file and pass the manga name as an argument

        #subprocess.run(["python", "search_box_chapters.py", manga_name])

        # Open a new frame with the manga name printed
        #new_frame = wx.Frame(None, title="Selected Manga")
        #panel = wx.Panel(new_frame)
        #text = wx.StaticText(panel, label=f"Selected manga: {manga_name}")

        # Add the text to the panel
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(text, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        #panel.SetSizer(sizer)

        #new_frame.Show()

        # Create the application and show the main frame
        app = wx.App()
        # unnecessary , exists just to avoid Process finished with exit code -1073740771 (0xC000041D)
        if len(manga_name) > 1:
            # Get the manga name passed as a command-line argument
            frame = ChapterListFrame(None, manga_name)
        else:
            # If no arguments are provided, set a default manga name
            manga_name = "No Manga Name"

        frame.Show()

        # Run the main loop
        app.MainLoop()

    def on_search(self, event):
        search_term = event.GetString()
        if search_term == "":
            for i in range(self.manga_list.GetItemCount()):
                self.manga_list.SetItemState(i, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
                self.manga_list.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        else:
            for i in range(self.manga_list.GetItemCount()):
                if search_term.lower() not in self.manga_list.GetItemText(i).lower():
                    self.manga_list.SetItemState(i, 0, wx.LIST_STATE_FOCUSED | wx.LIST_STATE_SELECTED)
                else:
                    self.manga_list.SetItemState(i, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
                    self.manga_list.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)



class ChapterListFrame(wx.Frame):
    def __init__(self, parent,manga_name):

                self.manga_name=manga_name

                super().__init__(parent, title="Chapters List of {}".format(manga_name), size=(500, 400))

                # Create a panel to hold the controls
                panel = wx.Panel(self)
                #text = wx.StaticText(panel, label=f"Selected manga: {manga_name}")

                # Create a list control to display the manga titles and their details
                self.chapter_list = wx.ListCtrl(panel, style=wx.LC_REPORT)
                self.chapter_list.InsertColumn(0, "Title")
                self.chapter_list.InsertColumn(1, "No.")
                self.chapter_list.InsertColumn(2, "Notes")
                for i in range(10):
                    self.chapter_list.Append(["Chapter " + str(i), "title", "Some notes about Chapter " + str(i)])

                self.chapter_list.SetColumnWidth(2, 200)

                # Create a search box to filter the manga titles
                self.search_box = wx.SearchCtrl(panel)
                self.search_box.ShowCancelButton(True)
                self.search_box.Bind(wx.EVT_TEXT, self.on_search)

                # Bind an event for activating a manga item
                self.chapter_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_chapter_activated)

                # Add the controls to a sizer
                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(self.search_box, 0, wx.EXPAND | wx.ALL, 5)
                sizer.Add(self.chapter_list, 1, wx.EXPAND | wx.ALL, 5)

                # Create buttons for back, forward, and pause
                back_button = wx.Button(panel, label="Back")
                forward_button = wx.Button(panel, label="Forward")
                pause_button = wx.Button(panel, label="Pause")

                # Bind button events to functions
                back_button.Bind(wx.EVT_BUTTON, self.on_back)
                forward_button.Bind(wx.EVT_BUTTON, self.on_forward)
                pause_button.Bind(wx.EVT_BUTTON, self.on_pause)

                # Create a horizontal sizer for the buttons
                buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
                buttons_sizer.Add(back_button, 0, wx.ALIGN_LEFT | wx.ALL, 5)
                buttons_sizer.Add(forward_button, 0, wx.ALIGN_LEFT | wx.ALL, 5)
                buttons_sizer.Add(pause_button, 0, wx.ALIGN_LEFT | wx.ALL, 5)

                # Add the controls to a sizer
                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(buttons_sizer, 0, wx.EXPAND | wx.ALL, 5)
                sizer.Add(self.search_box, 0, wx.EXPAND | wx.ALL, 5)
                sizer.Add(self.chapter_list, 1, wx.EXPAND | wx.ALL, 5)

                # Set the sizer for the panel
                panel.SetSizer(sizer)

    def on_forward(self, event):
        print("Yikes!")

    def on_pause(self, event):
        print("Yikes!")

    def on_arrow_clicked(self, event):
        print("Yikes!")

    def on_back(self, event):
        self.Close()
        # Create the application and show the main frame
        app = wx.App()
        frame = MangaListFrame(None)

        frame.Show()

        # Run the main loop
        app.MainLoop()

    def on_search(self, event):
        search_term = event.GetString()
        if search_term == "":
            for i in range(self.chapter_list.GetItemCount()):
                self.chapter_list.SetItemState(i, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
                self.chapter_list.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        else:
            for i in range(self.chapter_list.GetItemCount()):
                if search_term.lower() not in self.chapter_list.GetItemText(i).lower():
                    self.chapter_list.SetItemState(i, 0, wx.LIST_STATE_FOCUSED | wx.LIST_STATE_SELECTED)
                else:
                    self.chapter_list.SetItemState(i, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
                    self.chapter_list.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def on_chapter_activated(self, event):
        #print("whoops")
        # Get the index of the activated item

        index = event.GetIndex()

        # Get the text of the activated item (manga name)
        chapter_name = self.chapter_list.GetItemText(index)


        # Close the current frame
        self.Close()

        # Launch a new Python file and pass the manga name as an argument

        # subprocess.run(["python", "search_box_chapters.py", manga_name])

        # Open a new frame with the manga name printed
        # new_frame = wx.Frame(None, title="Selected Manga")
        # panel = wx.Panel(new_frame)
        # text = wx.StaticText(panel, label=f"Selected manga: {manga_name}")

        # Add the text to the panel
        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(text, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # panel.SetSizer(sizer)

        # new_frame.Show()

        # Create the application and show the main frame
        app = wx.App()
        # unnecessary , exists just to avoid Process finished with exit code -1073740771 (0xC000041D)
        if len(chapter_name) > 1:
            # Get the manga name passed as a command-line argument
            #name=chapter_name+"of manga:"+self.manga_name
            frame = PictureFrame(None, chapter_name,self.manga_name)
        else:
            # If no arguments are provided, set a default manga name
            frame=PictureFrame(None,"no chapter found",self.manga_name)

        frame.Show()

        # Run the main loop
        app.MainLoop()

class PictureViewerFrame(wx.Frame):
    def __init__(self, parent, picture_path):
        super().__init__(parent, title="Picture Viewer", size=(500, 500))

        self.picture_paths = []
        self.current_index = 0
        self.zoom_factor = 1.0

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.picture_label = wx.StaticText(panel, label="")
        sizer.Add(self.picture_label, 0, wx.CENTER | wx.ALL, 10)

        self.picture_panel = wx.Panel(panel)
        self.picture_panel.SetBackgroundColour(wx.WHITE)
        self.picture_panel.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.picture_panel.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)
        self.picture_panel.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.picture_sizer = wx.BoxSizer(wx.VERTICAL)
        self.picture_panel.SetSizer(self.picture_sizer)
        sizer.Add(self.picture_panel, 1, wx.EXPAND | wx.ALL, 10)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        previous_button = wx.Button(panel, label="Previous")
        previous_button.Bind(wx.EVT_BUTTON, self.on_previous_button)
        button_sizer.Add(previous_button, 0, wx.ALL, 10)

        next_button = wx.Button(panel, label="Next")
        next_button.Bind(wx.EVT_BUTTON, self.on_next_button)
        button_sizer.Add(next_button, 0, wx.ALL, 10)

        zoom_in_button = wx.Button(panel, label="Zoom In")
        zoom_in_button.Bind(wx.EVT_BUTTON, self.on_zoom_in_button)
        button_sizer.Add(zoom_in_button, 0, wx.ALL, 10)

        zoom_out_button = wx.Button(panel, label="Zoom Out")
        zoom_out_button.Bind(wx.EVT_BUTTON, self.on_zoom_out_button)
        button_sizer.Add(zoom_out_button, 0, wx.ALL, 10)

        sizer.Add(button_sizer, 0, wx.CENTER)

        panel.SetSizer(sizer)

        self.load_pictures()

        if picture_path:
            self.show_picture(picture_path)

    def load_pictures(self):
        folder_path = "C:/Users/james/Desktop/fotos"  # Replace with the actual folder path
        self.picture_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)
                               if file_name.endswith(".jpg")]

    def show_picture(self, picture_path):
        image = Image.open(picture_path)
        image = image.resize((400, 400))
        self.current_image = image
        self.update_picture()

        self.current_index = self.picture_paths.index(picture_path)
        self.update_picture_label()

    def update_picture(self):
        zoomed_image = self.current_image.resize((int(self.current_image.width * self.zoom_factor),
                                                  int(self.current_image.height * self.zoom_factor)))
        bitmap = wx.Bitmap.FromBufferRGBA(zoomed_image.width, zoomed_image.height,
                                          zoomed_image.convert("RGBA").tobytes())

        picture = wx.StaticBitmap(self.picture_panel, bitmap=bitmap)
        self.picture_sizer.Clear(True)
        self.picture_sizer.Add(picture, 1, wx.EXPAND)
        self.picture_panel.Layout()

    def update_picture_label(self):
        total_pictures = len(self.picture_paths)
        current_picture = self.current_index + 1
        self.picture_label.SetLabel(f"Picture {current_picture} of {total_pictures}")
        self.Layout()

    def on_previous_button(self, event):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.picture_paths) - 1
        self.show_picture(self.picture_paths[self.current_index])

    def on_next_button(self, event):
        self.current_index += 1
        if self.current_index >= len(self.picture_paths):
            self.current_index = 0
        self.show_picture(self.picture_paths[self.current_index])

    def on_zoom_in_button(self, event):
        self.zoom_factor *= 1.1
        self.update_picture()

    def on_zoom_out_button(self, event):
        self.zoom_factor /= 1.1
        self.update_picture()

    def on_mouse_down(self, event):
        self.last_mouse_position = event.GetPosition()

    def on_mouse_up(self, event):
        self.last_mouse_position = None

    def on_mouse_move(self, event):
        if event.Dragging() and event.LeftIsDown() and self.last_mouse_position:
            current_mouse_position = event.GetPosition()
            delta = current_mouse_position - self.last_mouse_position
            self.last_mouse_position = current_mouse_position

            self.current_image = self.current_image.transform(
                self.current_image.size, Image.AFFINE, (1, 0, delta.x, 0, 1, delta.y)
            )
            self.update_picture()


class PictureFrame(wx.Frame):
    def __init__(self, parent, manga_name, chapter_name):
        super().__init__(parent, title=f"Pictures for {chapter_name} of {manga_name}", size=(800, 600))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        scrolled_window = wx.ScrolledWindow(panel)
        scrolled_window.SetScrollRate(10, 10)

        grid_sizer = wx.GridSizer(rows=0, cols=5, hgap=10, vgap=10)

        folder_path = "C:/Users/james/Desktop/fotos"  # Replace with the actual folder path
        picture_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)
                         if file_name.endswith(".jpg")]

        for picture_path in picture_paths:
            image = Image.open(picture_path)
            image = image.resize((150, 150))
            image_data = image.convert("RGBA").tobytes()
            bitmap = wx.Bitmap.FromBufferRGBA(image.size[0], image.size[1], image_data)

            picture_panel = wx.Panel(scrolled_window)
            picture_panel.SetBackgroundColour(wx.WHITE)

            picture_button = wx.BitmapButton(picture_panel, bitmap=bitmap)
            picture_button.Bind(wx.EVT_BUTTON, lambda event, path=picture_path: self.on_picture_button(event, path))

            title_label = wx.StaticText(picture_panel, label=os.path.basename(picture_path))

            picture_sizer = wx.BoxSizer(wx.VERTICAL)
            picture_sizer.Add(picture_button, 1, wx.EXPAND | wx.ALL, border=10)
            picture_sizer.Add(title_label, 0, wx.ALIGN_CENTER)

            picture_panel.SetSizer(picture_sizer)
            grid_sizer.Add(picture_panel, 0, wx.EXPAND)

        scrolled_sizer = wx.BoxSizer(wx.VERTICAL)
        scrolled_sizer.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, 10)

        scrolled_window.SetSizer(scrolled_sizer)
        scrolled_window.SetVirtualSize(grid_sizer.GetMinSize())
        scrolled_window.SetScrollbars(10, 10, *grid_sizer.GetMinSize())

        sizer.Add(scrolled_window, 1, wx.EXPAND)
        panel.SetSizer(sizer)

    def on_picture_button(self, event, picture_path):
        picture_frame = PictureViewerFrame(self, picture_path)
        picture_frame.Show()
# Create the application and show the main frame
app = wx.App()
frame = MangaListFrame(None)
frame.Show()

# Run the main loop
app.MainLoop()
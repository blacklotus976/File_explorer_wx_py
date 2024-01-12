import wx
import os
from PIL import Image


import wx
import os
from PIL import Image


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
        self.picture_panel.Bind(wx.EVT_PAINT, self.on_paint)
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
        self.current_image = image
        self.current_index = self.picture_paths.index(picture_path)
        self.update_picture_label()
        self.Refresh()

    def update_picture_label(self):
        total_pictures = len(self.picture_paths)
        current_picture = self.current_index + 1
        self.picture_label.SetLabel(f"Picture {current_picture} of {total_pictures}")
        self.Layout()

    def update_picture(self):
        self.Refresh()

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

    def on_paint(self, event):
        dc = wx.PaintDC(self.picture_panel)
        dc.Clear()
        image = self.current_image.copy()
        image.thumbnail((self.picture_panel.GetSize()[0], self.picture_panel.GetSize()[1]))
        image = image.resize((int(image.width * self.zoom_factor), int(image.height * self.zoom_factor)))

        # Save the PIL Image to a temporary file
        temp_file_path = "temp_image.jpg"
        image.save(temp_file_path)

        # Load the temporary file into a wx.Image
        wx_image = wx.Image(temp_file_path, wx.BITMAP_TYPE_ANY)

        # Remove the temporary file
        os.remove(temp_file_path)

        # Convert the wx.Image to a wx.Bitmap
        wx_bitmap = wx.Bitmap(wx_image)

        dc.DrawBitmap(wx_bitmap, 0, 0)

    # def on_paint(self, event):
    #     dc = wx.PaintDC(self.picture_panel)
    #     dc.Clear()
    #     image = self.current_image.copy()
    #     image.thumbnail((self.picture_panel.GetSize()[0], self.picture_panel.GetSize()[1]))
    #     image = image.resize((int(image.width * self.zoom_factor), int(image.height * self.zoom_factor)))
    #     dc.DrawBitmap(wx.BitmapFromImage(image), 0, 0)

    def on_mouse_down(self, event):
        self.last_mouse_position = event.GetPosition()

    def on_mouse_up(self, event):
        self.last_mouse_position = None

    def on_mouse_move(self, event):
        if event.Dragging() and event.LeftIsDown() and self.last_mouse_position:
            current_mouse_position = event.GetPosition()
            delta = current_mouse_position - self.last_mouse_position
            self.last_mouse_position = current_mouse_position

            image = self.current_image.copy()
            image.thumbnail((self.picture_panel.GetSize()[0], self.picture_panel.GetSize()[1]))
            image = image.resize((int(image.width * self.zoom_factor), int(image.height * self.zoom_factor)))
            image = image.transform(image.size, Image.AFFINE, (1, 0, delta.x, 0, 1, delta.y))

            self.current_image = image
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

        self.Layout()

    def on_picture_button(self, event, picture_path):
        picture_frame = PictureViewerFrame(self, picture_path)
        picture_frame.Show()


if __name__ == "__main__":
    app = wx.App()
    frame = PictureFrame(None, "Manga Name", "Chapter Name")
    frame.Show()
    app.MainLoop()



if __name__ == "__main__":
    app = wx.App()
    frame = PictureFrame(None, "Manga Name", "Chapter Name")
    frame.Show()
    app.MainLoop()

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
        scrolled_window.SetScrollbars(10, 10, grid_sizer.GetMinSize()[0] // 10, grid_sizer.GetMinSize()[1] // 10)

        sizer.Add(scrolled_window, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

    def on_picture_button(self, event, picture_path):
        viewer_frame = PictureViewerFrame(self, picture_path)
        viewer_frame.Show()


if __name__ == "__main__":
    app = wx.App()
    frame = PictureFrame(None, "Manga Name", "Chapter Name")
    frame.Show()
    app.MainLoop()
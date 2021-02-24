#!/usr/bin/env python3
"""
@project: python3
@file: bookmarks_tk
@author: mike
@time: 2021/2/24
 
@function:
"""
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import os
import sys
import webbrowser
import pickle


class MainWindow:
    def __init__(self, parent):
        self.parent = parent

        # Attribute to store
        self.filename = None
        self.dirty = False
        self.data = {}

        # Menubar
        menubar = tkinter.Menu(self.parent)
        self.parent['menu'] = menubar

        # File menu
        file_menu = tkinter.Menu(menubar)
        for label, command, shortcut_text, shortcut in (
                ('New...', self.file_new, 'Ctrl+N', '<Control-n>'),
                ('Open...', self.file_open, 'Ctrl+O', '<Control-o>'),
                ('Save', self.file_save, 'Ctrl+S', '<Control-s>'),
                (None, None, None, None),
                ('Quit', self.file_quit, 'Ctrl+Q', '<Control-q>')
        ):
            if label is None:
                file_menu.add_separator()
            else:
                file_menu.add_command(label=label,
                                      underline=0,
                                      command=command,
                                      accelerator=shortcut_text)
                self.parent.bind(shortcut, command)
        menubar.add_cascade(label='File',
                            menu=file_menu,
                            underline=0)

        # Edit menu
        edit_menu = tkinter.Menu(menubar)
        for label, command, shortcut_text, shortcut in (
                ("Add...", self.edit_add, "Ctrl+A", "<Control-a>"),
                ("Edit...", self.edit_edit, "Ctrl+E", "<Control-e>"),
                ("Delete...", self.edit_delete, "Delete", "<Delete>"),
                (None, None, None, None),
                ("Show Web Page...", self.edit_show_web_page, "Ctrl+W", "<Control-w>")
        ):
            if label is None:
                edit_menu.add_separator()
            else:
                edit_menu.add_command(label=label,
                                      underline=0,
                                      command=command,
                                      accelerator=shortcut_text)
                self.parent.bind(shortcut, command)
        menubar.add_cascade(label='Edit',
                            menu=edit_menu,
                            underline=0)

        # toolbar
        frame = tkinter.Frame(self.parent)
        self.tool_bar_images = []
        toolbar = tkinter.Frame(frame)
        for image, command in (
                ('images/filenew.gif', self.file_new),
                ('images/fileopen.gif', self.file_open),
                ('images/filesave.gif', self.file_save),
                ("images/editadd.gif", self.edit_add),
                ("images/editedit.gif", self.edit_edit),
                ("images/editdelete.gif", self.edit_delete),
                ("images/editshowwebpage.gif", self.edit_show_web_page)):
            image = os.path.join(os.path.dirname(__file__), image)
            try:
                image = tkinter.PhotoImage(file=image)
                self.tool_bar_images.append(image)
                button = tkinter.Button(toolbar,
                                        image=image,
                                        command=command)
                button.grid(row=0, column=len(self.tool_bar_images) - 1)
            except tkinter.TclError as err:
                print(err)
        toolbar.grid(row=0, column=0, columnspan=2, sticky=tkinter.NW)

        # List box, scroll bar
        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        # List box, scrollbar, both widgets are kept in sync
        self.listBox = tkinter.Listbox(frame, yscrollcommand=scrollbar.set)
        self.listBox.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.listBox.focus_set()
        # List box, scrollbar, both widgets are kept in sync
        scrollbar['command'] = self.listBox.yview
        scrollbar.grid(row=1, column=1, sticky=tkinter.NS)

        # Status bar
        self.statusbar = tkinter.Label(frame, text='Ready...', anchor=tkinter.W)
        self.statusbar.after(5000, self.clear_status_bar)
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky=tkinter.EW)

        # locate the frame
        frame.grid(row=0, column=0, sticky=tkinter.NSEW)

        frame.columnconfigure(0, weight=999)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=999)
        frame.rowconfigure(2, weight=1)

        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        self.parent.geometry('{}x{}+{}+{}'.format(400, 500, 0, 50))
        self.parent.title('Bookmarks -Unnamed')

    def clear_status_bar(self):
        self.statusbar['text'] = ''

    def file_new(self, *ignore):
        if not self.okay_to_continue():
            return
        self.listBox.delete(0, tkinter.END)
        self.dirty = False
        self.filename = None
        self.data = {}
        self.parent.title('Bookmarks - Unnamed')

    def okay_to_continue(self):
        if not self.dirty:
            return True
        reply = tkinter.messagebox.askyesnocancel(
            'Bookmarks - Unsaved Changes',
            'Save unsaved change?',
            parent=self.parent
        )
        if reply is None:  # Cancel
            return False
        if reply:  # Save
            return self.file_save()
        # Don't save
        return True

    def file_save(self, *ignore):
        if self.filename is None:
            filename = tkinter.filedialog.asksaveasfilename(
                title='Bookmarks - Save File',
                initialdir='.',
                filetypes=[('Bookmarks file', '*.bmf')],
                defaultextension='.bmf',
                parent=self.parent)

            if not filename:
                return False

            self.filename = filename
            if not self.filename.endswith('.bmf'):
                self.filename += '.bmf'

        try:
            with open(self.filename, 'wb') as fh:
                pickle.dump(self.data, fh, pickle.HIGHEST_PROTOCOL)
            self.dirty = False
            self.set_status_bar(f'Saved {len(self.data)} to {self.filename}')
            self.parent.title(f'Bookmarks - {os.path.basename(self.filename)}')
        except (EnvironmentError, pickle.PickleError) as err:
            tkinter.messagebox.showwarning('Bookmarks - Error',
                                           f'Failed to save {self.filename}:\n{err}',
                                           parent=self.parent)
        return True

    def set_status_bar(self, text, timeout=5000):
        self.statusbar['text'] = text
        if timeout:
            self.statusbar.after(timeout, self.clear_status_bar)

    def file_open(self, *ignore):
        if not self.okay_to_continue():
            return

        dir_ = (os.path.dirname(self.filename) if self.filename else '.')
        filename = tkinter.filedialog.askopenfilename(
            title='Bookmarks - Open File',
            initialdir=dir_,
            filetypes=[('Bookmarks files', '*.bmf')],
            defaultextension='.bmf',
            parent=self.parent
        )
        if filename:
            self.load_file(filename)

    def load_file(self, filename):
        self.filename = filename
        self.listBox.delete(0, tkinter.END)
        self.dirty = False
        try:
            with open(self.filename, 'rb') as fh:
                self.data = pickle.load(fh)
            for name in sorted(self.data, key=str.lower):
                self.listBox.insert(tkinter.END, name)
            self.set_status_bar(f'Loaded {self.listBox.size()} bookmarks from {self.filename}')
            self.parent.title(f'Bookmarks - {os.path.basename(self.filename)}')
        except (EnvironmentError, pickle.PickleError) as err:
            tkinter.messagebox.showwarning(
                'Bookmarks - Error',
                f'Failed to load {self.filename}:\n{err}',
                parent=self.parent
            )

    def file_quit(self, event=None):
        if self.okay_to_continue():
            self.parent.destroy()

    def edit_add(self, *ignore):
        form = AddEditForm(self.parent)
        if form.accepted and form.name:
            self.data[form.name] = form.url
            self.listBox.delete(0, tkinter.END)
            for name in sorted(self.data, key=str.lower):
                self.listBox.insert(tkinter.END, name)
            self.dirty = True

    def edit_edit(self, *ignore):
        indexes = self.listBox.curselection()
        # Only one index need to be supplied
        if not indexes or len(indexes) > 1:
            return

        index = indexes[0]
        name = self.listBox.get(index)
        form = AddEditForm(self.parent, name, self.data[name])
        if form.accepted and form.name:
            self.data[form.name] = form.url
            if form.name != name:
                del self.data[name]
                self.listBox.delete(0, tkinter.END)
                for name in sorted(self.data, key=str.lower):
                    self.listBox.insert(tkinter.END, name)
            self.dirty = True

    def edit_delete(self, *ignore):
        indexes = self.listBox.curselection()
        if not indexes or len(indexes) > 1:
            return
        index = indexes[0]
        name = self.listBox.get(index)
        if tkinter.messagebox.askyesno(
                'Bookmarks - Delete',
                f'Delete "{name}"?'):
            self.listBox.delete(index)
            self.listBox.focus_set()
            del self.data[name]
            self.dirty = True

    def edit_show_web_page(self, *ignore):
        indexes = self.listBox.curselection()
        if not indexes or len(indexes) > 1:
            return
        index = indexes[0]
        url = self.data[self.listBox.get(index)]
        webbrowser.open_new_tab(url)


class AddEditForm(tkinter.Toplevel):
    def __init__(self, parent, name=None, url=None):
        super().__init__(parent)
        self.parent = parent
        self.accepted = False
        # To inform the parent window that
        # this window must always appear on top of the parent.
        self.transient(self.parent)
        self.title('Bookmarks - ' + 'Edit' if name else 'Add')

        self.nameVar = tkinter.StringVar()
        if name:
            self.nameVar.set(name)
        self.urlVar = tkinter.StringVar()
        self.urlVar.set(url if url else 'http://')

        frame = tkinter.Frame(self)
        name_label = tkinter.Label(frame, text='Name:', underline=0)
        name_entry = tkinter.Entry(frame, textvariable=self.nameVar)
        name_entry.focus_set()
        url_label = tkinter.Label(frame, text='URL:', underline=0)
        url_entry = tkinter.Entry(frame, textvariable=self.urlVar)
        ok_button = tkinter.Button(frame, text='OK', command=self.ok)
        cancel_button = tkinter.Button(frame, text='Cancel', command=self.close)

        name_label.grid(row=0, column=0, sticky=tkinter.W, padx=3, pady=3)
        name_entry.grid(row=0, column=1, columnspan=3, sticky=tkinter.EW, padx=3, pady=3)
        url_label.grid(row=1, column=0, sticky=tkinter.W, padx=3, pady=3)
        url_entry.grid(row=1, column=1, columnspan=3, sticky=tkinter.EW, padx=3, pady=3)
        ok_button.grid(row=2, column=2, sticky=tkinter.EW, padx=3, pady=3)
        cancel_button.grid(row=2, column=3, sticky=tkinter.EW, padx=3, pady=3)

        frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        frame.columnconfigure(1, weight=1)
        window = self.winfo_toplevel()
        window.columnconfigure(0, weight=1)

        self.bind("<Alt-n>", lambda *ignore: name_entry.focus_set())
        self.bind("<Alt-u>", lambda *ignore: url_entry.focus_set())
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.close)
        self.protocol("WM_DELETE_WINDOW", self.close)
        # The calls to grab_set() and wait_window() are both needed
        # to turn the window into a modal dialog.
        self.grab_set()
        self.wait_window(self)

    def ok(self, enven=None):
        self.name = self.nameVar.get()
        self.url = self.urlVar.get()
        self.accepted = True
        self.close()

    def close(self, event=None):
        self.parent.focus_set()
        self.destroy()


application = tkinter.Tk()
path = os.path.join(os.path.dirname(__file__), 'images/')
if sys.platform.startswith('win'):
    icon = path + 'bookmark.ico'
    application.iconbitmap(icon, default=icon)
else:
    application.iconbitmap('@' + path + 'bookmark.xbm')
window = MainWindow(application)
application.protocol('WM_DELETE_WINDOW', window.file_quit)
application.mainloop()

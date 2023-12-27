#!/usr/bin/python3

'''
name LADSPA-Tester
license GNU GPL v3
written by SANTA no Mix
https://ameblo.jp/math-physics/entry-12834252800.html
https://github.com/SantaNoMix/
'''

import tkinter as tk
from tkinter import ttk
import customtkinter
from CTkListbox import *
import os
import re
import datetime
import value as g
import plugins_patch

# FONT_TYPE = "Arial"
FONT_TYPE = "M+ 2p light"

path = '/usr/lib/ladspa'
alsa_output = 'alsa_output.default'
srate = '44100'
to_range = '100'
toggled = '[0 to 100]'
date = datetime.date.today()
pulse_sleep = 0 # os.system("sleep (pulse_sleep)")
win_no = 0
is_file = os.path.isfile("../.config/pulse/default.pa")
if is_file:
    os.system("mv ../.config/pulse/default.pa ../.config/pulse/default.pa-{}-bak".format(date))
else:
    pass
os.system("cp /etc/pulse/default.pa ../.config/pulse/default.pa")
os.system("sed -i \"s/#load-module module-alsa-sink/load-module module-alsa-sink/g\" ../.config/pulse/default.pa")
os.system("sed -i \"s/load-module module-switch-on-port-available/#load-module module-switch-on-port-available/g\" ../.config/pulse/default.pa")
#os.system("ps ax | grep \'pluseaudio\'")
os.system("sleep 2")
os.system("pulseaudio -k")
os.system("sleep 1")
os.system("pulseaudio --start")

class Toplevelwindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("960x480")
        self.title(plugin_file)
        self.frame = customtkinter.CTkScrollableFrame(self, width=900, height=300)
        self.frame.grid(row=1, column=0, padx=(20, 20), sticky="nsew")

        global plugin_name_txt
        global page
        with open("tmp/tmp_s." + str(page).zfill(2), "r") as text:
            plugin_txt = text.readlines()
            plugin_name_txt = [s.replace("[", "").replace("]", "") for s in plugin_txt]
            plugin_name_txt = [s.replace("Plugin Name: ", "").replace(" ", " ").replace("\n", "") for s in plugin_txt]

        self.label = customtkinter.CTkLabel(self, text=plugin_name_txt[0], font=(FONT_TYPE, 16))
        self.label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")
        self.textbox = customtkinter.CTkTextbox(self, width=460, height=100, font=(FONT_TYPE, 16))
        self.textbox.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.textbox.insert("0.0", "\n")
        global plugin_info
        self.textbox.insert(tk.END, plugin_info)
        global cannel_var
        channel_var = tk.StringVar(value="sinks: None")

        def combobox_callback(choice):
            pass

        global io_var
        if io_var == 0:
            code = "self.combobox{} = customtkinter.CTkComboBox(self, values=[\"pactl list sinks:0\", \"pactl list sinks:1\", \"pulseaudio:restart\"], command=combobox_callback, variable=channel_var, width=167, border_width=1, font=(FONT_TYPE, 14), dropdown_font=(FONT_TYPE, 14))".format(process_pid[0])
            exec(code)
        elif io_var == 1:
            code = "self.combobox{} = customtkinter.CTkComboBox(self, values=[\"1ch:pactl list sinks:1\", \"1ch:pactl list sinks:0\", \"2ch:pactl list sinks:2\", \"2ch:pactl list sinks:0\", \"3ch:pactl list sinks:3\", \"3ch:pactl list sinks:0\", \"4ch:pactl list sinks:4\", \"4ch:pactl list sinks:0\", \"pulseaudio:restart\"], command=combobox_callback, variable=channel_var, width=167, border_width=1, state=\"readonly\", justify=\"center\", font=(FONT_TYPE, 13), dropdown_font=(FONT_TYPE, 14))".format(process_pid[0])
            exec(code)
        elif io_var == 2:
            code = "self.combobox{} = customtkinter.CTkComboBox(self, values=[\"1ch:pactl list sinks:1\", \"1ch:pactl list sinks:0\", \"2ch:pactl list sinks:2\", \"2ch:pactl list sinks:0\", \"3ch:pactl list sinks:3\", \"3ch:pactl list sinks:0\", \"4ch:pactl list sinks:4\", \"4ch:pactl list sinks:0\",  \"5ch:pactl list sinks:5\", \"5ch:pactl list sinks:0\", \"6ch:pactl list sinks:6\", \"6ch:pactl list sinks:0\", \"pulseaudio:restart\"], command=combobox_callback, variable=channel_var, width=167, border_width=1, state=\"readonly\", justify=\"center\", font=(FONT_TYPE, 13), dropdown_font=(FONT_TYPE, 14))".format(process_pid[0])
            exec(code)
        else:
            self.combobox = customtkinter.CTkComboBox(self, values=["ladspa_out:sink 0"], command=combobox_callback, variable=channel_var, width=167, border_width=1, font=(FONT_TYPE, 14), dropdown_font=(FONT_TYPE, 14))

        code = "self.combobox{}.grid(row=0, column=0, padx=21, pady=10, sticky=\"se\")".format(process_pid[0])
        exec(code)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.entry = customtkinter.CTkEntry(self.frame, width=742,  placeholder_text="Entry", border_width=1,  font=(FONT_TYPE, 14))
        self.entry.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.entry_button = customtkinter.CTkButton(self.frame, width=150, text="Edit", fg_color="#3B8ED0", font=(FONT_TYPE, 14),  command=self.entry_add_port)
        self.save_button = customtkinter.CTkButton(self.frame, text="Save", fg_color="#27577D", command=self.save_callback, font=(FONT_TYPE, 14))
        self.set_button = customtkinter.CTkButton(self.frame, width=150, text="Set Effect", fg_color="#27577D", font=(FONT_TYPE, 14), command=self.set_button_callback)

        self.resizable(False, False)

        self.set_button.grid(row=1, column=2, padx=5, pady=(5, 5), sticky="e")
        self.entry_button.grid(row=0, column=2, padx=5, pady=(5, 5), sticky="e")
        self.save_button.grid(row=1, column=0, padx=0, pady=(5, 5), sticky="w")

        global source
        source = 0
        global port_on
        port_on = 0
        self.put_slider()
        global sink
        if sink == 19:
            sink = 0

        global ladspa_list
        if "ladspa_list" in globals():
            win_no = int(self.textbox.get("1.6", "1.8"))
            for win_no in range(1, win_no):
                ladspa_list.append([0, 0, 0, 0, 0, 0])
        else:
            ladspa_list = [[0, 0, 0, 0, 0, 0]]
        global sink_0_list
        if "sink_0_list" in globals():
            sink_0_list.append([0, 0, 0, 0, 0, 0])
        else:
            sink_0_list = [[0, 0, 0, 0, 0, 0]]

        global num_strip
        with open("tmp/port_name{}.txt".format(page), "r") as text:
            lines = text.readlines()
            num_strip = [line.strip() for line in lines]
            num_strip = [s.replace("[", "").replace("]", "") for s in num_strip]
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.INSERT, "plugin=")
            self.entry.insert(tk.END, plugin_file.replace(".so", "") + " label=" + num_strip[1] + " control=")

            win_no = int(self.textbox.get("1.6", "1.8"))
            global win_no_num_strip
            win_no_num_strip[int(win_no)-1] = num_strip[1]
            global command_txt
            command_txt = self.entry.get()

        self.entry_add_port()

        win_no = int(self.textbox.get("1.6", "1.8"))
        global place_list
        if "place_list" in globals():
            place_list.append(place_list[int(win_no)-2])
        else:
            if io_var == 1 or io_var == 2:
                place_list = [[0, 0, 0, 0, 0, 0]]

    def save_callback(self):
    
        def save_button_callback():
            save_data = save_textbox.get("1.0", tk.END)
            save_name = save_entry.get()
            with open("{}".format(save_name), "w") as file:
                file.write("#!/bin/sh\n")
                file.write(save_data)
            os.system("chmod +x \"{}\"".format(save_name))
            os.system("sleep 1")
            save_win.destroy()

        def cancel_button_callback():
            save_win.destroy()

        global save_win
        if save_win == None or not save_win.winfo_exists():
            global command_all
            if command_all != None:
                save_win = customtkinter.CTkToplevel()
                save_win.title("Save the data")
                save_frame = customtkinter.CTkFrame(save_win, fg_color="gray14")
                save_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 7))
                save_button_info = customtkinter.CTkButton(save_win, command=save_button_callback, text="Save the data", font=(FONT_TYPE, 16))
                save_button_info.grid(row=5, column=0, padx=15, pady=(7, 15), sticky="e")
                save_button_cancel = customtkinter.CTkButton(save_win, command=cancel_button_callback, text="Cancel", fg_color="transparent", text_color="white", border_width=1, font=(FONT_TYPE, 16))
                save_button_cancel.grid(row=5, column=0, padx=15, pady=(7, 15), sticky="w")
                save_textbox = customtkinter.CTkTextbox(save_frame, width=500, height=140, font=(FONT_TYPE, 16))
                save_textbox.grid(row=0, column=0, columnspan=2, padx=7, pady=(10, 5), sticky="ew")
                save_label_entry = customtkinter.CTkLabel(save_frame, text="File_name", width=80,  height=5, font=(FONT_TYPE, 16))
                save_label_entry.grid(row=1, column=0, padx=7, pady=0, sticky="w") 
                save_entry = customtkinter.CTkEntry(save_frame, width=400, placeholder_text="", fg_color="white", border_width=2, corner_radius=5, text_color="gray14", font=(FONT_TYPE, 14))
                save_entry.grid(row=2, column=0, padx=7, pady=5, sticky="w")
                save_entry.insert(0, channel_var + "-{}".format(str(date)) + ".sh")
                global sink
                global sink_name
                global source
                if sink == 2 or sink == 4 or sink == 6 or sink == 8:
                    save_textbox.insert("0.0", "pacmd load-module module-loopback source={} sink=0".format(source))
                elif sink == 1 or sink == 3 or sink == 5 or sink == 7:
                    save_textbox.insert("0.0", "pacmd " + command_all + "\n" + "\n" + "pacmd load-module module-loopback source={} sink=ladspa_out.{}".format(source, sink_name))

                save_win.attributes("-topmost", True)

    def combo_button_callback(self):
        pass

    def entry_add_port(self):
        command_txt = self.entry.get()
        sep = " "
        control_del = command_txt.split(sep)
        command_txt = control_del[0:2]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, command_txt)
        self.entry.insert(tk.END, " control=")
        win_no = int(self.textbox.get("1.6", "1.8"))

        global add_port
        port_val = []
        count_port = self.textbox.get("1.0", "1.11")
        count_port = int(count_port[-2:])

        for port in range(0, count_port):
 #           code = "print(\"variable_var\", self.slider_label{}[\"text\"])".format(port)
 #           exec(code)
            port_val = port_val + [eval("self.slider_label{}[\"text\"]".format(port))]

            self.entry.insert(tk.END, str(round(float(port_val[port]), 3)) + ",")

        g.command_diff = self.entry.get()
        self.entry.delete(0, tk.END)
        g.command_diff = g.command_diff.rstrip(",")
        plugins_patch.plugin_patch(num_strip[1])
        self.entry.insert(0, g.command_diff)

    def set_button_callback(self):
        win_no = int(self.textbox.get("1.6", "1.8"))
        global channel_var
        channel_var = eval("self.combobox{}.get()".format(win_no))

        global source
        global sink
        for i in range(0, 15):
            if channel_var == "pactl list sinks:{}".format(i):
                sink = i
            elif channel_var == "{}ch:pactl list sinks:{}".format(i, i):
                source = i
                sink = 2*i-1
            elif channel_var == "{}ch:pactl list sinks:0".format(i):
                source = i
                sink = 2*i
            elif channel_var == "pulseaudio:restart":
                sink = 19
            elif channel_var == "sinks: None":
                sink = 18
        
        os.system("pavucontrol &")
        os.system("sleep {}".format(pulse_sleep))

        def ladspa_out_count():
            os.system("pactl list short sinks > tmp/ladspa_count")
            with open("tmp/ladspa_count", "r") as text:
                ladspa_base = text.readlines()
                ladspa_base = "".join(ladspa_base)
                global out_count
                out_count = len(re.findall("ladspa_out", ladspa_base))

        def ladspa_load_id(sink_name):
            os.system("pactl list short modules > tmp/ladspa_load")
            with open("tmp/ladspa_load", "r") as text:
                lines = text.read().splitlines()
            global ladspa_list
            for line in lines:
                if "sink_name=ladspa_out.{}".format(sink_name) in line:
                    line = line.split("\t")
                    ladspa_list[int(win_no)-1][int(sink_name)-1] = int(line[0])
            global sink_0_list
            for line in lines:
                if "source={} sink=0".format(sink_name) in line:
                    line = line.split("\t")
                    sink_0_list[int(win_no)-1][int(sink_name)-1] = int(line[0])

        def ladspa_loopback(sink_name):
            global command_all
            command_all = self.entry.get()
            command_all = "load-module module-ladspa-sink sink_name=ladspa_out.{} master={} ".format(sink_name, alsa_output) + command_all
            os.system("pacmd {}".format(command_all))
            win_no = int(self.textbox.get("1.6", "1.8"))
            global num_strip
            global plugin
            if plugin[int(win_no)-1] == []:
                plugin[int(win_no)-1] = win_no_num_strip[int(win_no)-1]
            os.system("pacmd update-sink-proplist ladspa_out.{} device.description={}ch:LADSPA_{}".format(sink_name, sink_name, plugin[int(win_no)-1]))
            os.system("pacmd load-module module-loopback source={} sink=ladspa_out.{}".format(source, sink_name))
            os.system("sleep {}".format(pulse_sleep))

        ladspa_out_count()

        global out_count
        global place_list
        global ladspa_list
        global sink_0_list
        global sink_name
        if sink == 18:
            pass
        elif io_var == 0 and sink == 0:
            source = 1
            if out_count == 1:
                os.system("pacmd unload-module module-loopback")
                os.system("pacmd unload-module module-ladspa-sink")
            os.system("pacmd load-module module-loopback source=1 sink=0")
        elif io_var == 0 and sink == 1:
            source = 1
            if out_count == 1:
                os.system("pacmd unload-module module-loopback")
                os.system("pacmd unload-module module-ladspa-sink")
            sink_name = sink
            ladspa_loopback(sink_name)
#        elif io_var == 1 or io_var == 2 and sink == 19:
        elif io_var == 1 and sink == 19:
            if place_list != [[0, 0, 0, 0, 0, 0]]:
                os.system("pacmd unload-module module-loopback")
                os.system("pacmd unload-module module-ladspa-sink")
            os.system("pulseaudio -k")
            os.system("sleep 2")
            os.system("pulseaudio --start")
            source = 0
            sink = 0

        elif io_var == 1 or io_var == 2:
            if sink == 2 or sink == 4 or sink == 6 or sink == 8 or sink == 10 or sink ==12:
                sink_name = int(sink/2)
                if place_list[int(win_no)-1][source-1] == 1:
                    ladspa_load_id(sink_name)
                    os.system("pacmd unload-module {}".format(sink_0_list[int(win_no)-1][int(sink_name)-1]))
                    os.system("pacmd load-module module-loopback source={} sink=0".format(source))
                elif place_list[int(win_no)-1][source-1] == 2:
                    ladspa_load_id(sink_name)
                    os.system("pacmd unload-module {}".format(ladspa_list[int(win_no)-1][int(sink_name)-1]))
                    os.system("pacmd unload-module {}".format(ladspa_list[int(win_no)-1][int(sink_name)-1]+1))
                    os.system("pacmd load-module module-loopback source={} sink=0".format(source))
                    place_list[int(win_no)-1][source-1] = 1
                elif place_list[int(win_no)-1][source-1] == 0:
                    os.system("pacmd load-module module-loopback source={} sink=0".format(source))
                    ladspa_load_id(sink_name)
                    place_list[int(win_no)-1][source-1] = 1

            elif sink == 1 or sink == 3 or sink == 5 or sink == 7 or sink == 9 or sink == 11:
                sink_name = int((sink+1)/2)
                if place_list[int(win_no)-1][source-1] == 1:
                    ladspa_load_id(sink_name)
                    os.system("pacmd unload-module {}".format(sink_0_list[int(win_no)-1][int(sink_name)-1]))
                    ladspa_loopback(sink_name)
                    place_list[int(win_no)-1][source-1] = 2
                elif place_list[int(win_no)-1][source-1] == 2:
                    ladspa_load_id(sink_name)
                    os.system("pacmd unload-module {}".format(ladspa_list[int(win_no)-1][int(sink_name)-1]))
                    os.system("pacmd unload-module {}".format(ladspa_list[int(win_no)-1][int(sink_name)-1]+1))
                    ladspa_loopback(sink_name)
                    ladspa_load_id(sink_name)
                    place_list[int(win_no)-1][source-1] = 2
                elif place_list[int(win_no)-1][source-1] == 0:
                    ladspa_loopback(sink_name)
                    place_list[int(win_no)-1][source-1] = 2
                    
            elif io_var == 1 and sink == 19:
                os.system("pacmd unload-module module-loopback")
                os.system("pacmd unload-module module-ladspa-sink")
                os.system("pulseaudio -k")
                os.system("sleep 2")
                os.system("pulseaudio --start")
                source = 0
                sink = 0
                win_no = int(self.textbox.get("1.6", "1.8"))
                sink_0_list[int(win_no)-1] = [0, 0, 0, 0, 0, 0]
                ladspa_list[int(win_no)-1] = [0, 0, 0, 0, 0, 0]

    def slider_event(self):
        pass
    def put_slider(self):
        os.system("rm tmp/temp_s*")
        with open("tmp/port.txt", "r") as text:
            plugin_port_txt = text.readlines()
            plugin_port_txt = "".join(plugin_port_txt)
            os.system("csplit -z -f tmp/temp_s. tmp/port.txt '/\" input/' {*}")

        with open("tmp/port_count.txt", "r") as text:
            lines = text.readlines()
            num_strip = [line.strip() for line in lines]
            global add_port
            add_port = int(num_strip[page-1])
            process_pid[1] = add_port
            global win_pid
            win_pid = process_pid[0]
            win_port = process_pid[1]
            pid = "Pid: " + "\"" + str(process_pid[0]).zfill(2) + "-" + str(process_pid[1]).zfill(2) + "\""
            self.textbox.insert("0.0", pid)
            self.textbox.configure(state="disabled")

        for port in range(0, int(lines[page-1])):
            global add_count
            add_count += 1
            global port_on
            port_on += 1
            with open("tmp/temp_s." + str(add_count-1).zfill(2), "r") as text:
                plugin_port_txt = text.readlines()
                control = plugin_port_txt[1].split(",")
                control = [s.replace("\n", "").replace("[", "").replace("]", "") for s in control]
                control = [s.replace("srate", srate) for s in control]
                default = plugin_port_txt[2].split(",")
                default = [s.replace("\n", "").replace("[", "").replace("]", "") for s in default]

                global default_var
                if "*" in control[0] and control[1] and default[0]:
                    control_from = eval(control[0])
                    control_to = eval(control[1])
                    default_var = eval(default[0])
                elif "*" in control[1] and control[0] and default[0]:
                    control_from = float(control[0])
                    control_to = eval(control[1])
                    default_var = eval(default[0])
                elif "*" in control[1] and not control[0] and not default[0]:
                    control_from = float(control[0])
                    control_to = eval(control[1])
                    default_var = float(default[0])
                else:
                    control_from = float(control[0])
                    control_to = float(control[1])
                    default_var = float(default[0])

                def slider_event(value):
                    global var
                    var = value
                plugin_port_txt = [s.replace("[", "").replace("]", "").replace("\n", "") for s in plugin_port_txt]
                self.label = customtkinter.CTkLabel(self.frame, text=plugin_port_txt[0], width=180,  height=5, font=(FONT_TYPE, 16))

                global double_checkbox
                if "float" in double_checkbox:
                    self.frame.var = tk.DoubleVar(value=default_var)
                else:
                    self.frame.var = tk.IntVar(value=int(default_var))
                self.slider = customtkinter.CTkSlider(self.frame, width=400, from_=control_from, to=control_to, number_of_steps=100, border_width=7, variable=self.frame.var, command=slider_event)
                code = "self.slider_label{} = ttk.Label(self.frame, width=7, textvariable=self.frame.var, foreground=\"gray17\", background=\"gray70\")".format(str(port_on-1))
                exec(code)
                self.label.grid(row=2+port*add_port, column=0, columnspan=3, pady=0, sticky="w")
                code = "self.slider_label{}.grid(row=3+port*add_port, column=0, padx=10, sticky=\"e\")".format(str(port_on-1))
                exec(code)
                self.slider.grid(row=3+port*add_port, column=1, columnspan=2,  pady=(0, 0), sticky="ew")

                if port_on == add_port:
                    port_on = 0

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.fonts = (FONT_TYPE, 15)

        plugin_list = sorted(os.listdir(path))

        with open("plugin_blocklist", "r") as text:
            plugin_block = text.readlines()
            plugin_block = [s.replace("\n", "") for s in plugin_block]
            for block in plugin_list:
                for exclude in plugin_block:
                    if block == exclude:
                        plugin_list.remove(exclude)
            plugin_list = [item for item in plugin_list if item != "sc3_1427.so"]

        list_var = tk.StringVar(value=plugin_list)

        global process_pid
        process_pid = [0] * 5

        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.geometry("440x320")
        self.title("LADSPA Tester")

        self.main_frame = customtkinter.CTkFrame(self)
        self.grid_columnconfigure(0, weight=1)
        self.plugin_label = customtkinter.CTkLabel(self, text="Plugins", font=(FONT_TYPE, 18))
        self.listbox = CTkListbox(self, fg_color="gray20", border_color="gray37", font=(FONT_TYPE, 18), listvariable=list_var, border_width=1)
        self.button_config = customtkinter.CTkButton(self, fg_color="transparent", text_color="white", border_width=1, command=self.button_config_callback, text="Config", font=(FONT_TYPE, 16))

        global double_checkbox
        double_checkbox = []
        double_checkbox.append("float")

        int_float = tk.BooleanVar()
        int_float.set(True)
        self.check_int = customtkinter.CTkSwitch(self, text="float", font=(FONT_TYPE, 16), variable=int_float, command=self.checkbox_event)
        self.button_open = customtkinter.CTkButton(self, command=self.button_select_callback, text="Open", font=(FONT_TYPE, 16))
        self.plugin_label.grid(row=0, column=0, padx=20, pady=(5, 5), sticky="sw")
        self.main_frame.grid(row=1, column=0, padx=20, pady=0, sticky="ew")
        self.listbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.button_open.grid(row=2, column=0, padx=10, pady=(7, 15), sticky="e")
        self.button_config.grid(row=2, column=0, padx=10, pady=(7, 15), sticky="w")
        self.check_int.grid(row=0, column=0, padx=(0, 0), pady=(0, 7), sticky="se")

        self.resizable(False, False)

        global sub_win
        sub_win = None

        global save_win
        save_win = None

        global command_all
        command_all = None

        global io_var
        io_var = 2

        global select_io_var
        select_io_var = tk.IntVar(value=2)

        global sink
        sink = 0

        global plugin
        plugin = [[]] * 45
        global win_no_num_strip
        win_no_num_strip = [[]] * 45

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        is_file = os.path.isfile("../.config/pulse/default.pa-{}-bak".format(date))
        if is_file:
            os.system("rm ../.config/pulse/default.pa")
            os.system("mv ../.config/pulse/default.pa-{}-bak ../.config/default.pa".format(date))
        else:
            os.system("rm ../.config/pulse/default.pa")
        self.destroy()
        os.system("pulseaudio -k &")
        os.system("sleep 2")
        os.system("pulseaudio --start &")

#        self.toplevel_window = None

    def checkbox_event(self):
        global double_checkbox
        double_checkbox = []
        if self.check_int.get() == 1:
            double_checkbox.append(self.check_int.cget("text"))

    def button_config_callback(self):
        def button_select_config():
            global to_range
            to_range = to_range_entry.get()
            global srate
            srate = srate_entry.get()

            sub_win.destroy()


        global sub_win
        if sub_win == None or not sub_win.winfo_exists():
            sub_win = customtkinter.CTkToplevel()
            sub_win.title("Config")
            sub_frame = customtkinter.CTkFrame(sub_win, fg_color="gray14")
            sub_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 7))
            button_config_info = customtkinter.CTkButton(sub_win, command=button_select_config, text="OK", font=(FONT_TYPE, 16))

            def check_io_event():
                global io_var
                global select_io_var
                io_var = select_io_var.get()

            check_io_0 = customtkinter.CTkRadioButton(sub_frame, text="Single pickup:\"pactl list sources\" 0 to 1", border_width_unchecked=2, font=(FONT_TYPE, 16), command=check_io_event, variable=select_io_var, value=0)
            check_io_0.grid(row=2, column=0, columnspan=3, padx=15, pady=5, sticky="w")
            check_io_1 = customtkinter.CTkRadioButton(sub_frame, text="4 strings pickup:\"pactl list sources\" 0 to 4",  border_width_unchecked=2, font=(FONT_TYPE, 16), command=check_io_event, variable=select_io_var, value=1)
            check_io_1.grid(row=1, column=0, padx=15, pady=5, sticky="w")
            check_io_2 = customtkinter.CTkRadioButton(sub_frame, text="6 strings pickup:\"pactl list sources\" 0 to 6", border_width_unchecked=2, font=(FONT_TYPE, 16), command=check_io_event, variable=select_io_var, value=2)
            check_io_2.grid(row=0, column=0, padx=15, pady=5, sticky="w")
            check_io_3 = customtkinter.CTkRadioButton(sub_frame, text="Multi pickup", border_width_unchecked=2, font=(FONT_TYPE, 16), command=check_io_event, variable=select_io_var, value=3)
            check_io_3.grid(row=3, column=0, padx=15, pady=(5, 0), sticky="w")
            button_config_info.grid(row=8, column=0, padx=10, pady=(7, 15), sticky="e")

            frame_in = customtkinter.CTkFrame(sub_frame, fg_color="gray10")
            frame_in.grid(row=4, column=0, padx=(10, 10), pady=(10, 7), sticky="ew")
            
            to_range_entry = customtkinter.CTkEntry(frame_in, width=70, placeholder_text="1", fg_color="white", border_width=2, corner_radius=1, text_color="gray14", font=(FONT_TYPE, 14))
            srate_entry = customtkinter.CTkEntry(frame_in, width=70, placeholder_text="44100", fg_color="white", border_width=2, corner_radius=1, text_color="gray14", font=(FONT_TYPE, 14))
            to_range_entry.grid(row=6, column=0, padx=15, pady=0, sticky="w")
            srate_entry.grid(row=8, column=0, padx=15, pady=(0, 15), sticky="w")
            to_range_text = customtkinter.CTkTextbox(frame_in, width=300, height=3, padx=0, pady=0, fg_color="gray10", font=(FONT_TYPE, 16))
            to_range_text.grid(row=5, column=0, padx=5, pady=5, sticky="w")
            srate_text = customtkinter.CTkTextbox(frame_in, width=300, height=3, padx=0, pady=0, fg_color="gray10", font=(FONT_TYPE, 16))
            srate_text.grid(row=7, column=0, padx=5, pady=5, sticky="w")
            to_range_text.insert("0.0", "to_range(slider)value")
            srate_text.insert("0.0", "sample_rate(srate)value")
            to_range_entry.insert(0, 100)
            srate_entry.insert(0, 44100)

            sub_win.attributes("-topmost", True)

    def button_select_callback(self):
        global plugin_file
        plugin_file = self.listbox.get()

        if plugin_file == None:
            pass
        else:
            global add_count
            add_count = 0

#    if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
#        self.toplevel_window = Toplevelwindow(self)

            global path
            os.system("analyseplugin {}/{} | tee tmp/tmp.txt".format(path, plugin_file))
            os.system("rm tmp/tmp_s.*")
            os.system("csplit -z -f tmp/tmp_s. tmp/tmp.txt '/Plugin Name:.*/' {*}")
            os.system("ls -1u tmp/tmp_s* | wc -l > tmp/tmp_s.00")
            os.system("rm tmp/port*.txt")

            with open("tmp/tmp_s.00", "r") as text:
                lines = text.readlines()
                num_strip = [line.strip() for line in lines]
            global add_page
            add_page = int(num_strip[0]) - 1

            global page
            for page in range(1, add_page + 1):
                with open("tmp/tmp_s." + str(page).zfill(2), "r") as text:

                    os.system("touch tmp/port.txt")

                    pram_base = text.readlines()
                    global plugin_info
                    plugin_info = "".join(pram_base)

                    global count
                    count = len(re.findall('\" input, control,', plugin_info))
                    os.system("echo {} >> tmp/port_count.txt".format(count))

                    global to_range
                    for line in pram_base:
                        if "Plugin Name" in line:
                            global plugin_name
                            plugin_name = line
                            plugin_name = line.split(",")
                            plugin_name = [s.replace("\t", "") for s in plugin_name]
                            plugin_name = [s.replace("\n", "") for s in plugin_name]
                            plugin_name = [s.replace("\"", "") for s in plugin_name]
                            plugin_name = [s.replace("Plugin Name: ", "") for s in plugin_name]
                            os.system("echo {} >> tmp/port_name{}.txt".format(plugin_name, page))

                        if "Plugin Label" in line:
                            global plugin_label
                            plugin_label = line
                            plugin_label = line.split(",")
                            plugin_label = [s.replace("\n", "") for s in plugin_label]
                            plugin_label = [s.replace("\"", "") for s in plugin_label]
                            plugin_label = [s.replace("Plugin Label: ", "") for s in plugin_label]
                            os.system("echo {} >> tmp/port_name{}.txt".format(plugin_label, page))

                        if "ID:" in line:
                            global plugin_ID
                            plugin_ID = line
                            plugin_ID = line.split(",")
                            plugin_ID = [s.replace("\n", "") for s in plugin_ID]
                            plugin_ID = [s.replace("\"", "") for s in plugin_ID]
                            plugin_ID = [s.replace("Plugin Unique ID:", "") for s in plugin_ID]
                            os.system("echo {} >> tmp/port_name{}.txt".format(plugin_ID, page))

                        if "\" input, control," in line:
                            port = line
                            plugin_port = port.split(",")
                            plugin_port = [s.replace("\t", "") for s in plugin_port]
                            plugin_port = [s.replace("\n", "") for s in plugin_port]
                            plugin_port = [s.replace("Ports:", "") for s in plugin_port]
                            plugin_port = [s.replace("  ", " ") for s in plugin_port]
                            os.system("echo {} >> tmp/port.txt".format(plugin_port))
                            control_to = [s for s in plugin_port if " to " in s]
                            control_to += [s for s in plugin_port if "toggled" in s]
                            control_to = [s.replace("toggled", toggled) for s in control_to]
                            control_to = [s.replace(" to ", ", ") for s in control_to]
                            control_to = [s.replace("...", to_range) for s in control_to]
                            control_to = [s.replace("srate", srate) for s in control_to]
                            control_default = [s for s in plugin_port if "default" in s]
                            os.system("echo {} >> tmp/port.txt".format(control_to))
                            control_default = [s.replace("default", "") for s in control_default]
                            control_default = [s.replace("srate", srate) for s in control_default]

                            if control_default == []:
                                control_default = ['0']

                            os.system("echo {} >> tmp/port.txt".format(control_default))

                global process_pid
                process_pid[0] += 1

                global sub_win
                if sub_win == None or not sub_win.winfo_exists():
                    self.toplevel_window = Toplevelwindow(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()

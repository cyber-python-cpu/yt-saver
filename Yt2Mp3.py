from pytube import YouTube
import re
import customtkinter as tk

gui = tk.CTk()
gui.title("Yt to mp3, By Syskill")
gui.geometry("600x500")
illegal_chars_regex = r'[<>:/\\|?*]'
log = tk.CTkTextbox(gui, width=600, height=300)
log.grid(row=0,column=0)
last_command = ""
audio_only=True
command_input = tk.CTkTextbox(gui, width=500, height=25)
command_description = tk.CTkLabel(gui,text="Commands here v ################################## Log here ^")
command_description.grid(row=1,column=0,sticky="ns")
command_input.grid(row=2,column=0)

def logen():
    #enables the log
    log.configure(True,state="normal")
def logdi():
    #disables the log
    log.configure(True,state="disabled")

def command_parse(event=None):  #event=None to handle key bindings
    global last_command, audio_only
    last_command = command_input.get(1.0, "end-1c")#1,
    command_input.delete("1.0", "end") #2, Get and clear
    logen() #Get log ready for writing
    log.insert("end", f"> {last_command}\n")
    print(f"DEBUG: {last_command}") #Debug info, will be removed in release
    if last_command.startswith("http") or last_command.startswith("you"):
        log.insert("end", "Link Detected.\n")
        download(last_command)
    elif last_command.lower().startswith("v"):
        log.insert("end","Video mode enabled.\n")
        audio_only=False
    elif last_command.lower().startswith("a"):
        log.insert("end", "Audio mode enabled.\n")
        audio_only=True
    elif last_command.lower().startswith("help"):
        help_command()
    gui.after(10,lambda: command_input.delete("1.0","end")) #Bugfix, dont pr this to be removed
    logdi()

def help_command():
    helptext = """\
    Any link starting in http or you: Downloads the video in the current mode.
    v, video: Changes the video download mode into video mode. Downloads an mp4 file.
    a, audio: Changes the video download mode into audio mode. Downloads an mp3 file.
    help: Shows this message.\n"""
    log.insert("end",helptext)

def download(url_arg):
    try:
        video = YouTube(url_arg)
        filename = re.sub(illegal_chars_regex, '_', video.title)
        if audio_only:
            stream = video.streams.filter(only_audio=True).order_by("abr").desc().first()
        else:
            stream = video.streams.filter(progressive=True).order_by("resolution").desc().first() 
        stream.download(filename=f"{filename}.{'mp3' if audio_only else 'mp4'}")
        log.insert("end",f"Downloaded {filename}.{'mp3' if audio_only else 'mp4'}\n")
    except KeyError:
        log.insert("end", "Unable to fetch video information. Please check the video URL.\n")

def close_window():
    #Cleanup here
    gui.destroy()

#Some last minute touches
command_input.bind("<Return>", command_parse)
gui.protocol("WM_DELETE_WINDOW",close_window)
log.insert("end","""Welcome to my youtube downloader tool!
To get started, try just pasting a youtube link into the command box!
It should download a mp3 into your current directory.
If this program is in the downloads folder try moving it into another folder for orginization.
Type help into the command box to list all commands.\n""")
logdi()
gui.mainloop()
    

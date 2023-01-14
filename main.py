import re
import threading
from time import sleep
from tkinter import *  
from functools import partial
from tkinter.scrolledtext import ScrolledText

from ping_scan import *
from host_scan import *
from os_detect import *
from port_scan import *

# Create the main window
window = Tk()

# Set the window title
window.title("NetMapper 0.0.3")

# Set the window size and make it un-resizable
window.geometry("750x450")
window.resizable(False, False)
# window.config(bg="cyan")

back_state = 0
ip_arr = []

def back_func():
    match back_state:
        case 0:
            # main
            main_frame()
        case 1:
            host_dis_frame()
        case 2:
            host_scan_frame()
        case _:
            print("Something went wrong!")

def all_scan_frame(ip):
    default_txt = 'Scanning <' + ip + '>\nPlease wait ... '

    def set_back_to_main():
        global back_state
        back_state = 0

    def remove_all_scan_frame():
        #remove the text widgets
        target_ip.grid_remove()
        scan_result.grid_remove()
        #remove the buttons
        host_scan_btn.grid_remove()
        port_scan_btn.grid_remove()
        version_detect_btn.grid_remove()
        os_detect_btn.grid_remove()
        back_btn.grid_remove()

    target_ip = Text(window, padx=10, pady=7, font=("Aileron", 14),
        height=1, width=32, borderwidth=2, relief="solid")
    target_ip.insert(END, 'TARGET IP : ' + ip)
    target_ip.config(state="disabled")
    target_ip.grid(row=0, column=0,pady=(21,0), padx=(14,0),columnspan=1, sticky = "ne")

    scan_result = ScrolledText(window, padx=10, pady=7, font=("Aileron", 14),
        height=15, width=32, borderwidth=2, relief="solid", wrap=WORD)
    scan_result.insert(END, default_txt)
    scan_result.config(state="disabled")
    scan_result.grid(row=0, column=0,pady=(60,30), padx=(30,0), columnspan=2, sticky = "ne")

    def update_scan_result(func, arg):
        scan_result.config(state="normal")
        scan_result.delete('1.0', END) # delete all text
        scan_result.insert(END, default_txt)
        scan_result.config(state="disabled")
        txt = func(arg)
        scan_result.config(state="normal")
        scan_result.delete('1.0', END) # delete all text
        scan_result.insert(INSERT, txt) # insert new text
        scan_result.config(state="disabled")
        enable_all_btn()

    def scan_init(func, arg):
        stat, txt = func(arg)
        scan_result.config(state="normal")
        scan_result.delete('1.0', END) # delete all text
        scan_result.tag_config("host_alive", foreground="green")
        scan_result.tag_config("host_dead", foreground="red")
        scan_result.insert(INSERT, txt, "host_dead" if not stat else "host_alive") # insert new text

        if stat:
            enable_all_btn()
            scan_result.insert(INSERT, "\nPlease proceed with other scan >> ")
            
        else:
            scan_result.insert(INSERT, "\nPlease input available IP address to scan")

        scan_result.config(state="disabled")


    def disable_all_btn():
        host_scan_btn['state'] = 'disabled'
        port_scan_btn['state'] = 'disabled'
        version_detect_btn['state'] = 'disabled'
        os_detect_btn['state'] = 'disabled'

    def enable_all_btn():
        host_scan_btn['state'] = 'normal'
        port_scan_btn['state'] = 'normal'
        version_detect_btn['state'] = 'normal'
        os_detect_btn['state'] = 'normal'

    # Buttons
    host_scan_btn = Button(window, text="Host Scan", command=lambda: update_scan(host_scan, ip))
    host_scan_btn.grid(row=0, column=3,pady=(20, 0), padx=(20,0), sticky = "nw")
    host_scan_btn.config(font=("Montserrat", 12, "bold"), width=25, height=2, bg='#b1b1b1')
    host_scan_btn.bind("<Enter>", lambda event, b=host_scan_btn: b.config(bg='#d8d8d8') if b['state'] == 'normal' else None)
    host_scan_btn.bind("<Leave>", lambda event, b=host_scan_btn: b.config(bg='#b1b1b1') if b['state'] == 'normal' else None)

    port_scan_btn = Button(window, text="Port Scan", command=lambda: update_scan(port_scan, ip))
    port_scan_btn.grid(row=0, column=3,pady=(100, 0), padx=(20,0), sticky = "nw")
    port_scan_btn.config(font=("Montserrat", 12, "bold"), width=25, height=2, bg='#b1b1b1')
    port_scan_btn.bind("<Enter>", lambda event, b=port_scan_btn: b.config(bg='#d8d8d8') if b['state'] == 'normal' else None)
    port_scan_btn.bind("<Leave>", lambda event, b=port_scan_btn: b.config(bg='#b1b1b1') if b['state'] == 'normal' else None)

    version_detect_btn = Button(window, text="Version Detection", command=lambda: update_scan(port_scan_with_version, ip)) #command=lambda: update_scan_result(test, ip)
    version_detect_btn.grid(row=0, column=3,pady=(180, 0), padx=(20,0), sticky = "nw")
    version_detect_btn.config(font=("Montserrat", 12, "bold"), width=25, height=2, bg='#b1b1b1')
    version_detect_btn.bind("<Enter>", lambda event, b=version_detect_btn: b.config(bg='#d8d8d8') if b['state'] == 'normal' else None)
    version_detect_btn.bind("<Leave>", lambda event, b=version_detect_btn: b.config(bg='#b1b1b1') if b['state'] == 'normal' else None)

    os_detect_btn = Button(window, text="OS Detection", command=lambda: update_scan(os_detect, ip))
    os_detect_btn.grid(row=0, column=3,pady=(260, 0), padx=(20,0), sticky = "nw")
    os_detect_btn.config(font=("Montserrat", 12, "bold"), width=25, height=2, bg='#b1b1b1')
    os_detect_btn.bind("<Enter>", lambda event, b=os_detect_btn: b.config(bg='#d8d8d8') if b['state'] == 'normal' else None)
    os_detect_btn.bind("<Leave>", lambda event, b=os_detect_btn: b.config(bg='#b1b1b1') if b['state'] == 'normal' else None)

    back_btn = Button(window, text="Back", command=lambda: [remove_all_scan_frame(), back_func() if back_state == 1 else back_func(), set_back_to_main()])
    back_btn.grid(row=0, column=3,pady=(360,20), padx=(20,0), sticky = "nw")
    back_btn.config(font=("Montserrat", 12, "bold"), width=25, height=2, fg='white', bg='#ff4c4c')
    back_btn.bind("<Enter>", lambda event, b=back_btn: b.config(bg='#ff7f7f'))
    back_btn.bind("<Leave>", lambda event, b=back_btn: b.config(bg='#ff4c4c'))

    def update_scan_init( ):
        disable_all_btn()
        scan_init(ip_scan,ip)

    def update_scan(func, arg):
        disable_all_btn()
        ta = threading.Thread(target=update_scan_result, args=(func, arg))
        ta.start()

    t = threading.Thread(target=update_scan_init)
    t.start()

def host_dis_load_frame(ip):
    def get_data():
        def remove_host_dis_load_frame():
            title_host_dis.destroy()
            title_host_dis_wait.destroy()

        title_host_dis = Label(window, text="SCANNING FOR IP IN SUBNET " + '.'.join(ip.split('.')[:3]) + '.XXX', fg="green", font=("Montserrat", 20, "bold"))
        title_host_dis.place(relx=.5, rely=.4, anchor="center")
        title_host_dis_wait = Label(window, text="PLEASE WAIT ...", fg="black", font=("Montserrat", 18, "bold"))
        title_host_dis_wait.place(relx=.5, rely=.5, anchor="center") 
        global ip_arr  
        if (not ip_arr):   
            ip_arr = host_dis(ip)
        remove_host_dis_load_frame()
        host_dis_frame()            
    t = threading.Thread(target=get_data)
    t.start()

def host_dis_frame():
    def set_back_to_host_scan():
        global back_state
        back_state = 1

    def remove_host_dis_frame():
        #remove the frame
        frame.grid_remove()
        header.place_forget()
        footer.place_forget()
        #remove the canvas
        canvas.grid_remove()
        sb.grid_remove()

    def ip_button_click(ip):
        remove_host_dis_frame()
        all_scan_frame(ip)
        set_back_to_host_scan()


    canvas = Canvas(window)
    sb = Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)

    
    frame = Frame(window)
    frame.grid(padx=85, pady=90, sticky='nsew')
    canvas = Canvas(frame)
    canvas.grid(row=1, column=0,sticky='nsew')
    canvas.config(height=250, width=640)
    sb = Scrollbar(frame, orient="vertical", command=canvas.yview)
    sb.grid(row=1, column=1,sticky='ns')
    canvas.configure(yscrollcommand=sb.set)
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    frame_canvas = Frame(canvas)

    
    for line in ip_arr:
        button_text = "<" + str(line) + ">"
        button = Button(frame_canvas, text=button_text, bg="white", justify="center", command=partial(ip_button_click, line))  
        button.config(font=("Montserrat", 12, "bold"), width=50, height=2, bg='#b1b1b1')
        button.pack(pady=10, anchor="center")
        button.bind("<Enter>", lambda event, b=button: b.config(bg='#d8d8d8'))
        button.bind("<Leave>", lambda event, b=button: b.config(bg='#b1b1b1'))
    else:
        header = Label(window, text="LIST OF ALIVE HOST \n(SCROLL TO VIEW MORE) : ", font=("Aileron Bold", 15))
        header.place(relx=.5, rely=.05, anchor="n")

        footer = Button(window, text="Back", command=lambda: [remove_host_dis_frame(), back_func()])
        footer.config(font=("Montserrat", 12, "bold"), width=35, height=2, fg='white', bg='#ff4c4c')
        footer.bind("<Enter>", lambda event, b=footer: b.config(bg='#ff7f7f'))
        footer.bind("<Leave>", lambda event, b=footer: b.config(bg='#ff4c4c'))
        footer.place(relx=.49, rely=.8, anchor="n")
    
    (canvas.create_window((0,0), window=frame_canvas, anchor='nw'))

    (frame_canvas.update_idletasks())
    (canvas.config(scrollregion=canvas.bbox("all")))

def host_scan_frame():
    def set_back_to_host_scan():
        global back_state
        back_state = 2

    def remove_host_scan_frame():
        # Code to execute when the first button is clicked goes here
        title_input.grid_remove()
        input_field.grid_remove()
        button1.grid_remove()
        back_btn.grid_remove()
        # title_ip.grid_remove()
    
    default_txt = "INPUT IP :"

    # Create a big title label
    title_input = Label(window, text=default_txt, font=("Aileron Bold", 15))
    title_input.grid(pady=(0,40), padx=(50,0))

    def on_submit(event=None):
        # Retrieve the input
        input_text = input_field.get().strip()

        if input_text == "":
            title_input['fg'] = "red"
            title_input['text'] = "EMPTY!"
        else:
            pattern = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            if re.match(pattern, input_text):
                # title_input['fg'] = "green"
                # title_input['text'] = "SCANNING <" + input_text + ">, PLEASE WAIT ..."
                # button1['state'] = "disabled"
                # input_field['state'] = "disabled"
                remove_host_scan_frame()
                all_scan_frame(input_text)
                set_back_to_host_scan()
                

            else:
                title_input['fg'] = "red"
                title_input['text'] = "INVALID IP ADDRESS!"
        
    def press_animation(event):
        if button1['state'] != "disabled":
            button1.config(bg = "white") # change the background color to white
            button1.config(relief = "sunken") # change the relief to sunken
            window.after(100, lambda: button1.config(relief='raised', bg = "#b1b1b1")) # wait for 100 ms
            on_submit()

    def click(key):
        if input_field['state'] != "disabled":
    # print the key that was pressed
            title_input['fg'] = "black"
            title_input['text'] = default_txt

    input_field = Entry(window)
    input_field.config(bd=3, relief="solid", bg='white', fg='black', justify="center", font=("Montserrat", 20, 'bold'), width=35)
    input_field.bind('<Return>', press_animation)
    input_field.bind('<KeyPress>', click)

    # using grid geometry manager to place the widget
    input_field.grid(row=0, column=0, padx=(40,0), pady=(125,45))
    input_field.focus()

    # Create the first button
    button1 = Button(window, text="SUBMIT IP", command=on_submit)
    # Center the button horizontally and stack it above the second button
    button1.grid(padx=(40,0), pady=20)
    button1.config(font=("Montserrat", 12, "bold"), width=60, height=3, bg='#b1b1b1')

    back_btn = Button(window, text="Back", command=lambda: [remove_host_scan_frame(), back_func()])
    back_btn.grid(padx=(40,0), pady=10)
    back_btn.config(font=("Montserrat", 12, "bold"), width=25, height=2, fg='white', bg='#ff4c4c')
    back_btn.bind("<Enter>", lambda event, b=back_btn: b.config(bg='#ff7f7f'))
    back_btn.bind("<Leave>", lambda event, b=back_btn: b.config(bg='#ff4c4c'))

def main_frame():
    ip = get_ip()
    global ip_arr  
    ip_arr = []
    # Create a big title label
    title = Label(window, text="NetMapper™", font=("Montserrat", 30, "bold"))
    title.grid(pady=(35,40), padx=(65,0))

    # Create a IP label
    title_ip = Label(window, padx=10, text="MY IP : " + ip, font=("Aileron Bold", 15),
            height=2, borderwidth=2, relief="solid")
    title_ip.grid(pady=(0,30), padx=(50,0))

    def on_button_enter(e, button):
        button.config(bg='#d8d8d8')

    def on_button_leave(e, button):
        button.config(bg='#b1b1b1')

        
    # Define the function that will be called when the first button is clicked
    def on_button1_click():
        remove_main_frame()
        host_dis_load_frame(ip)
        
    # Define the function that will be called when the second button is clicked
    def on_button2_click():
        # Code to execute when the second button is clicked goes here
        remove_main_frame() 
        host_scan_frame()

    # Create the first button
    button1 = Button(window, text="HOST DISCOVERY", command=on_button1_click)
    # Center the button horizontally and stack it above the second button
    button1.grid(pady=(0,30), padx=(40,0))
    button1.config(font=("Montserrat", 12, "bold"), width=60, height=3, bg='#b1b1b1')

    button1.bind("<Enter>",  lambda e: on_button_enter(e, button1))
    button1.bind("<Leave>",  lambda e: on_button_leave(e, button1))

    # Create the second button
    button2 = Button(window, text="HOST SCAN", command=on_button2_click)
    # Center the button horizontally
    button2.grid(pady=(0,30), padx=(40,0))
    button2.config(font=("Montserrat", 12, "bold"), width=60, height=3, bg='#b1b1b1')

    button2.bind("<Enter>",  lambda e: on_button_enter(e, button2))
    button2.bind("<Leave>",  lambda e: on_button_leave(e, button2))

    def remove_main_frame():
        # Code to execute when the first button is clicked goes here
        button1.grid_remove()
        button2.grid_remove()
        title.grid_remove()
        title_ip.grid_remove()

def error_connect():
    title = Label(window, text="NetMapper™", font=("Montserrat", 30, "bold"))
    title.grid(pady=(60,40), padx=(240,0))
    title_host_dis = Label(window, text="NO NETWORK CONNECTION DETECTED!", fg="red", font=("Montserrat", 23, "bold"))
    title_host_dis.place(relx=.5, rely=.45, anchor="center")
    title_host_dis_wait = Label(window, text="PLEASE CHECK YOUR CONNECTIVITY \nAND RESTART THE APP", fg="black", font=("Montserrat", 15, "bold"))
    title_host_dis_wait.place(relx=.5, rely=.60, anchor="center")    

if check_connection():
    main_frame()
else:
    error_connect()   
      
# all_scan_frame('222.1.3.4')
# all_scan_frame('1.1.1.1')

# host_scan_frame()
# host_dis_frame()
# Run the Tkinter event loop
window.mainloop()
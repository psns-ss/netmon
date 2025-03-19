import xml.etree.ElementTree as ET
import time
import os
import threading
from smb.SMBConnection import SMBConnection
from io import BytesIO
from lxml import etree

def delete_line():
    while True:
        line_number = input("Enter the line number to delete: ")
        try:
            line_number = int(line_number)
            with open("rules/local.rules", "r") as f:
                lines = f.readlines()
            with open("rules/local.rules", "w") as f:
                for i, line in enumerate(lines):
                    if i != line_number - 1:
                        f.write(line)
            print(f"Line number {line_number} deleted.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except IndexError:
            print("Line number is out of range.")

namespace = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}
processed_process_ids = set()
sid = 5

def smb_connect():
    conn = SMBConnection("me", "1", "polym", "DESKTOP-0QN63TJ", use_ntlm_v2=True)
    assert conn.connect("192.168.2.202", 139)
    return conn

def smb_read_file(conn, filename):
    with BytesIO() as file_obj:
        conn.retrieveFile("logs", filename, file_obj)
        return file_obj.getvalue()

def process_xml_file(xml_data):
    global sid
    root = etree.fromstring(xml_data)
    event_elements = root.findall(".//ns:Event", namespace)
    with open('rules/local.rules', 'a') as f:

        for event_element in event_elements:
            event_id_element = event_element.find(".//ns:EventID", namespace)

            if event_id_element is not None:
                event_id = event_id_element.text.strip()

                if event_id == "3":
                    data_elements = event_element.findall(".//ns:EventData/ns:Data", namespace)
                    data_values = {}
                    for data_element in data_elements:
                        name = data_element.get("Name")
                        value = data_element.text.strip() if data_element.text else ""
                        data_values[name] = value
                    protocol = data_values.get("Protocol", "")
                    source_ip = data_values.get("SourceIp", "")
                    source_port = data_values.get("SourcePort", "")
                    dest_ip = data_values.get("DestinationIp", "")
                    dest_port = data_values.get("DestinationPort", "")
                    source_hostname = data_values.get("SourceHostname", "")
                    image = data_values.get("Image", "")
                    process_id = data_values.get("ProcessId", "")

                    if source_ip.startswith(("192", "127", "224", "10")):

                        if process_id not in processed_process_ids:
                            processed_process_ids.add(process_id)
                            output_string = 'alert {protocol} {source_ip} {source_port} -> {dest_ip} {dest_port} (msg:"Application {image} with PID {process_id} has access to network"; sid:{sid};)'.format(
                                protocol=protocol,
                                source_ip=source_ip,
                                source_port=source_port,
                                dest_ip=dest_ip,
                                dest_port=dest_port,
                                image=image,
                                process_id=process_id,
                                sid=sid
                            )
                            sid += 1
                            f.write(output_string + '\n')

if __name__ == "__main__":
    threading.Thread(target=delete_line, daemon=True).start() 
    conn = smb_connect()
    last_modified_time = None
    while True:
        try:
            xml_data = smb_read_file(conn, 'logs.xml')
            file = open("logs/suricata/logs.xml", "w")
            file.write(xml_data.decode("utf-8").replace('\r\n','\n'))
            file.close()
            current_modified_time = os.path.getmtime('logs/suricata/logs.xml')
            if last_modified_time is None or last_modified_time != current_modified_time:
                last_modified_time = current_modified_time
                with open('logs/suricata/logs.xml', 'r') as f:
                    for line in f:
                        if line.strip().startswith("<Events>"):
                            process_xml_file(line)
        except FileNotFoundError:
            pass
        except ET.ParseError:
            pass
        time.sleep(1)

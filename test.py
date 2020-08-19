import telnetlib
import re
from graphviz import Digraph


srv = "he"

if srv == "opentransit": 
    host = "route-server.opentransit.net"
    user = "rviews"
    password = "Rviews"
    lg_asn = "5511"
    cmd = "show bgp {}"
elif srv == "oregonuniv": 
    host = "route-views.routeviews.org"
    user = "rviews"
    password = "none"
    lg_asn = "3582"
    cmd = "show bgp {}"
elif srv == "warian": 
    host = "route-server.warian.net"
    user = "none"
    password = "rviews"
    lg_asn = "56911"
    cmd = "show bgp ipv4 unicast {}"
elif srv == "csaholdigs": #Blacklist des fois
    host = "route-views.sg.routeviews.org"
    user = "none"
    password = "none"
    lg_asn = "45494"
    cmd = "show bgp ipv4 unicast {}"
elif srv == "he": #Blacklist des fois
    host = "route-server.he.net"
    user = "none"
    password = "none"
    lg_asn = "6939"
    cmd = "show bgp ipv4 unicast {}"
elif srv == "iamageeknz": #Blacklist des fois
    host = "rs.as45186.net"
    user = "none"
    password = "none"
    lg_asn = "45186"
    cmd = "show bgp ipv4 unicast {}"    
elif srv == "att": 
    host = "route-server.ip.att.net"
    user = "rviews"
    password = "rviews"
    lg_asn = "7018"
    cmd = "show route {}" 
    

# Récupération de l'IP dont on veux connaitre plus d'informations
ip = input("IP : ")

# Connexion à OpenTransit
tn = telnetlib.Telnet(host)

if user != "none":
    if(srv == "att"):
        tn.read_until("login: ".encode())
        tn.write((user + "\n").encode())
        print("ok")
    else:
        tn.read_until("Username: ".encode())
        tn.write((user + "\n").encode())

if password != "none":
    if(srv == "att"):
        tn.read_until("Password:".encode())
        tn.write((password + "\n").encode())
        print("ok")
    else: 
        tn.read_until("Password: ".encode())
        tn.write((password + "\n").encode())

# Execution d'une commande d'information BGP
tn.write((cmd + "\n").format(ip).encode())
tn.write(chr(25).encode())
tn.write(chr(25).encode())
tn.write(chr(25).encode())
tn.write("q\n".encode())
tn.write("exit\n".encode())


# Decodage des données pour les adaptées à python
data = tn.read_all().decode("utf-8")

print(data)

# Récupération des données grâce à l'utilisation d'expression régulière (module re)
paths = {}

paths["as_list"] = re.findall(r"  ([0-9][0-9 ]+),", data)
if(paths["as_list"] == []):
    paths["as_list"] = re.findall(r"  ([0-9][0-9 ]+)[^0-9.]", data)

if(srv == "att"):
    paths["as_list"] = re.findall(r"(?<=AS path: 7018 )[0-9][0-9 ]+[^ I]", data)

as_list = paths['as_list']

g = Digraph('G', filename='hello', format='png', graph_attr={'rankdir':'LR', 'concentrate': 'true'})

for as_path in as_list: 
    as_path = as_path.split(" ")
    as_path.reverse()
    original_asn = as_path[0]
    border_asn = as_path[-1]
    precedent_asn = original_asn
    for asn in as_path: 
        if asn != original_asn: 
            g.edge("AS" + asn, "AS" + precedent_asn)
            precedent_asn = asn
        if asn == border_asn: 
            g.edge("AS" + lg_asn, "AS" + asn)

g.render()
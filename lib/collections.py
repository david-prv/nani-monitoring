#! /usr/bin/env python3

from decouple import config

"""
COLLECTIONS:

Enumerations of all available components, hostnames and their
corresponding statuspage.io email addresses goes here
"""

# Map for Component names to corresponding
# email addresses
COMPONENTS = {
    "Frontend": config("FRONTEND"),
    "Backend": config("BACKEND"),
    "Minecraft-001": config("MC01"),
    "Minecraft-002": config("MC02"),
    "Teamspeak-001": config("TS01"),
    "Pixle": config("PIXLE"),
    "Database": config("DB"),
    "External SMTP": config("SMTP"),
    "External DNS 1": config("DNS01"),
    "External DNS 2": config("DNS02"),
}

# Collection of relevant hostnames with their component
# label name, as seen in COMPONENTS
HOSTNAMES = [
    { # 0
        "hostname": "thelads.nani-games.net",
        "label": "Minecraft-001"
    },
    { # 1
        "hostname": "boi.nani-games.net",
        "label": "Minecraft-002"
    },
    { # 2
        "hostname": "heiligerts.nani-games.net",
        "label": "Teamspeak-001"
    },
    { # 3
        "hostname": "ns1.mc-host24.de",
        "label": "External DNS 1"
    },
    { # 4
        "hostname": "ns2.mc-host24.de",
        "label": "External DNS 2"
    },
    { # 5
        "hostname": "https://www.nani-games.net",
        "label": "Frontend"
    },
    { # 6
        "hostname": "88.218.227.153",
        "label": "Backend"         
    } 
]

import configparser
import os
import sys
import re

BAD_SEARCH_PATTERNS = ["index=\*"]
ERROR_MESSAGES = []
WARNING_MESSAGES = []
OUTPUT_FILE = "output.txt"

config_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".conf"):
            config_files.append(os.path.join(root, file))

for file in config_files:
    config = configparser.ConfigParser()
    config.read(file)
    for section in config.sections():
        if config.has_option(section, "search"):
            search_string = config.get(section, "search")
            # Check for bad search patterns
            for pattern in BAD_SEARCH_PATTERNS:
                if re.search(pattern, search_string):
                    ERROR_MESSAGES.append(
                        f"The search `{section}` in `{file}` contains a bad search pattern `{pattern}`."
                    )

with open(OUTPUT_FILE, "w") as f:
    if ERROR_MESSAGES:
        print(f"::set-output name=status::failure")
        f.write("### Errors :red_circle:\n")
        f.write("\n".join(ERROR_MESSAGES))
    else:
        f.write("### No errors found! :tada:\n")
    if WARNING_MESSAGES:
        f.write("\n### Warnings :warning:\n")
        f.write("\n".join(WARNING_MESSAGES))

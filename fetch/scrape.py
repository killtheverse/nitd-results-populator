import logging

from .rolls import roll_numbers, skip_numbers



PAGE_URL = "https://erp.nitdelhi.ac.in/CampusLynxNITD/studentonindex.jsp"

def generate_list():
    '''
    Generates a list of roll numbers to be considered
    '''

    # set to remove duplicate entries
    rolls = set()
    # add all numbers to set
    for entry in roll_numbers:
        valid_entry = True
        # if entry is in a form of range
        if isinstance(entry, tuple):
            if len(str(entry[0]))!=9 or len(str(entry[1]))!=9:
                valid_entry = False
            elif entry[0] >= entry[1]:
                valid_entry = False
            if valid_entry == True:
                rolls.update(range(entry[0], entry[1]))
        # if entry is a single roll number
        elif isinstance(entry, int):
            if len(str(entry))!=9:
                valid_entry = False
            if valid_entry == True:
                rolls.add(entry)
        # if entry is invalid print a message
        if valid_entry == False:
            logging.info(f"Invalid entry in roll_numbers for: {entry}. Skipping")
    
    # now remove numbers which are to be skipped
    for entry in skip_numbers:
        valid_entry = True
        if isinstance(entry, tuple):
            if len(str(entry[0]))!=9 or len(str(entry[1]))!=9:
                valid_entry = False
            elif entry[0] >= entry[1]:
                valid_entry = False
            if valid_entry == True:
                rolls.difference_update(range(entry[0], entry[1]))
        elif isinstance(entry, int):
            if len(str(entry))!=9:
                valid_entry = False
            if valid_entry == True:
                rolls.remove(entry)
        if valid_entry == False:
            logging.info(f"Invalid entry in skip_numbers for: {entry}. Skipping")
        
    # convert to list and return
    return sorted(list(rolls))




def fetch_results():
    pass
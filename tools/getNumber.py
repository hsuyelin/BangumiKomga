import re

class NumberType:
    VOLUME='volume'
    CHAPTER='chapter'
    NORMAL='normal'
    NONE='none'
    

def getNumberWithPrefix(s):
    pattern = r'vol\.(\d+)|chap\.(\d+)'
    match = re.search(pattern, s, re.IGNORECASE)

    if match:  
        if match.group(1):
            return (float(match.group(1)), NumberType.VOLUME)
        elif match.group(2):
            return (float(match.group(2)), NumberType.CHAPTER) 
    return 1.0, NumberType.NONE


def normal(s):
    # Define the pattern to match decimal numbers in the format of "xx.xx"
    decimal_pattern = r"\d+\.\d"
    # Use the `re.findall` function to search for all occurrences of the pattern in the input string
    match = re.findall(decimal_pattern, s)
    # If no decimal numbers are found, change the pattern to match integer numbers
    if not match:
        int_pattern = r"\d+|[一二三四五六七八九十]+|[①-⑩]+"
        match = re.findall(int_pattern, s)

    if match[-1]:
        return float(match[-1]), NumberType.NORMAL
    return  1.0, NumberType.NONE
        


def formatString(s):
    # e.g. 16-5
    return s.replace('-', '.').replace('_', '.')
    

def getNumber(s):
    
    s=formatString(s)
    
    number,type=getNumberWithPrefix(s)
    if not number:
        number,type=normal(s)

    return number,type
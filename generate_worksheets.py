import json
import string
import os
from xml.etree import ElementTree as ET

JSON_DIR = "json"
WORKSHEETS_DIR = "worksheets"

WORKSHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
def json_to_worksheet(jObj):
    row_charset = string.ascii_uppercase
    root = ET.Element("worksheet")
    root.attrib["xmlns"] = WORKSHEET_NS
    sheet_data = ET.SubElement(root, "sheetData")
    for i, key in enumerate(jObj):
        row = ET.SubElement(sheet_data, "row")
        row.attrib["r"] = str(i + 1)
        for j, c in enumerate([key] + jObj[key]):
            cell = ET.SubElement(row, "c")
            digits = []
            j, dig = divmod(j, 26)
            digits.append(row_charset[dig])
            while j > 0:
                j, dig = divmod(j, 26)
                digits.append(row_charset[dig])
            coord = "".join(digits) + str(i + 1)
            cell.attrib["r"] = coord
            if isinstance(c, float) or isinstance(c, int):
                valueNode = ET.SubElement(cell, "v")
                valueNode.text = str(c)
            else:
                cell.attrib["t"] = "inlineStr"
                inlineStr = ET.SubElement(cell, "is")
                sText = ET.SubElement(inlineStr, "t")
                sText.text = str(c)
    return root
    
if __name__ == "__main__":
    for fname in os.listdir(JSON_DIR):
        with open(os.path.join(JSON_DIR, fname)) as fp:
            jObj = json.load(fp)
            root = json_to_worksheet(jObj)
            pre, ext = os.path.splitext(fname)
            ET.ElementTree(root).write(os.path.join(WORKSHEETS_DIR, f"{pre}.xml"))
        

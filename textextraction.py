import PyPDF2
import re

pdf_file = open('uploads\\2.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)


def getseverity(range, value):
    pattern = r"\w+[-]?\w+:?[><]?=?\d+[-]?\d+"
    matches = re.findall(pattern, range)
    d = {}
    for i in matches:
        v = i.split(":")
        if '-' in v[-1]:
            d[v[0]] = v[-1].split('-')
        else:
            d[v[0]] = v[-1]
    severity = ''
    print(d)
    for k, v in d.items():
        if type(v) == str:
            if eval(str(value)+v):
                severity = k
                break
        else:
            if int(value)-int(v[-1]) <= 0:
                severity = k
                break
    return severity


range1 = ''
range2 = ''
for page in range(len(pdf_reader.pages)):
    pdf_page = pdf_reader.pages[page]
    page_text = pdf_page.extract_text()

    lines = page_text.split()
    print(lines)
    
    for i in range(len(lines)):
        if lines[i] == "Age:":
            age = lines[i+1]
        if lines[i] == "Gender:":
            gender = lines[i+1]
        if lines[i] == "Weight:":
            weight = lines[i+1]
        if lines[i] == "Glucose" and lines[i+1:i+3] == ['Fasting', '(FBS)']:
            value1 = lines[i+3]
            unit1 = lines[i+4]
            range1 = lines[i+5:i+14]
        if lines[i] == "Glucose" and lines[i+1:i+3] == ['Postprandial', '(PPBS)']:
            value2 = lines[i+3]
            unit2 = lines[i+4]
            range2 = lines[i+5:i+13]
range1 = "".join(range1)
range2 = "".join(range2)
severity = getseverity(range1, value1)
severity2 = getseverity(range2, value2)

print(f"Age: {age}, Gender: {gender},weight: {weight},\n Value1: {value1}, unit1: {unit1}, severity: {severity},\n Value2: {value2}, unit2: {unit2}, severity2: {severity2}")

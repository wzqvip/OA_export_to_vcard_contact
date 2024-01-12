import uuid


def parse_text(text):
    lines = text.split("\n")
    vcards = []

    for line in lines:
        parts = line.split("\t")
        FN, ORG, TEL, EMAIL, NOTE, TITLE = "", "", "", "", "", ""
        info = {}
        # print(parts)
        # print(len(parts))
        if len(parts) == 1:
            continue
        elif len(parts) == 6:
            # ['Name', 'ORG', 'TEL****', 'mail', 'gender', 'id']
            FN = parts[0]
            ORG = parts[1]
            TEL = parts[2]
            EMAIL = parts[3]
            NOTE = parts[4]
            TITLE = parts[5]
        elif len(parts) == 7:
            # ['Name', 'ORG', 'TEL****', 'mail', 'gender', 'id', 'location']
            #   0       1      2           3      4         5     6         
            FN = parts[0]
            ORG = parts[1] + " " + parts[6]
            TEL = parts[2]
            EMAIL = parts[3]
            NOTE = parts[4]
            TITLE = parts[5]
        elif len(parts) == 8:
            # ['Name', 'ORG', 'TEL****', 'mail', 'gender', 'id', 'location', '?(null)']
            #   0       1      2           3      4         5     6            7
            FN = parts[0]
            ORG = parts[1] + " " + parts[6]
            TEL = parts[2]
            EMAIL = parts[3]
            NOTE = parts[4]
            TITLE = parts[5]
        elif len(parts) > 8:
                        # ['Name', 'ORG', 'TEL****', 'mail', 'gender', 'id', 'location', 'TEL', '?(null)']
            #               0       1       2           3      4         5      6         7        8
            FN = parts[0]
            ORG = parts[1] + " " + parts[6] + " " + parts[7]
            TEL = parts[2]
            EMAIL = parts[3]
            NOTE = parts[4]
            TITLE = parts[5]
            print("Warning: line length > 8")
            print(parts)
        else:
            print(parts)
            raise ValueError("Invalid line length: " + str(len(parts)))

        info["FN"] = FN
        info["ORG"] = ORG
        info["TEL"] = TEL
        info["EMAIL"] = EMAIL
        info["NOTE"] = NOTE
        info["TITLE"] = TITLE
        info["UID"] = str(uuid.uuid4())
        vcards.append(info)

    return vcards


def generate_vcard(vcard):
    vcard_template = """BEGIN:VCARD
VERSION:3.0
FN:{FN}
ORG:{ORG}
TEL;TYPE=CELL:{TEL}
EMAIL:{EMAIL}
NOTE:{NOTE}
TITLE:{TITLE}
UID:{UID}
END:VCARD
"""
    return vcard_template.format(**vcard)


def read_txt(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def write_vcard(filename, vcards):
    with open(filename, "w", encoding="utf-8") as f:
        for vcard in vcards:
            f.write(generate_vcard(vcard))
            f.write("\n")

def autocheck(vcard1,vcard2):
    # if the text in 1 has "*" at the end, it's a bad number. Use the info in text2 to replace it.
    # if the info in 2 is not in 1, add it to 1.
    
    for i in range(len(vcard1)):
        if vcard1[i]["TEL"][-1] == "*":
            # use TITLE to find the same person in vcard2
            for j in range(len(vcard2)):
                if vcard1[i]["TITLE"] == vcard2[j]["TITLE"]:
                    if vcard2[j]["TEL"][-1] != "*":
                        print("replace " + vcard1[i]["TEL"] + " with " + vcard2[j]["TEL"])
                        vcard1[i]["TEL"] = vcard2[j]["TEL"]
                    break

    for i in range(len(vcard2)):
        # if the person in vcard2 is not in vcard1, add it to vcard1
        found = False
        for j in range(len(vcard1)):
            if vcard2[i]["TITLE"] == vcard1[j]["TITLE"]:
                found = True
                break
        if found == False:
            print("add " + vcard2[i]["TEL"] + " to vcard1")
            vcard1.append(vcard2[i])
            
    return vcard1

def check_duplicate(vcard):
    # check if there is duplicate in the list
    for i in range(len(vcard)):
        for j in range(i+1,len(vcard)):
            if vcard[i]["TITLE"] == vcard[j]["TITLE"]:
                print("duplicate found")
                print(vcard[i])
                print(vcard[j])
                
    return False

if __name__ == "__main__":
    text1 = read_txt("OA_contact_01.txt")
    text2 = read_txt("OA_contact_02.txt")

    vcard1 = parse_text(text1)
    vcard2 = parse_text(text2)
    
    vcard = autocheck(vcard1,vcard2)
    
    check_duplicate(vcard)
    print("total length" + str(len(vcard)))
    
    write_vcard("OA_contact_new.vcf", vcard)
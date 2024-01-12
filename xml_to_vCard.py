import uuid

# <row rowClick="">
#         <col text="" type="none" showvalue="8502" />
#         <col width="10%" labelid="413" text="Name " column="lastname" orderkey="lastname" linkvaluecolumn="id" linkkey="id" href="/hrm/HrmTab.jsp?_fromURL=HrmResource" target="_fullwindow" systemid="398" linkvalue="8502" value="田宇"><![CDATA[田宇]]></col>
#         <col width="10%" labelid="124" text="Department " column="departmentid" orderkey="departmentid" transmethod="weaver.hrm.company.DepartmentComInfo.getDepartmentname" linkkey="id" href="/hrm/company/HrmDepartmentDsp.jsp?hasTree=false" target="_fullwindow" systemid="403" linkvalue="886" value="886"><![CDATA[研究生]]></col>
#         <col width="10%" labelid="620" text="Mobile Telephone " column="mobile" transmethod="weaver.hrm.resource.ResourceComInfo.getMobileShow1" otherpara="column:id+9655" systemid="414" linkvalue="18885679946" value="18885679946"><![CDATA[1888567****]]></col>
#         <col width="10%" labelid="477" text="E-Mail " column="email" orderkey="email" transmethod="weaver.hrm.HrmTransMethod.getDefineContent" otherpara="email:8" systemid="418" linkvalue="tianyu@shanghaitech.edu.cn" value="tianyu@shanghaitech.edu.cn"><![CDATA[tianyu@shanghaitech.edu.cn]]></col>
#         <col width="10%" labelid="416" text="Gender " column="sex" orderkey="sex" transmethod="weaver.hrm.resource.ResourceComInfo.getSexName" systemid="399" linkvalue="0" value="0"><![CDATA[男]]></col>
#         <col width="10%" labelid="714" text="No. " column="workcode" orderkey="workcode" transmethod="weaver.hrm.HrmTransMethod.getDefineContent" otherpara="workcode:8" systemid="396" linkvalue="2020231105" value="2020231105"><![CDATA[2020231105]]></col>
#         <col width="10%" labelid="420" text="Office " column="workroom" orderkey="workroom" transmethod="weaver.hrm.HrmTransMethod.getDefineContent" otherpara="workroom:8" systemid="419" linkvalue="" value="" />
#         <col width="10%" labelid="6086" text="Position " column="jobtitle" orderkey="jobtitle" linkkey="id" transmethod="weaver.hrm.job.JobTitlesComInfo.getJobTitlesname" href="/hrm/jobtitles/HrmJobTitlesEdit.jsp" target="_fullwindow" systemid="404" linkvalue="42" value="42"><![CDATA[硕士生]]></col>
#         <col width="10%" labelid="661" text="Office Telephone " column="telephone" orderkey="telephone" transmethod="weaver.hrm.HrmTransMethod.getDefineContent" otherpara="telephone:8" systemid="415" linkvalue="" value="" />
#         <col width="10%" labelid="15709" text="Direct Superior " column="managerid" orderkey="managerid" transmethod="weaver.hrm.resource.ResourceComInfo.getResourcename" linkvaluecolumn="managerid" linkkey="id" href="/hrm/HrmTab.jsp?_fromURL=HrmResource" target="_fullwindow" systemid="420" linkvalue="" value="" />
#         <operates>
#             <operate href="/email/new/MailInBox.jsp" linkkey="opNewEmail=1&amp;isInternal=1&amp;internalto" linkvaluecolumn="id" text="Send Mail " target="_fullwindow" isalwaysshow="true" index="0" value="8502" />
#         </operates>
#     </row>


def parse_xml_data(data):
    # Splits the data into rows
    lines = data.split('<row rowClick="">')[1:]
    vcards = []

    for line in lines:
        parts = line.split("<col ")
        FN, ORG, TEL, EMAIL, NOTE, TITLE = "", "", "", "", "", ""
        info = {}
        for col in parts:
            if 'labelid="413"'in col  and "CDATA" in col:  # Name
                FN = col.split("><![CDATA[")[1].split("]]></col>")[0]
            elif 'labelid="124"'in col  and "CDATA" in col:  # Department
                ORG = col.split("><![CDATA[")[1].split("]]></col>")[0]
            elif 'labelid="420"'in col  and "CDATA" in col:  # Office
                ORG += " " + col.split("><![CDATA[")[1].split("]]></col>")[0]
            elif 'labelid="6086"'in col  and "CDATA" in col:  # Position
                ORG += " " + col.split("><![CDATA[")[1].split("]]></col>")[0]
            elif 'labelid="620"' in col:  # Mobile Telephone
                TEL = col.split('value="')[1].split('"><!')[0]
            elif 'labelid="477"' in col:  # E-Mail
                EMAIL = col.split('value="')[1].split('"><!')[0]
            elif 'labelid="714"'in col  and "CDATA" in col:  # WorkCode
                TITLE = col.split("><![CDATA[")[1].split("]]></col>")[0]
            elif 'labelid="416"'in col  and "CDATA" in col:
                NOTE = col.split("><![CDATA[")[1].split("]]></col>")[0]
            elif 'labelid="661"'in col  and "CDATA" in col:  # Office Telephone
                NOTE += " TEL:" + col.split("><![CDATA[")[1].split("]]></col>")[0]
            elif 'labelid="15709"'in col  and "CDATA" in col:  # Direct Superior
                NOTE += " " + col.split("><![CDATA[")[1].split("]]></col>")[0]

        info["FN"] = FN
        info["ORG"] = ORG
        info["TEL"] = TEL
        info["EMAIL"] = EMAIL
        info["NOTE"] = NOTE
        info["TITLE"] = TITLE
        info["UID"] = str(uuid.uuid4())
        vcards.append(info)
        # print(info)

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


if __name__ == "__main__":
    xml = read_txt("OA_2023.xml")
    vcards = parse_xml_data(xml)
    
    # for vcard in vcards:
    #     print((vcard))
    
    write_vcard("OA_2023_xml.vcf", vcards)
    
    print("Done!")
    
    
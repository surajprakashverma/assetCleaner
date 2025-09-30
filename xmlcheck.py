import xml.etree.ElementTree as ET
tree = ET.parse('sample_VFS.xml')
root = tree.getroot()
new_root = ET.Element("company")

#print(root)
for child in root.findall('employee'):
    new_child=ET.SubElement(new_root, "employee", child.attrib)

    if 'id' in new_child.attrib:
        del new_child.attrib['id']


    for subtag in child:
        if subtag.attrib == 'id':
            continue  # Skip the <note> subtag
        ET.SubElement(new_child, subtag.tag).text = subtag.text

tree = ET.ElementTree(new_root)
tree.write("filtered_employees.xml", encoding="utf-8", xml_declaration=True)


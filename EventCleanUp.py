def eventCleanUp(input_FileName):
    import xml.etree.ElementTree as ET
    NS = {'ns': 'http://namespaces.softwareag.com/webMethods/MFT_NS'}
    XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
    XS_NS = "http://www.w3.org/2001/XMLSchema"

    tree = ET.parse(input_FileName)
    root = tree.getroot()

    ET.register_namespace('', NS['ns'])
    ET.register_namespace('xsi', XSI_NS)
    ET.register_namespace('xs', XS_NS)
    for assetType in list(root):
        tag_no_ns = assetType.tag.split('}')[-1]  # Strip namespace
        name_attr = assetType.get('name')
        if tag_no_ns == 'assetType' and name_attr in ('userTemplate', 'user', 'VFS', 'partnerMapping'):
            root.remove(assetType)

    def remove_all_elements(root, tag_name):
        for parent in root.iter():
            for child in list(parent):
                if child.tag.split('}')[-1] == tag_name:
                    parent.remove(child)

    for tag in ['users', 'user', 'userId', 'eventUser', 'userTemplate']:
        remove_all_elements(root, tag)

    for elem in root.iter():
        tag_no_ns = elem.tag.split('}')[-1]
        if tag_no_ns in ('key', 'value'):
            elem.set("xmlns:xs", XS_NS)
            elem.set("xmlns:xsi", XSI_NS)
            elem.set("{%s}type" % XSI_NS, "xs:string")
    return root

import xml.etree.ElementTree as ET
def vfsCleanUp(input_filename):
    NS = {'ns': 'http://namespaces.softwareag.com/webMethods/MFT_NS'}

    tree = ET.parse(input_filename)
    root = tree.getroot()

    ET.register_namespace('', NS['ns'])

    for assetType in list(root):
        tag_no_ns = assetType.tag.split('}')[-1]  # Strip namespace
        name_attr = assetType.get('name')
        if tag_no_ns == 'assetType' and name_attr in ('userTemplate', 'user'):
            root.remove(assetType)

    def remove_all_elements(root, tag_name):
        for parent in root.iter():
            for child in list(parent):
                if child.tag.split('}')[-1] == tag_name:
                    parent.remove(child)

    remove_all_elements(root, 'users')
    remove_all_elements(root, 'user')
    remove_all_elements(root, 'userId')
    return root



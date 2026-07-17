def eventCleanUp(input_FileName):
    from lxml import etree
    import copy

    input_file = input_FileName
    output_file = "scheduleAction.xml"

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(input_file, parser)

    root = tree.getroot()

    # Find scheduleAction
    schedule_action = root.xpath(
        './/*[local-name()="assetType" and @name="scheduleAction"]'
    )[0]

    # Remove <depends> tags
    for depends in schedule_action.xpath('.//*[local-name()="depends"]'):
        depends.getparent().remove(depends)

    # Create new root with original namespace + attributes
    new_root = etree.Element(
        root.tag,
        nsmap=root.nsmap,
        attrib=root.attrib
    )

    # Copy scheduleAction preserving xmlns=""
    new_root.append(copy.deepcopy(schedule_action))

    # Write output
    new_tree = etree.ElementTree(new_root)
    return (new_tree)

def eventCleanUp(input_FileName):
    from lxml import etree
    import copy

    input_file = input_FileName

    parser = etree.XMLParser(
        remove_blank_text=True,
        recover=True
    )

    tree = etree.parse(
        input_file,
        parser
    )

    root = tree.getroot()

    # Create new root with original namespace and attributes
    new_root = etree.Element(
        root.tag,
        nsmap=root.nsmap,
        attrib=root.attrib
    )

    # Find required assetType blocks
    required_asset_types = root.xpath(
        './/*[local-name()="assetType" and '
        '(@name="scheduleAction" or @name="postProcessEvent")]'
    )

    if not required_asset_types:
        raise ValueError(
            "No scheduleAction or postProcessEvent assetType found in the uploaded XML."
        )

    for asset_type in required_asset_types:

        cleaned_asset_type = copy.deepcopy(
            asset_type
        )

        # Remove all <depends> tags from this assetType
        for depends in cleaned_asset_type.xpath(
            './/*[local-name()="depends"]'
        ):
            parent = depends.getparent()

            if parent is not None:
                parent.remove(
                    depends
                )

        # Append cleaned assetType preserving xmlns=""
        new_root.append(
            cleaned_asset_type
        )

    new_tree = etree.ElementTree(
        new_root
    )

    return new_tree

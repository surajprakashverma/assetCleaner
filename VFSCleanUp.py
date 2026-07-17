from lxml import etree as ET
import re


def vfsCleanUp(input_file, vfs_paths):

    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(input_file, parser)
    root = tree.getroot()

    def strip_ns(tag):
        if "}" in tag:
            return tag.split("}")[-1]
        return tag

    def normalize_path(path):

        if not path:
            return ""

        return path.strip().rstrip("/")

    def compare_key(path):

        path = normalize_path(path)
        return path.lstrip("/")

    def split_vfs_path(path):

        path = normalize_path(path)

        parts = path.rsplit("/", 1)

        if len(parts) != 2:
            return None, None

        parent_path = parts[0]
        vfs_name = parts[1]

        return parent_path, vfs_name

    def convert_input_to_list(vfs_paths):
        """
        Supports:
        1. Comma-separated input
        2. Newline-separated input
        3. <br>-separated input
        4. Python list input
        """

        if isinstance(vfs_paths, list):
            return [
                path.strip()
                for path in vfs_paths
                if path and path.strip()
            ]

        if isinstance(vfs_paths, str):
            vfs_paths = vfs_paths.replace("<br>", "\n")
            vfs_paths = vfs_paths.replace("<br/>", "\n")
            vfs_paths = vfs_paths.replace("<br />", "\n")

            return [
                path.strip()
                for path in re.split(r"[,\n]+", vfs_paths)
                if path.strip()
            ]

        return []

    def remove_elements_by_local_name(root_node, tag_name):
       

        elements = root_node.xpath(".//*[local-name()=$name]", name=tag_name)

        for elem in elements:
            parent = elem.getparent()

            if parent is not None:
                parent.remove(elem)

    def remove_empty_depends(root_node):
        

        depends_elements = root_node.xpath(".//*[local-name()='depends']")

        for depends in depends_elements:
            has_child = len(depends) > 0
            has_text = depends.text and depends.text.strip()

            if not has_child and not has_text:
                parent = depends.getparent()

                if parent is not None:
                    parent.remove(depends)

    # Convert input paths
    vfs_paths_list = convert_input_to_list(vfs_paths)

    allowed_vfs = set()

    for path in vfs_paths_list:
        parent_path, vfs_name = split_vfs_path(path)

        if parent_path and vfs_name:
            allowed_vfs.add(
                (
                    compare_key(parent_path),
                    normalize_path(vfs_name)
                )
            )

    
    for assetType in list(root):
        tag_name = strip_ns(assetType.tag)
        name_attr = assetType.get("name")

        if tag_name == "assetType" and name_attr != "VFS":
            root.remove(assetType)

    for assetType in list(root):
        tag_name = strip_ns(assetType.tag)
        name_attr = assetType.get("name")

        if tag_name != "assetType" or name_attr != "VFS":
            continue

        for asset in list(assetType):
            virtual_parent_path = ""
            vfs_name = ""

            for elem in asset.iter():
                elem_tag = strip_ns(elem.tag)

                if elem_tag == "virtualParentPath":
                    virtual_parent_path = elem.text.strip() if elem.text else ""

                elif elem_tag == "VFSName":
                    vfs_name = elem.text.strip() if elem.text else ""

            virtual_parent_path_key = compare_key(virtual_parent_path)
            vfs_name_key = normalize_path(vfs_name)

            if (virtual_parent_path_key, vfs_name_key) not in allowed_vfs:
                assetType.remove(asset)

        if len(assetType) == 0:
            root.remove(assetType)

    remove_elements_by_local_name(root, "users")

    remove_elements_by_local_name(root, "userId")

    
    remove_elements_by_local_name(root, "user")

    remove_empty_depends(root)

    return tree

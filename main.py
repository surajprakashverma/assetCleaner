from io import BytesIO
from flask import Flask, request, send_file, render_template
import xml.etree.ElementTree as ET
from EventCleanUp import eventCleanUp
from VFSCleanUp import vfsCleanUp
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        asset_type = request.form.get('assettype')
        if uploaded_file:
            # Save the file with its original filename
            if uploaded_file and uploaded_file.filename.endswith('.xml'):

                # Read the file into memory (as bytes)
                xml_bytes = uploaded_file.read()
                root_element = ''
                if asset_type=='event':
                    root_element=eventCleanUp(BytesIO(xml_bytes))
                elif asset_type=='vfs':
                    root_element=vfsCleanUp(BytesIO(xml_bytes))
                tree = ET.ElementTree(root_element)
                output = BytesIO()
                tree.write(output, encoding='utf-8')
                output.seek(0)
                return send_file(
                    output,
                    mimetype='application/xml',
                    as_attachment=True,
                    download_name=uploaded_file.filename
                )

        else:
            return 'No file uploaded!'
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

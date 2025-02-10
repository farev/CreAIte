from flask import Flask, render_template, request, send_file, jsonify
from flask_bootstrap import Bootstrap5
from ToolGenerator import ToolGenerator
import os
import tempfile
import zipfile
import io
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
Bootstrap5(app)
generator = ToolGenerator()

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_tool():
    try:
        description = request.form.get('description')
        if not description:
            return jsonify({'error': 'Description is required'}), 400

        # Generate the tool
        code, filename, readme = generator.generate_tool(description)

        # Create a zip file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            # Add the tool file
            zf.writestr(filename, code)
            # Add the README
            zf.writestr('README.md', readme)

        # Prepare the zip file for download
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{filename.replace(".py", "")}_tool.zip'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False) 
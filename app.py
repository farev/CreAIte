from flask import Flask, render_template, request, send_file, jsonify
from flask_bootstrap import Bootstrap5
from ToolGenerator import ToolGenerator
import os
import tempfile
import zipfile
import io
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

app = Flask(__name__)
Bootstrap5(app)
generator = ToolGenerator()

# Handle Azure's reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure for production
app.config['PROPAGATE_EXCEPTIONS'] = True

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Setup Azure Application Insights if key is available
INSTRUMENTATION_KEY = os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY')
if INSTRUMENTATION_KEY:
    try:
        from opencensus.ext.azure import metrics_exporter
        from opencensus.ext.azure.log_exporter import AzureLogHandler
        from opencensus.ext.flask.flask_middleware import FlaskMiddleware

        # Initialize Flask Middleware for App Insights
        middleware = FlaskMiddleware(
            app,
            exporter=metrics_exporter.new_metrics_exporter(
                enable_standard_metrics=True,
                connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}'
            )
        )

        # Add Azure Log Handler
        logger.addHandler(AzureLogHandler(
            connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}'
        ))
        
        logger.info('Application Insights initialized successfully')
    except Exception as e:
        logger.warning(f'Failed to initialize Application Insights: {str(e)}')
        # Add a basic stream handler if App Insights fails
        logging.basicConfig(level=logging.INFO)
else:
    # Add basic logging if no App Insights key
    logging.basicConfig(level=logging.INFO)
    logger.warning('No Application Insights key found, using basic logging')

@app.route('/', methods=['GET'])
def index():
    # Log page visit
    logger.info('Home page visited', extra={'custom_dimensions': {
        'user_agent': request.headers.get('User-Agent')
    }} if INSTRUMENTATION_KEY else {})
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_tool():
    try:
        description = request.form.get('description')
        if not description:
            logger.warning('Empty description submitted')
            return jsonify({'error': 'Description is required'}), 400

        # Log tool generation attempt
        logger.info('Tool generation started', extra={'custom_dimensions': {
            'description_length': len(description)
        }})

        # Generate the tool
        code, filename, readme = generator.generate_tool(description)

        # Create a zip file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            # Add the tool file
            zf.writestr(filename, code)
            # Add the README
            zf.writestr('README.md', readme)

        # Log successful generation
        logger.info('Tool generated successfully', extra={'custom_dimensions': {
            'filename': filename,
            'code_length': len(code)
        }})

        # Prepare the zip file for download
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{filename.replace(".py", "")}_tool.zip'
        )

    except Exception as e:
        # Log error
        logger.error(f'Tool generation failed: {str(e)}', extra={'custom_dimensions': {
            'error_type': type(e).__name__
        }})
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 
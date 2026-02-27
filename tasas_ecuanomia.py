import os

from tasas_ecuanomia_dash import app, server

# Backward-compatible entrypoint:
# If Render is configured to run `python tasas_ecuanomia.py`,
# this will still boot the Dash app that contains both views.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False)

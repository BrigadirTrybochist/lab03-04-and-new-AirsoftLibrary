"""Entry point for the lab03 Flask project.

If the larger `AirsoftArsenal` application exists in the workspace, delegate
to that app (so the Airsoft Arsenal site runs). Otherwise run a small demo
app that uses the local templates.

Note: we intentionally do NOT import any Replit-specific files; those live
under `AirsoftArsenal/.local` or similar and are ignored.
"""

import os
import sys
from flask import Flask, render_template

# Try to locate and delegate to the AirsoftArsenal app if present
app = None
try:
    # First try a local copy placed under lab03-flaskProject/airsoft_site
    local_site_dir = os.path.join(os.path.dirname(__file__), 'airsoft_site')
    airsoft_app = None
    if os.path.isdir(local_site_dir):
        local_app_path = os.path.join(local_site_dir, 'app.py')
        if os.path.isfile(local_app_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location('airsoft_local_app', local_app_path)
            if spec and spec.loader:
                airsoft_mod = importlib.util.module_from_spec(spec)
                sys.modules['airsoft_local_app'] = airsoft_mod
                # Temporarily ensure local_site_dir is on sys.path so absolute imports inside the module work
                inserted = False
                if local_site_dir not in sys.path:
                    sys.path.insert(0, local_site_dir)
                    inserted = True

                previous_app_mod = sys.modules.get('app')
                sys.modules['app'] = airsoft_mod
                try:
                    spec.loader.exec_module(airsoft_mod)
                finally:
                    if previous_app_mod is not None:
                        sys.modules['app'] = previous_app_mod
                    else:
                        del sys.modules['app']
                    if inserted:
                        try:
                            sys.path.remove(local_site_dir)
                        except ValueError:
                            pass

                airsoft_app = getattr(airsoft_mod, 'app', None)

    # If no local copy, fall back to sibling AirsoftArsenal folder
    if not airsoft_app:
        workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        airsoft_path = os.path.join(workspace_root, 'AirsoftArsenal')
        if os.path.isdir(airsoft_path):
            airsoft_app_path = os.path.join(airsoft_path, 'app.py')
            if os.path.isfile(airsoft_app_path):
                import importlib.util
                spec = importlib.util.spec_from_file_location('airsoft_app', airsoft_app_path)
                if spec and spec.loader:
                    airsoft_mod = importlib.util.module_from_spec(spec)
                    sys.modules['airsoft_app'] = airsoft_mod
                    inserted = False
                    if airsoft_path not in sys.path:
                        sys.path.insert(0, airsoft_path)
                        inserted = True

                    previous_app_mod = sys.modules.get('app')
                    sys.modules['app'] = airsoft_mod
                    try:
                        spec.loader.exec_module(airsoft_mod)
                    finally:
                        if previous_app_mod is not None:
                            sys.modules['app'] = previous_app_mod
                        else:
                            del sys.modules['app']
                        if inserted:
                            try:
                                sys.path.remove(airsoft_path)
                            except ValueError:
                                pass

                    airsoft_app = getattr(airsoft_mod, 'app', None)

    if airsoft_app:
        app = airsoft_app
        print('Delegating to AirsoftArsenal.app')
except Exception as e:
    # If anything goes wrong, fall back to the simple lab03 app
    print(f'Could not load AirsoftArsenal app (falling back). Error: {e}')
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')


if __name__ == '__main__':
    # Run with reloader off for clearer console output during development
    app.run(debug=True, use_reloader=False)

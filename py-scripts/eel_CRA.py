"""Main Python application file for the EEL-CRA demo."""

import os
import platform
import random
import sys

import eel

"""

    TODO:
    - Add in Eel support for final built assets from next
    - Organize file structure better

"""

"""
@eel.expose  # Expose function to JavaScript
def say_hello_py(x):
    """
# Print message from JavaScript on app initialization, then call a JS function.
"""
    print('Hello from %s' % x)  # noqa T001
    eel.say_hello_js('Python {from within say_hello_py()}!')

"""
"""
@eel.expose
def expand_user(folder):
    """
# Return the full path to display in the UI.
"""
    return '{}/*'.format(os.path.expanduser(folder))

"""
"""
@eel.expose
def pick_file(folder):
    """
# Return a random file from the specified folder.
"""
    folder = os.path.expanduser(folder)
    if os.path.isdir(folder):
        listFiles = [_f for _f in os.listdir(
            folder) if not os.path.isdir(os.path.join(folder, _f))]
        if len(listFiles) == 0:
            return 'No Files found in {}'.format(folder)
        return random.choice(listFiles)
    else:
        return '{} is not a valid folder'.format(folder)

"""


def start_eel(develop):
    """Start Eel with either production or development configuration."""
    print('starting eel server...')
    if develop:
        directory = 'ns-compass/pages'
        app = None
        page = {'port': 3000}
    else:
        directory = 'build'
        app = 'chrome-app'
        page = 'index.html'
        sys.exit(
            "Production support is not implemented yet, please run this script with the `true` command line arg"
        )

    eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])

    eel_kwargs = dict(
        host='localhost',
        port=8080,
        size=(1280, 800),
    )
    print('eel server running...')
    try:
        eel.start(page, mode=app, **eel_kwargs)
    except EnvironmentError:
        # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
        if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
            eel.start(page, mode='edge', **eel_kwargs)
        else:
            raise


if __name__ == '__main__':
    import sys

    # Pass any second argument to enable debugging
    start_eel(develop=len(sys.argv) == 2)

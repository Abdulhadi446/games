from flask import Flask, send_from_directory, abort, render_template
import os

app = Flask(__name__, template_folder="templates")
BASE_DIR = os.path.abspath(".")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    full_path = os.path.join(BASE_DIR, path)

    if os.path.isdir(full_path):  
        # Look for index.html
        index_file = os.path.join(full_path, "index.html")
        if os.path.isfile(index_file):
            return send_from_directory(full_path, "index.html")
        else:
            # Show file list using list.html
            try:
                files = sorted(os.listdir(full_path))
                file_links = []
                for f in files:
                    if os.path.isdir(os.path.join(full_path, f)):
                        f += "/"  # Mark folders
                    file_links.append(f)

                parent = None
                if path:
                    parent = "/" + "/".join(path.strip("/").split("/")[:-1])

                return render_template(
                    "list.html",
                    path=path,
                    files=file_links,
                    # parent=parent,
                    file_count=len(file_links)
                )
            except PermissionError:
                abort(403)

    elif os.path.isfile(full_path):
        return send_from_directory(BASE_DIR, path)

    else:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
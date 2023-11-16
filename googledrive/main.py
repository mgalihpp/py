from flask import Flask, request, render_template, send_from_directory
from g_drive_service import GoogleDriveService
from googleapiclient.http import MediaIoBaseUpload
from datetime import datetime
from io import BytesIO
from apiclient import errors
import os

app = Flask(__name__)
service = GoogleDriveService().build()
DOWNLOAD_FOLDER = "downloads"  # Define a folder to store downloaded files
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER  # Set the download folder


@app.get("/")
def index():
    return render_template("index.html")


@app.route("/get-file/<file_id>/")
def get_file(file_id):
    try:
        # Use the Google Drive API to get the file's metadata
        file_metadata = service.files().get(fileId=file_id).execute()

        # Get the direct download link for the file
        download_link = file_metadata.get("webViewLink")

        if download_link:
            # Use send_from_directory to serve the file
            download_filename = file_metadata.get("name")
            download_path = os.path.join(
                app.config["DOWNLOAD_FOLDER"], download_filename
            )

            if not os.path.exists(download_path):
                # Download the file and save it to the download folder
                response = request.get(download_link)
                with open(download_path, "wb") as file:
                    file.write(response.content)

            return send_from_directory(
                app.config["DOWNLOAD_FOLDER"], download_filename, as_attachment=True
            )
        else:
            return "File not found."
    except errors.HttpError as error:
        return {"status": "Fail", "error_message": error.reason}
    except Exception as e:
        return {"status": "Fail", "error_message": str(e)}


@app.get("/all-files")
def get_all_files():
    selected_field = "files(id, name, webViewLink)"
    return service.files().list(fields=selected_field).execute()


@app.get("/files-with-id/<file_id>/")
def get_files_with_id(file_id):
    selected_field = "id, name, webViewLink"
    return service.files().get(fileId=file_id, fields=selected_field).execute()


@app.get("/files-in-folder/<folder_id>/")
def get_files_in_folder(folder_id):
    selected_field = "files(id, name, webViewLink, mimeType)"
    query = f" '{folder_id}' in parents "

    return service.files().list(q=query, fields=selected_field).execute()


@app.get("/files-with-type")
def get_files_with_type():
    selected_mimetype = request.json.get("mimetype")
    folder_mimeType = "application/vnd.google-apps.folder"

    selected_field = "files(id, name, webViewLink, mimeType)"

    query = f"""
        mimeType != '{folder_mimeType}' 
        and 
        mimeType = '{selected_mimetype}' 
    """

    return service.files().list(q=query, fields=selected_field).execute()


@app.post("/upload")
def upload_file():
    uploaded_file = request.files.get("file")

    buffer_memory = BytesIO()
    uploaded_file.save(buffer_memory)

    media_body = MediaIoBaseUpload(
        uploaded_file, uploaded_file.mimetype, resumable=True
    )

    created_at = datetime.now().strftime("%Y%m%d%H%M%S")
    file_metadata = {"name": f"{uploaded_file.filename} ({created_at})"}

    returned_fields = "id, name, mimeType, webViewLink, exportLinks"

    upload_response = (
        service.files()
        .create(body=file_metadata, media_body=media_body, fields=returned_fields)
        .execute()
    )

    return upload_response


@app.delete("/file/<file_id>/")
def delete_file(file_id):
    try:
        service.files().delete(fileId=file_id).execute()
        return {"status": "OK"}
    except errors.HttpError as error:
        return {"status": "Fail", "error_message": error.reason}
    except Exception as e:
        return {"status": "Fail", "error_message": str(e)}


if __name__ == "__main__":
    app.run(debug=True)

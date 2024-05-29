from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import getpass

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    password = request.form.get('password')
    if password == "ayush":
        return redirect(url_for('menu'))
    else:
        flash('Authentication failed')
        return redirect(url_for('index'))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form.get('command')
    if command:
        output = run_command(command)
        flash(output)
    else:
        flash("No command provided")
    return redirect(url_for('menu'))

@app.route('/local_create_file', methods=['POST'])
def local_create_file():
    file_name = request.form.get('file_name')
    if file_name:
        output = run_command(f"touch {file_name}")
        flash(output)
    else:
        flash("File name cannot be empty")
    return redirect(url_for('menu'))

@app.route('/local_create_folder', methods=['POST'])
def local_create_folder():
    folder_name = request.form.get('folder_name')
    if folder_name:
        output = run_command(f"mkdir {folder_name}")
        flash(output)
    else:
        flash("Folder name cannot be empty")
    return redirect(url_for('menu'))

@app.route('/show_date', methods=['POST'])
def show_date():
    output = run_command("date")
    flash(output)
    return redirect(url_for('menu'))

@app.route('/show_calendar', methods=['POST'])
def show_calendar():
    output = run_command("cal")
    flash(output)
    return redirect(url_for('menu'))

@app.route('/install_software', methods=['POST'])
def install_software():
    software_name = request.form.get('software_name')
    if software_name:
        output = run_command(f"yum install -y {software_name}")
        flash(output)
    else:
        flash("Software name cannot be empty")
    return redirect(url_for('menu'))

@app.route('/show_ip', methods=['POST'])
def show_ip():
    output = run_command("ifconfig")
    flash(output)
    return redirect(url_for('menu'))

@app.route('/ssh_execute', methods=['POST'])
def ssh_execute():
    remote_ip = request.form.get('remote_ip')
    remote_user = request.form.get('remote_user')
    command = request.form.get('remote_command')
    if remote_ip and remote_user and command:
        output = run_command(f"ssh {remote_user}@{remote_ip} {command}")
        flash(output)
    else:
        flash("IP, user, and command cannot be empty")
    return redirect(url_for('menu'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

# Apk-Pusher-
A lightweight local web tool for deploying signed APKs to Android set-top boxes over ADB.

## Features
- Drag & drop APK deployment
- Automatic ADB connect, root, remount, push and reboot
- Live deployment log in the browser
- No dependencies — pure Python standard library

## Requirements
- Python 3.6+
- ADB installed and in PATH (`brew install android-platform-tools`)

## Usage
```bash
python3 bada_pusher.py
```
Opens automatically at `http://localhost:7777`

## Workflow
1. Enter device IP and ADB port
2. Drag & drop your signed APK
3. Click **Test Connection** to verify device is reachable
4. Click **⚡ Push APK** — done

import liboxide

print("Applications:")
for name, app in liboxide.apps.applications.items():
    print(f"  {name}: {app.bin}")

print(f"Running: {', '.join(list(liboxide.apps.runningApplications.keys()))}")
print(f"Paused: {', '.join(list(liboxide.apps.pausedApplications.keys()))}")
print(f"Previous: {', '.join(liboxide.apps.previousApplications)}")

print("Notifications:")
for notification in liboxide.notification.allNotifications:
    app = liboxide.apps.getApplication(notification.application)
    print(f"  {notification.identifier} owned by {app.displayName}")

path = liboxide.settings.get("apps", "lockscreenApplication")
app = liboxide.Application(path)
print(f"Lockscreen App: {app.displayName}")
autoLock = liboxide.settings.get("autoLock")
print(f"Automatic lock: {autoLock} minutes")
liboxide.wifi.scan(False)
bss = liboxide.wifi.on.bssFound()
print(f"Found BSS for SSID: {bss.ssid}")

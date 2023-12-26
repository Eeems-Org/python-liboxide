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
print(f"Battery level: {liboxide.power.batteryLevel}")
while True:
    batteryLevel = liboxide.power.on.batteryLevelChanged()
    print(f"Battery level: {batteryLevel}")

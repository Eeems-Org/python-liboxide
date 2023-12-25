import liboxide

print("Applications:")
for name, app in liboxide.Apps.applications.items():
    print(f"  {name}: {app.bin}")

print(f"Running: {', '.join(list(liboxide.Apps.runningApplications.keys()))}")
print(f"Paused: {', '.join(list(liboxide.Apps.pausedApplications.keys()))}")
print(f"Previous: {', '.join(liboxide.Apps.previousApplications)}")

import os
import platform

system = (platform.system())
release = (platform.release())

print("System: %s " % (system))
print("Release: %s " % (release))
print("OS name: %s "% (os.name))

if ("Linux" in system):
    print("PASS")
else:
    print("FAIL")

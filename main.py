import os

# get reference to webcam depending on operating system
# current support for windows + linux
webcam_ref = None

if os.name == "posix":
    webcam_ref = os.name
elif os.name == "nt":
    webcam_ref = os.name
else:
    raise Exception("Sorry your operating system does not work with the package")

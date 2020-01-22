import flywheel
import re
import json

# Grab Config
CONFIG_FILE_PATH = '/flywheel/v0/config.json'
with open(CONFIG_FILE_PATH) as config_file:
    config = json.load(config_file)

api_key = config['inputs']['api_key']['key']
session_id = config['destination']['id']


#api_key = "uscdni.flywheel.io:oepWHsARl4CUfN6me6"
fw = flywheel.Flywheel(api_key)
session = fw.get_session(session_id)

#loop through acquisitions
for acquisition in session.acquisitions():
	if "fmap" in acquisition.label:
		for file in acquisition.files:
			if file.type == "nifti":

				#Check for magnitude 1 image
				pattern = "^.*_e1\\.nii\\.gz";
				if re.match(pattern,file.name):
					mag1 = file

				#Check for magnitude 2 image
				pattern = "^.*_e2\\.nii\\.gz";
				if re.match(pattern,file.name):
					mag2 = file

				#Check for phase image
				pattern = "^.*_e2_ph\\.nii\\.gz";
				if re.match(pattern,file.name):
					phase = file

#Determine echo times from the mag images
mag1_meta = fw.acquisitions_api.get_acquisition_file_info(mag1.parent.id,mag1.name) 
echotime1 = mag1_meta.info["EchoTime"]
mag2_meta = fw.acquisitions_api.get_acquisition_file_info(mag2.parent.id,mag2.name) 
echotime2 = mag2_meta.info["EchoTime"]
print("EchoTime1: %.5f EchoTime2: %.5f" % (echotime1,echotime2))

#Update the phasediff metadata with those values
phase.update_info({"EchoTime1":echotime1,"EchoTime2":echotime2})


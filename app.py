import natsume
import modules.utils as natsumeUtils
import sys


natsumeApp = natsume.NatsumeAI(debug=True)
utils = natsumeUtils.NatsumeUtils()
opState = natsumeApp.debugStats()




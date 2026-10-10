#!/bin/bash
# Obfuscated Dropper Simulator
PAYLOAD="ZWNobyAiQ29ubmVjdGluZyB0byBDMiBOb2RlLi4uIgpDTT0iZXZpbC1jMi5jb20iCmVjaG8gJENNIHwgYmFzZTY0Cg=="
eval $(echo $PAYLOAD | base64 -d)

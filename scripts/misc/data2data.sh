

uses=durel_system/upload_formats/test_uug/uses/Vorwort.csv
judgments=durel_system/upload_formats/test_uug/judgments/Vorwort.csv
usesout=durel_system/upload_formats/test_uug/uses/Vorwort_.csv
judgmentsout=durel_system/upload_formats/test_uug/judgments/Vorwort_.csv

python3 scripts/misc/data2data.py $uses $judgments $usesout $judgmentsout

echo Current path is: %CD%
pyinstaller --onefile --debug=all --name lamf_analysis --collect-all ScanImageTiffReader --collect-all skimage src\lamf_analysis\__main__.py
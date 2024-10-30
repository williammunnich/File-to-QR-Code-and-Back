# File to QR Code and Back
 With data breaches and several personal data losses, I am interested in storing data that is both redundant and resilient. The intended use case for this project is to insert photograph files, get them broken up into QR code, put them into a pdf which culd be printed, then be able to reasemble them later to get the original file. QR codes themselves are reduntant and large parts of the code can be damaged but still be able to reconstruct their data. Paper storage is relatively stable in ways that electronic formats are not  as in they can survice EMPs and Microwaves. That is my thinking at least and redundant and varied data starage solutions should be used.

pip install -r requirements.txt
source /qr_venv/bin/activate

python split.py

python recombine.py

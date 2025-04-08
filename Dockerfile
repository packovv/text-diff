FROM --platform=linux/amd64 cdrx/pyinstaller-windows:python3

WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN pyinstaller --onefile text_diff_gui.py 
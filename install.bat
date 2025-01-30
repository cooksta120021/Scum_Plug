@echo off
git clone https://github.com/cooksta120021/Scum_Plug.git
cd Scum_Plug
python -m venv project_venv
call project_venv\Scripts\activate
pip install -r requirements.txt
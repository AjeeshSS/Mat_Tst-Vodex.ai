pip install fastapi uvicorn sqlalchemy
pip install motor
pip install pydantic[email]


uvicorn main:app    # run

pip freeze > requirements.txt

uvicorn <your_filename>:app --reload  # reload


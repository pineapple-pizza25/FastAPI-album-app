from fastapi import FastAPI, Depends, Request, Form, status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

templates = Jinja2Templates(directory="templates")

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    albums = db.query(models.Album).all()
    return templates.TemplateResponse("base.html",
                                      {"request": request, "album_list": albums})

@app.post("/add")
def add(request: Request, title: str = Form(...), artist: str = Form(...), rating: int = Form(...), db:Session = Depends(get_db)):
    new_album = models.Album(title=title, artist=artist, rating=rating)
    db.add(new_album)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/update/{album_id}")
def update(request: Request, album_id: int, db: Session = Depends(get_db)):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@app.get("/delete/{album_id}")
def delete(request: Request, album_id: int, db: Session = Depends(get_db)):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    db.delete(album)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

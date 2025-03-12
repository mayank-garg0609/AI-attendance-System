from fastapi import FastAPI, Depends, status, HTTPException
from typing import Optional
from app import model, schemas, token, oauth2
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.hashing import Hash
import uvicorn
# import sys
# import os

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

@app.get("/")
def index():
    return {"message": "Hell"}

@app.get("/user")
def user(limit=10, verified: bool = True, sort: Optional[str] = None):
    return {"message": f"{limit}, {'true' if verified else 'false'}"}

# @app.get("/user/{id}")
# def get_user(id: int):
#     return {"id": id}

# @app.get("/blogs")
# def all(db:Session = Depends(get_db)):
#     blogs=db.query(model.Blog).all()
#     return blogs

# @app.get('/blog/{id}', status_code=200)
# def show(id, db: Session = Depends (get_db)):
#     blog = db.query(model.Student).filter(model.Student.student_id == id).first()
#     if not blog:
#         raise HTTPException(status_code=404, detail="Blog not found")
#         # response.status_code = status. HTTP_404_NOT_FOUND
#         # return {'detail': f"Blog with the id {id} is not available"}
#     return blog

# @app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id, db: Session = Depends(get_db)):
#     blog = db.query(model.Student).filter(model.Student.student_id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status. HTTP_404_NOT_FOUND,
#                             detail=f" Blog with id {id} not found")
#     blog.update(request)
#     db.commit()
#     return 'updated'

@app.post("/attendance/add")
def attendance(att: schemas.att, db: Session = Depends(get_db)):
    new_attendance = model.Attendance(student_id=att.student_id, course_id=att.course_id, date=att.date, present=True)
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

# @app.get("/profile/student/{id}", response_model=List[schemas.ShowUserProfile])
@app.get("/profile/student/{id}", response_model=schemas.ShowUserProfile)
def show_profile(id:int, db: Session = Depends(get_db),get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(model.Student).filter(model.Student.student_id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available"
        )
    return user

@app.get("/student/{id}",tags=["user"])
def student(id:int, db: Session = Depends(get_db)):
    user = db.query(model.Student).filter(model.Student.student_id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available")

    return user

@app.post("/login")
def login(request:schemas.LoginBody, db: Session = Depends(get_db)):
    user=db.query(model.Student).filter(model.Student.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {request.email} is not available")
    if not user.password==request.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    access_token=token.create_access_token(data={"sub": user.email, "role": "student"})
    return {"access_token": access_token,"token_type": "bearer"}

# Hash.bcrypt(request.password)
@app.post('/user/create')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_student = model.Student(student_name=request.name, email=request.email, password=request.password)
    db.add(new_student)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=9000)


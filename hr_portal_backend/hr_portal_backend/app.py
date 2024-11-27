from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from hr_portal_backend.utils.auth import hash_password, verify_password, create_access_token, decode_access_token
from hr_portal_backend.utils.database import User, UserInformation, get_db
from fastapi.middleware.cors import CORSMiddleware
# Initialize FastAPI app
app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)
# OAuth2 scheme to extract token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=True)

# Pydantic models for request validation
class LoginRequest(BaseModel):
    email: str
    password: str

class UserInfoRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    sex: str | None = None
    sexual_orientation: str | None = None
    preferred_pronouns: str | None = None
    phone_number: str | None = None
    ssn: str | None = None

# Endpoints

@app.post("/signup")
async def signup(request: LoginRequest, db: Session = Depends(get_db)):
    # Check if the user already exists in the database
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and save the user in the database
    hashed_password = hash_password(request.password)
    new_user = User(email=request.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "email": new_user.email}


@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    email = request.email
    password = request.password
    
    # Retrieve the user from the database by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate a JWT token for the authenticated user
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    email = payload.get("sub")
    
    # Retrieve the user from the database by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"id": user.id, "email": user.email}


@app.put("/me/info")
async def update_user_info(
    request: UserInfoRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    # Decode the token to get user email
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    email = payload.get("sub")
    
    # Retrieve the user from the database by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user information already exists
    user_info = db.query(UserInformation).filter(UserInformation.user_id == user.id).first()
    
    if not user_info:
        # Create new user information if it doesn't exist
        user_info = UserInformation(user_id=user.id)
        db.add(user_info)

    # Update user's personal information
    if request.first_name is not None:
        user_info.first_name = request.first_name
    if request.last_name is not None:
        user_info.last_name = request.last_name
    if request.age is not None:
        user_info.age = request.age
    if request.sex is not None:
        user_info.sex = request.sex
    if request.sexual_orientation is not None:
        user_info.sexual_orientation = request.sexual_orientation
    if request.preferred_pronouns is not None:
        user_info.preferred_pronouns = request.preferred_pronouns
    if request.phone_number is not None:
        user_info.phone_number = request.phone_number
    if request.ssn is not None:
        user_info.ssn = request.ssn
    
    # Save changes to the database
    db.commit()
    
    return {"message": "User information updated successfully"}


@app.get("/me/info")
async def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decode the token to get user email
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    email = payload.get("sub")
    
    # Retrieve the user from the database by email and their associated information
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's personal information from UserInformation table
    user_info = db.query(UserInformation).filter(UserInformation.user_id == user.id).first()
    
    if not user_info:
        return {
        "id": user.id,
        "email": user.email,
        "first_name": "",
        "last_name": "",
        "age": "",
        "sex": "",
        "sexual_orientation": "",
        "preferred_pronouns": "",
        "phone_number": "",
        "ssn": "",
    }
    
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user_info.first_name,
        "last_name": user_info.last_name,
        "age": user_info.age,
        "sex": user_info.sex,
        "sexual_orientation": user_info.sexual_orientation,
        "preferred_pronouns": user_info.preferred_pronouns,
        "phone_number": user_info.phone_number,
        "ssn": user_info.ssn,
    }
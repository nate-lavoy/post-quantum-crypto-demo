# app.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .utils.auth import hash_password, verify_password, create_access_token, decode_access_token
from .utils.database import User, UserInformation, get_db
from .utils.encryption import EncryptionManager

app = FastAPI()
encryption_manager = EncryptionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=True)

class LoginRequest(BaseModel):
    email: str
    password: str

class UserInfoRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    sexual_orientation: Optional[str] = None
    preferred_pronouns: Optional[str] = None
    phone_number: Optional[str] = None
    ssn: Optional[str] = None

class DecryptRequest(BaseModel):
    private_key: str

@app.post("/signup")
async def signup(request: LoginRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(request.password)
    new_user = User(email=request.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "email": new_user.email}

@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"id": user.id, "email": user.email}

@app.put("/me/info")
async def update_user_info(
    request: UserInfoRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate encryption keys
    public_key, private_key = encryption_manager.generate_keypair()
    
    # Prepare and encrypt data
    user_data = request.dict(exclude_unset=True)
    encrypted_result = encryption_manager.encrypt_data(user_data, public_key)
    
    # Save encrypted data
    user_info = db.query(UserInformation).filter(UserInformation.user_id == user.id).first()
    if not user_info:
        user_info = UserInformation(user_id=user.id)
        db.add(user_info)
    
    user_info.encrypted_data = encrypted_result["encrypted_data"]
    user_info.public_key = public_key
    user_info.shared_secret_ciphertext = encrypted_result["shared_secret_ciphertext"]
    user_info.init_vector = encrypted_result["init_vector"]
    
    db.commit()
    
    return {
        "message": "User information encrypted and stored",
        "private_key": private_key
    }

@app.post("/me/info/decrypt")
async def get_user_info(
    decrypt_request: DecryptRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info = db.query(UserInformation).filter(UserInformation.user_id == user.id).first()
    if not user_info or not user_info.encrypted_data:
        return {"message": "No encrypted data found"}
    
    try:
        decrypted_data = encryption_manager.decrypt_data(
            user_info.encrypted_data,
            decrypt_request.private_key,
            user_info.shared_secret_ciphertext,
            user_info.init_vector
        )
        return decrypted_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/me/info/status")
async def check_user_info_status(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info = db.query(UserInformation).filter(UserInformation.user_id == user.id).first()
    
    return {
        "has_info": user_info is not None and user_info.encrypted_data is not None,
        "user_id": user.id,
        "email": user.email
    }
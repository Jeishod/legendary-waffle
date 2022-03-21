from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from api.schemas import CheckEmailResponse, LoginResponseSchema, UserRegisterSchema, UserSimpleSchema
from api.utils.security import authenticate, create_access_token, get_password_hash
from data.models import User


router = APIRouter()


@router.get("/check_email", response_model=CheckEmailResponse, status_code=status.HTTP_200_OK)
def check_email(
    email: EmailStr = Query(..., description="Email to check for available"),
):
    """
    Check if **email** is available for registering.
    """
    try:
        User.objects.get(email=email)
        is_available = False
    except User.DoesNotExist:
        is_available = True

    return CheckEmailResponse(email=email, is_available=is_available)


@router.post("/register", response_model=UserSimpleSchema, status_code=status.HTTP_201_CREATED)
def register(data: UserRegisterSchema):
    """
    Register a new user by self.
    """

    # check if email is used
    try:
        User.objects.get(email=data.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is already taken")
    except User.DoesNotExist:
        # create new user
        new_user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            hashed_password=get_password_hash(password=data.password),
        )
        new_user.save()
        return new_user


@router.post("/login", response_model=LoginResponseSchema, status_code=status.HTTP_200_OK)
def login(data: OAuth2PasswordRequestForm = Depends()):
    """
    Get auth token.
    """

    # authenticate user
    db_user = authenticate(email=EmailStr(data.username), password=data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # generate access token
    access_token = create_access_token(user_id=db_user.id)
    return LoginResponseSchema(access_token=access_token, token_type="bearer")

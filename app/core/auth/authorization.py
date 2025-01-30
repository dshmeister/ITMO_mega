import os
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Initializing HTTPBearer
http_bearer = HTTPBearer()

# Function for validating token
def validate_token(authorization: HTTPAuthorizationCredentials):
    if authorization.credentials != os.environ["BEARER_TOKEN"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return True


# Function for validating token (api_key)
def get_api_key(api_key: HTTPAuthorizationCredentials = Security(http_bearer)):
    return validate_token(api_key)
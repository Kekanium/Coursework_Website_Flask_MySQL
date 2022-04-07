UPDATE lab_schema.login
SET Login       = '$Login',
    PasswordL   = '$PasswordL',
    AccessLevel = $AccessLevel
WHERE idLogin = $idLogin
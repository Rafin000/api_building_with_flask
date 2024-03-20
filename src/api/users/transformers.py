def transform_user(user):
    return {
        "id": user.id,
        "fname": user.fname,
        "lname": user.lname,
        "username": user.username,
        "created_date": user.created_date,
        "updated_date": user.updated_date
    }
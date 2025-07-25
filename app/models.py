def user_to_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"]
    }
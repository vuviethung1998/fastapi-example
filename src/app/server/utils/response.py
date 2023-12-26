def ResponseModel(data, message, count=None):
    if count:
        return {
            "count": count,
            "data": data,
            "code": 200,
            "message": message,
        }
    else:
        return {
            "data": data,
            "code": 200,
            "message": message,
        }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

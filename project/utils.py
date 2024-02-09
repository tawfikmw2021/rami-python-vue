

import sqlalchemy 
def getUser(User, id):
    q = User.query.filter_by(id = id)
    if(q.count == 1):
        u = q.first()
        return u
    return {"name":"unknown"}
    
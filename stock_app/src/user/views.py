from database import get_db
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Request
from database import engine
from . import schema as schema_user, models as model_user
from . import hash
#import datetime
from datetime import datetime

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime


New_hasher = hash.Hasher()

model_user.Base.metadata.create_all(bind = engine)


router = APIRouter(
    prefix="/users",
    #tags = ['User'],
    responses= {404: {'description':'Not Found'}}
)

########################################################################### User Type #############################################################



@router.get("/user-type",  status_code=status.HTTP_200_OK, tags= ['User type'])
async def user_type(db:Session = Depends(get_db)):
    try:
        usertype_list = db.query(model_user.UserType.id, model_user.UserType.name).all()
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    return { 'status': status.HTTP_200_OK,'data':usertype_list}



@router.post("/add-user-type",status_code=status.HTTP_201_CREATED , tags= ['User type'])
async def add_user_type(request:Request, user_type_data:schema_user.user_type , db: Session = Depends(get_db)):
    result = user_type_data.dict()
    user_type_exist = db.query(model_user.UserType).filter(model_user.UserType.name == result['name']).first() 
    if user_type_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already Exist")
    else:
        try:
            
            new_user_type = model_user.UserType(**result)
            db.add(new_user_type)
            db.commit()
            db.refresh(new_user_type)
        except Exception as e:
            return {'error_message':e}
    return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}

# @router.delete("/user_type/{id}", tags= ['User type'])
# async def delete_user_type(id:int,db :Session=Depends(get_db)):
#     result = db.query(model_user.UserType).get(id)
#     if not result:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     db.delete(result)
#     db.commit()
#     return {"status":status.HTTP_200_OK,'message':"Successfully deleted"}



#################################################################  User #######################################################################

@router.post("/register", tags = ['User'])
async def add_user(request:Request, user:schema_user.User , db: Session = Depends(get_db)):
    result = user.dict()
    try:
        # print("error")
        pw = New_hasher.get_hash_password(result['password'])
        # print("Original Password: ",result['password'])
        # print("Hash Password: ",pw)
        result['password'] = str(pw)
        new_user_type = model_user.UserModel(**result)
        db.add(new_user_type)
        db.commit()
        db.refresh(new_user_type)
        return result
    except Exception as e:
        if 'violates foreign key constraint' in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_type_id does not exist in user type database")

        elif 'duplicate key value violates' in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Address Already Exists")
                #return {'error_message':"foreign key does not exist in user_type_data"}
        else:
            return {'error_message':str(e)}
        # print(e)
        #return {"status":e}


@router.delete("/delete-user/{id}", tags= ['User'])
async def delete_user(id:int,db :Session=Depends(get_db)):
    result = db.query(model_user.UserModel).get(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(result)
    db.commit()
    return {"status":status.HTTP_200_OK,'message':"Successfully deleted"}



@router.put('/update-user/{id}', status_code=status.HTTP_202_ACCEPTED, tags= ['User'])
def update(id, request:schema_user.User ,db:Session = Depends(get_db)):
    test= db.query(model_user.UserModel).filter(model_user.UserModel.id == id)
    if not test.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Test with id {id} is not found')
    try:
        test.update(request.dict())
        db.commit()
        return {"status":status.HTTP_200_OK,'message':"Successfully Updated"}
    except Exception as e:
        if 'violates foreign key constraint' in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_type_id does not exist in user type database")
                #return {'error_message':"foreign key does not exist in user_type_data"}
        else:
            return {'error_message':str(e)}


@router.post("/login", tags = ['User'])
async def login(request:Request, user_details:schema_user.UserLogin , db: Session = Depends(get_db)):
    result = user_details.dict()
    #print('this the original email: ',result['email'])
    test= db.query(model_user.UserModel).filter(model_user.UserModel.email == result['email']).first()
    
    #print("details of test: ", test.password)
    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Email not Exist')
    else:
        try:
            pw = New_hasher.verify_password(result['password'], test.password)
        except:
            pw = False
        if pw is True:
            #message = {'name':test.name,'email':test.email,'id':test.id}
            message = {"status": status.HTTP_200_OK, 'message':'successfully login','number': test.number, 'email':test.email, 'id':test.id}
            return message
        # result['password'] = str(pw)
        # new_user_type = model_user.UserModel(**result)
        # print(new_user_type)
        # pass
        else:
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail='Password is incorrect!')


@router.get("/",tags= ['User'])
async def read_root():
    return [{"id":1},{"id":2}]




#################################################################  Location Tracking #######################################################################

@router.post("/add-location", tags = ['Location Tracking'], status_code=status.HTTP_201_CREATED)
async def add_location(request:Request, user:schema_user.LocationTracker , db: Session = Depends(get_db)):
    result = user.dict()
    try:
        date = result['date_time']
        start_time = datetime.strptime('10:00:00', '%H:%M:%S').time()
        end_time = datetime.strptime('22:00:00', '%H:%M:%S').time()
        date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        user_time =date_time_obj.time()
        

        if user_time >= start_time and user_time <= end_time:
            new_location = model_user.LocationTracking(**result)
            db.add(new_location)
            db.commit()
            db.refresh(new_location)
            return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}
        else:
            return {"status":status.HTTP_404_NOT_FOUND,'message':"you can only add your data between 10 AM to 10 PM !"}
            #pass

            
    except Exception as e:
        if 'violates foreign key constraint' in str(e):
            return {"status":status.HTTP_404_NOT_FOUND,'message':"user_id does not exist in user database"}
            #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_id does not exist in user database")
        else:
            return {'error_message':str(e)}
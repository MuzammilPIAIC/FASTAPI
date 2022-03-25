from isort import file
from database import get_db
from fastapi import APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from database import engine
from . import schema as schema_user, models as model_user
import cloudinary
import cloudinary.uploader
from typing import List, Optional


model_user.Base.metadata.create_all(bind = engine)


router = APIRouter(
    prefix="/inventory",
    #tags = ['User'],
    responses= {404: {'description':'Not Found'}}
)



@router.get("/view_inventory",  status_code=status.HTTP_200_OK, tags= ['Inventory'])
async def view_inventory(db:Session = Depends(get_db)):
    try:
        usertype_list = db.query(model_user.testcall_2.id, model_user.testcall_2.name).all()
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    return { 'status': status.HTTP_200_OK,'data':usertype_list}



@router.post("/add-inventory",status_code=status.HTTP_201_CREATED , tags= ['Inventory'])
def add_inventory(request:Request, user_type_data:schema_user.Inventory , db: Session = Depends(get_db)):
    result = user_type_data.dict()
    #print("got data from input")
    user_type_exist = db.query(model_user.testcall_2).filter(model_user.testcall_2.email == result['email']).first() 
   # print("quert ran")
    if user_type_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already Exist")
    else:
        try:
            #print("in the try")
            new_user_type = model_user.testcall_2(**result)
            db.add(new_user_type)
            #print("data added into db")
            db.commit()
            db.refresh(new_user_type)
            #print("All set")
            return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}
        except Exception as e:
            #print("gone into exception")
            return {"status":status.HTTP_409_CONFLICT,'error_message':e}
    #return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}




##############################################################  AN Contacts ###########################################################

@router.post("/add-an-contact",status_code=status.HTTP_201_CREATED , tags= ['AN Contact'])
def add_an_contact(request:Request, user_data:schema_user.an_contact , db: Session = Depends(get_db)): #,file: UploadFile = File(...)
    result = user_data.dict()
    #print("got data from input")
    user_exist = db.query(model_user.ANContact).filter(model_user.ANContact.cnic_no == result['cnic_no']).first() 
   # print("quert ran")
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CNIC already Exist")
    else:
        try:
            
            # img = cloudinary.uploader.upload(file.file)
            # url = img.get('url')
            new_contact = model_user.ANContact(**result)
            db.add(new_contact)
            db.commit()
            db.refresh(new_contact)
            #print("image url is: ",url)
            return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}
        except Exception as e:
            if 'violates foreign key constraint' in str(e):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id or type_id is not exists in database")
            else:
                return {'error_message':str(e)}
            #print("gone into exception")
            #return {"status":status.HTTP_409_CONFLICT,'error_message':e}

# @router.post("/upload_image")
# async def upload(user_data:schema_user.an_contact, db: Session = Depends(get_db), file: UploadFile= File(...),  ):
#     result = user_data.dict()
#     return {'file_name': file.filename}



@router.post('/upload_image',status_code=status.HTTP_201_CREATED,tags= ['AN Contact'])
async def file_upload(
        request:Request,
        contact_id: str = Form(...),
        image_type_id: str = Form(...),
        #image_url: str = Form(...),
        my_file: UploadFile = File(...),
        #my_file: Optional[List[UploadFile]] = File(None),
        db: Session = Depends(get_db),
                
):  
    urls = []
    pb_id = []

    file_name = str(my_file.filename)
    # print('the file name is: ',file_name)
    # print(file_name.endswith(".jpg"))
    if file_name.endswith(".jpeg") is not True and file_name.endswith(".jpg") is not True and file_name.endswith(".png") is not True:
        return {"status":status.HTTP_409_CONFLICT,'error_message':"Please input a valid image"}
        
    try:
        
        #for i in my_file:
        img = cloudinary.uploader.upload(my_file.file, folder = "test")
        urls = img.get('url')
        #pb_id.append(img.get('public_id'))
        result = {"contact_id": contact_id, "image_type_id":image_type_id, 'image_url': urls}
        #result['image_url'] = str(url)
        new_image = model_user.Images(**result)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        #result = {"contact_id": contact_id, "image_type_id":image_type_id, 'image_url': url}
        return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}

    except Exception as e:
        if pb_id:
            for j in pb_id:
                cloudinary.uploader.destroy(j)
        return {"status":status.HTTP_409_CONFLICT,'error_message':e}


@router.get("/Show_contacts/{user_id}", tags = ['AN Contact'])
async def Show_contacts(user_id:int, request:Request,  db: Session = Depends(get_db)):
   
    user_check = db.query(model_user.UserModel).filter(model_user.UserModel.id == user_id).first()
    test1= db.query(model_user.ANContact).filter(model_user.ANContact.user_id == user_id).all()

    if not user_check:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Exist')
        return {"status": status.HTTP_404_NOT_FOUND, 'message':"User Not Exist"}

    if not test1:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Exist')
        return {"status": status.HTTP_404_NOT_FOUND, 'message':"This user does not have any contact yet!"}

    contacts_details = []
    for i in test1:
        dic = {"id": i.id, 'Full Name': i.full_name, "Company Name":i.company_name, "Address":i.address, "Cell No":i.cell_no_1}
        contacts_details.append(dic)
    
    
    if contacts_details:
        try:
            message = {"status": status.HTTP_200_OK, 'message':contacts_details}
            return message
        
        except Exception as e:
            return {"status": status.HTTP_409_CONFLICT, 'message':e}


@router.get("/contact_details/{contact_id}", tags = ['AN Contact'])
async def contact_details(contact_id:int, request:Request,  db: Session = Depends(get_db)):
   
    test2 = db.query(model_user.ANContact).filter(model_user.ANContact.id == contact_id).first()
    
            #print(i.image_type_id)
    #c_back= db.query(model_user.ANContact).filter(model_user.ANContact.user_id == user_id).all()

    # if not user_check:
    #     #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Exist')
    #     return {"status": status.HTTP_404_NOT_FOUND, 'message':"User Not Exist"}

    if not test2:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Exist')
        return {"status": status.HTTP_404_NOT_FOUND, 'message':"Contact not found"}

    #contacts_details = []
    #for i in test1:
    dic = {"id": test2.id, 'Full Name': test2.full_name, 
    "Company Name":test2.company_name, "Address":test2.address, 
    "Area":test2.area, "Cell No. 1":test2.cell_no_1, "Cell No. 2":test2.cell_no_2,
    "Phone":test2.phone, "Type":test2.type_id, "CNIC No.":test2.cnic_no,
    "CNIC Front Image": '', "CNIC Back Image": '', "Product Images": []
    }
    #contacts_details.append(dic)
    

    c_f = db.query(model_user.Images).filter(model_user.Images.contact_id == contact_id).all()
    for i in c_f:
        if i.image_type_id == 3:
            #print(i.image_url)
            dic['CNIC Front Image'] = i.image_url

        elif i.image_type_id == 4:
            #print(i.image_url)
            dic['CNIC Back Image'] = i.image_url
        
        elif i.image_type_id == 5:
            #print(i.image_url)
            img_dic = {"url":i.image_url}
            dic['Product Images'].append(img_dic)
    
    if dic:
        try:
            message = {"status": status.HTTP_200_OK, 'message':dic}
            return message
        
        except Exception as e:
            return {"status": status.HTTP_409_CONFLICT, 'message':e}



  


##############################################################  Image Type ###########################################################

@router.post("/add-image-type",status_code=status.HTTP_201_CREATED , tags= ['Image Type'])
def add_image_type(request:Request, user_data:schema_user.image_type , db: Session = Depends(get_db)):
    result = user_data.dict()
    #print("this is the result: ", result)
    
    try:
        #print("in the try")
        new_image_type = model_user.ImageType(**result)
        db.add(new_image_type)
        #print("data added into db")
        db.commit()
        db.refresh(new_image_type)
        #print("All set")
        return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}
    except Exception as e:
        #print("gone into exception")
        return {"status":status.HTTP_409_CONFLICT,'error_message':e}



##############################################################  Type ###########################################################

@router.post("/add-type",status_code=status.HTTP_201_CREATED , tags= ['AN Contact'])
def add_type(request:Request, user_data:schema_user.type , db: Session = Depends(get_db)):
    result = user_data.dict()

    
    try:
        #print("in the try")
        new_type = model_user.Type(**result)
        db.add(new_type)
        #print("data added into db")
        db.commit()
        db.refresh(new_type)
        #print("All set")
        return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}
    except Exception as e:
        #print("gone into exception")
        return {"status":status.HTTP_409_CONFLICT,'error_message':e}





##############################################################  Products ###########################################################

@router.post("/add-product",status_code=status.HTTP_201_CREATED , tags= ['Product'])
def add_product(request:Request, product_data:schema_user.product , db: Session = Depends(get_db)):
    result = product_data.dict()

    try:
        #print("in the try")
        new_product = model_user.Product(**result)
        db.add(new_product)
        #print("data added into db")
        db.commit()
        db.refresh(new_product)
        #print("All set")
        return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}
    except Exception as e:
        #print("gone into exception")
        return {"status":status.HTTP_409_CONFLICT,'error_message':e}


@router.post("/add-stock",status_code=status.HTTP_201_CREATED , tags= ['Product'])
def add_stock(request:Request, stock_data:schema_user.stock , db: Session = Depends(get_db)):
    result = stock_data.dict()

    try:
        #print("in the try")
        new_stock = model_user.Stock(**result)
        db.add(new_stock)
        #print("data added into db")
        db.commit()
        db.refresh(new_stock)
        #print("All set")
        return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}
    except Exception as e:
        #print("gone into exception")
        return {"status":status.HTTP_409_CONFLICT,'error_message':e}


@router.get("/show_product/", tags = ['Product'])
async def show_product( request:Request,  db: Session = Depends(get_db)):
   
    
    all_data= db.query(model_user.Product).all()
    all_qty = db.query(model_user.Stock).all()


    if not all_data:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Exist')
        return {"status": status.HTTP_404_NOT_FOUND, 'message':"Product Not Exist"}

    qtys = []
    for j in all_qty:
        qtys.append(j.qty)

    contacts_details = []
    for i,k in zip(all_data,qtys):
        dic = {"id": i.id, 'Name': i.name, "Description":i.description, "Quantity":k}
        contacts_details.append(dic)
    
    
    if contacts_details:
        try:
            message = {"status": status.HTTP_200_OK, 'data':contacts_details}
            return message
        
        except Exception as e:
            return {"status": status.HTTP_409_CONFLICT, 'message':e}



@router.put('/stock-update/', status_code=status.HTTP_202_ACCEPTED, tags= ['Product'])
def stock_update(request:schema_user.stock_update ,db:Session = Depends(get_db)):
    data = request.dict()
    check = db.query(model_user.Stock).filter(model_user.Stock.product_id == data['product_id'])

    if not check.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='This product_id is not exist')

    try:
        check.update(data)
        db.commit()
        return {"status":status.HTTP_200_OK,'message':"Successfully Updated"}
    except Exception as e:
        
        return {'error_message':str(e)}



# @router.post("/add-assign-inventory",status_code=status.HTTP_201_CREATED , tags= ['Product'])
# def add_assign_inventory(request:Request, ai_data:schema_user.assign_inventory , db: Session = Depends(get_db)):
#     result = ai_data.dict()

#     try:
#         #print("in the try")
#         new_ai = model_user.AssignInventory(**result)
#         db.add(new_ai)
#         #print("data added into db")
#         db.commit()
#         db.refresh(new_ai)
#         #print("All set")
#         return {"status":status.HTTP_201_CREATED,'message':"created", 'data':result}
#     except Exception as e:
#         #print("gone into exception")
#         return {"status":status.HTTP_409_CONFLICT,'error_message':e}


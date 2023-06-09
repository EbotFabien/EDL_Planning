'''   uploaded_file =request.files['photo']
    file_path = os.path.join( "/",uploaded_file.filename)
    uploaded_file.save(file_path)
    url=file_path
    fileName = url
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
       
    blob.make_public()
           
    data_['photo'] = blob.public_url '''  
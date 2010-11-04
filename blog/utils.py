def handle_uploaded_file(f,name):
    destination = open(name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


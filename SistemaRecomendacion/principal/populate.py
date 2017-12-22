from SistemaRecomendacion.principal.models import Usuario, Libro, Puntuacion
from datetime import datetime
from django.db import transaction

path = "datos"


def populateUsuarios():
    print("Loading occupations...")
    Usuario.objects.all().delete()
    
    fileobj=open(path+"\\u.occupation", "r")
    line=fileobj.readline()
    while line:
        occ = line.strip()
        if len(occ)>0:
            Usuario.objects.create(occupationName=occ)
        line=fileobj.readline()
    fileobj.close()
    transaction.commit()
    print("Occupations inserted: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")

    
def populateLibros():
    print("Loading Movie Genres...")
    Libro.objects.all().delete()
    
    fileobj=open(path+"\\u.genre", "r")
    line=fileobj.readline()
    while line:
        id_gen = line.split('|')
        if len(id_gen)>1:
            gen = id_gen[0].strip()
            ide = int(id_gen[1].strip())
            Libro.objects.create(id=ide,genreName=gen)
        line=fileobj.readline()
    fileobj.close()
    transaction.commit()
    print("Genres inserted: " + str(Libro.objects.count()))
    print("---------------------------------------------------------")


def populatePuntuaciones():
    print("Loading users...")
    Puntuacion.objects.all().delete()
    
    fileobj=open(path+"\\u.user", "r")
    line=fileobj.readline()
    while line:
        data = line.split('|')
        if len(data)>1:
            ide = int(data[0].strip())
            ag = int(data[1].strip())
            gen = data[2].strip()
            ocu = data[3].strip()
            zc = data[4].strip()
            Puntuacion.objects.create(id=ide, age=ag, gender=gen, occupation=Occupation.objects.get(occupationName=ocu), zipCode=zc)
        line=fileobj.readline()
    fileobj.close()
    transaction.commit()
    print("Users inserted: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")


def populateDatabase():
    populateUsuarios()
    populateLibros()
    populatePuntuaciones()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()
import os
import datetime
import pymongo
from dotenv import load_dotenv

# Load env vars
load_dotenv()

def fix_date_in_dict(d, key):
    """Helper to fix a date in a dictionary for a specific key."""
    if not isinstance(d, dict): return False
    val = d.get(key)
    if isinstance(val, (datetime.datetime, datetime.date)):
        if isinstance(val, datetime.datetime):
            d[key] = val.date().isoformat()
        else:
            d[key] = val.isoformat()
        return True
    return False

def fix_grupos():
    print("Fixing Grupos...")
    host = os.getenv('MONGO_DB_HOST', 'mongodb://localhost:27017')
    db_name = os.getenv('MONGO_DB_NAME', 'catequesis_db')
    
    print(f"Connecting to {host} / {db_name}")
    client = pymongo.MongoClient(host)
    db = client[db_name]
    
    try:
        print("Disabling validation for grupos...")
        db.command("collMod", "grupos", validationLevel="off")
    except Exception as e:
        print(f"Error disabling validation: {e}")

    collection = db['grupos']
    count = 0
    for doc in collection.find():
        updated = False
        
        # Fix Sesiones
        sesiones = doc.get('sesiones')
        if sesiones and isinstance(sesiones, list):
            new_sesiones = []
            modified_list = False
            for s in sesiones:
                if fix_date_in_dict(s, 'fecha'):
                     modified_list = True
                new_sesiones.append(s)
            
            if modified_list:
                doc['sesiones'] = new_sesiones
                updated = True
        
        if updated:
            try:
                collection.update_one({'_id': doc['_id']}, {'$set': {'sesiones': doc['sesiones']}})
                count += 1
            except Exception as e:
                print(f"Error updating Grupo {doc.get('_id')}: {e}")
                
    print(f"Fixed {count} Grupos")

def fix_inscripciones_extra():
    print("Fixing Inscripciones (Extra fields)...")
    host = os.getenv('MONGO_DB_HOST', 'mongodb://localhost:27017')
    db_name = os.getenv('MONGO_DB_NAME', 'catequesis_db')
    client = pymongo.MongoClient(host)
    db = client[db_name]
    collection = db['inscripciones']
    
    # We assume validation is already off or we try to disable again just in case
    try:
        db.command("collMod", "inscripciones", validationLevel="off")
    except: pass

    count = 0
    for doc in collection.find():
        updated = False
        updates = {}
        
        # 1. Certificado Final
        cert = doc.get('certificado_final')
        if cert and isinstance(cert, dict):
            if fix_date_in_dict(cert, 'fecha_emision'):
                updates['certificado_final'] = cert
                updated = True
        
        # 2. Registro Asistencia (usually no dates, but check if 'fecha' exists)
        asist = doc.get('registro_asistencia')
        if asist and isinstance(asist, list):
            new_asist = []
            modified_list = False
            for a in asist:
                # Check for 'fecha' key just in case user added it
                if fix_date_in_dict(a, 'fecha'):
                    modified_list = True
                new_asist.append(a)
            if modified_list:
                updates['registro_asistencia'] = new_asist
                updated = True
                
        if updated:
            try:
                collection.update_one({'_id': doc['_id']}, {'$set': updates})
                count += 1
            except Exception as e:
                print(f"Error updating Inscripcion {doc.get('_id')}: {e}")

    print(f"Fixed {count} Inscripciones (Extra)")

if __name__ == '__main__':
    fix_grupos()
    fix_inscripciones_extra()

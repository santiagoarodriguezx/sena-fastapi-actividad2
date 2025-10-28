from fastapi import FastAPI, Body  # Agregamos Body para el JSON
import uvicorn

# Crear la instancia de FastAPI
app = FastAPI()

# Lista simple de libros (simulada)
libros_db = [
    {"id": 1, "titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes"},
    {"id": 2, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez"},
    {"id": 3, "titulo": "El principito", "autor": "Antoine de Saint-Exupéry"}
]

# Variable para generar IDs únicos
contador_id = 4

# Rutas GET
@app.get("/")
def root():
    return {"mensaje": "¡Bienvenido a la Biblioteca API con FastAPI!"}

@app.get("/libros")
def obtener_libros():
    return {"libros": libros_db}

@app.get("/libros/{libro_id}")
def obtener_libro(libro_id: int):
    for libro in libros_db:
        if libro["id"] == libro_id:
            return {"libro": libro}
    return {"error": f"Libro con ID {libro_id} no encontrado"}

# Rutas POST 
@app.post("/libros")
def crear_libro(request: dict = Body(...)):  # Captura el JSON como dict
    global contador_id
    
    # Chequeo manual: verificar si faltan campos
    if "titulo" not in request or "autor" not in request:
        return {"error": "Faltan campos: titulo y autor son requeridos"}
    
    titulo = request["titulo"]
    autor = request["autor"]
    
    # Crear nuevo libro
    nuevo_libro = {
        "id": contador_id,
        "titulo": titulo,
        "autor": autor
    }
    
    libros_db.append(nuevo_libro)
    contador_id += 1
    
    return {"mensaje": "Libro creado exitosamente", "libro": nuevo_libro}

# Rutas PUT 
@app.put("/libros/{libro_id}")
def actualizar_libro(libro_id: int, request: dict = Body(...)):
    # Chequeo manual: verificar si faltan campos
    if "titulo" not in request or "autor" not in request:
        return {"error": "Faltan campos: titulo y autor son requeridos"}
    
    titulo = request["titulo"]
    autor = request["autor"]
    
    for i, libro in enumerate(libros_db):
        if libro["id"] == libro_id:
            libros_db[i] = {
                "id": libro_id,
                "titulo": titulo,
                "autor": autor
            }
            return {"mensaje": "Libro actualizado", "libro": libros_db[i]}
    
    return {"error": f"Libro con ID {libro_id} no encontrado"}

# Rutas DELETE
@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int):
    for i, libro in enumerate(libros_db):
        if libro["id"] == libro_id:
            libro_eliminado = libros_db.pop(i)
            return {"mensaje": "Libro eliminado", "libro": libro_eliminado}
    
    return {"error": f"Libro con ID {libro_id} no encontrado"}

# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

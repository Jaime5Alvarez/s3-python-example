import asyncio
import os
import json
import boto3
from botocore.exceptions import ClientError
from src.modules.storage.infraestructure.s3_service import S3Service
from src.modules.storage.application.use_cases import (
    GetTempUrlUseCase,
    GetItemUseCase,
    SetItemUseCase,
    RemoveItemUseCase
)


class S3UseCasesExample:
    """Ejemplo de uso de todos los casos de uso de S3 con LocalStack"""
    
    def __init__(self):
        # Configuración para LocalStack
        self.bucket_name = "test-bucket"
        self.endpoint_url = "http://localhost:4566"  # Puerto por defecto de LocalStack
        
        # Configurar el cliente de S3 para LocalStack
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        
        # Inicializar el servicio S3
        self.storage_service = S3Service(
            bucket_name=self.bucket_name,
            region_name='us-east-1'
        )
        
        # Configurar el servicio para usar LocalStack
        self._configure_localstack()
        
        # Inicializar casos de uso
        self.get_temp_url_use_case = GetTempUrlUseCase(self.storage_service)
        self.get_item_use_case = GetItemUseCase(self.storage_service)
        self.set_item_use_case = SetItemUseCase(self.storage_service)
        self.remove_item_use_case = RemoveItemUseCase(self.storage_service)
    
    def _configure_localstack(self):
        """Configurar el servicio S3 para usar LocalStack"""
        # Crear el bucket si no existe
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' ya existe")
        except ClientError:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' creado exitosamente")
    
    async def demonstrate_set_item(self):
        """Demostrar el caso de uso SetItem"""
        print("\n=== Demostrando SetItem Use Case ===")
        
        # Ejemplo 1: Almacenar un archivo de texto
        text_content = "¡Hola desde LocalStack S3!"
        text_key = "ejemplos/texto.txt"
        
        await self.set_item_use_case.execute(text_key, text_content.encode('utf-8'))
        print(f"✅ Archivo de texto almacenado: {text_key}")
        
        # Ejemplo 2: Almacenar datos JSON
        import json
        json_data = {
            "usuario": "test_user",
            "fecha": "2024-01-15",
            "activo": True,
            "puntuacion": 95.5
        }
        json_key = "ejemplos/datos.json"
        
        await self.set_item_use_case.execute(json_key, json.dumps(json_data).encode('utf-8'))
        print(f"✅ Datos JSON almacenados: {json_key}")
        
        # Ejemplo 3: Almacenar una imagen simulada (bytes)
        image_data = b"fake_image_data_12345"
        image_key = "ejemplos/imagen.jpg"
        
        await self.set_item_use_case.execute(image_key, image_data)
        print(f"✅ Imagen simulada almacenada: {image_key}")
    
    async def demonstrate_get_item(self):
        """Demostrar el caso de uso GetItem"""
        print("\n=== Demostrando GetItem Use Case ===")
        
        # Recuperar el archivo de texto
        text_key = "ejemplos/texto.txt"
        text_content = await self.get_item_use_case.execute(text_key)
        print(f"✅ Contenido del archivo de texto: {text_content.decode('utf-8')}")
        
        # Recuperar los datos JSON
        json_key = "ejemplos/datos.json"
        json_content = await self.get_item_use_case.execute(json_key)
        json_data = json.loads(json_content.decode('utf-8'))
        print(f"✅ Datos JSON recuperados: {json_data}")
        
        # Recuperar la imagen simulada
        image_key = "ejemplos/imagen.jpg"
        image_content = await self.get_item_use_case.execute(image_key)
        print(f"✅ Tamaño de la imagen: {len(image_content)} bytes")
    
    async def demonstrate_get_temp_url(self):
        """Demostrar el caso de uso GetTempUrl"""
        print("\n=== Demostrando GetTempUrl Use Case ===")
        
        # Generar URL temporal para el archivo de texto
        text_key = "ejemplos/texto.txt"
        temp_url = await self.get_temp_url_use_case.execute(text_key, expiration=300)  # 5 minutos
        print(f"✅ URL temporal para archivo de texto (5 min): {temp_url}")
        
        # Generar URL temporal para la imagen
        image_key = "ejemplos/imagen.jpg"
        temp_url_image = await self.get_temp_url_use_case.execute(image_key, expiration=1800)  # 30 minutos
        print(f"✅ URL temporal para imagen (30 min): {temp_url_image}")
        
        # Generar URL temporal para datos JSON
        json_key = "ejemplos/datos.json"
        temp_url_json = await self.get_temp_url_use_case.execute(json_key)
        print(f"✅ URL temporal para JSON (1 hora por defecto): {temp_url_json}")
    
    async def demonstrate_remove_item(self):
        """Demostrar el caso de uso RemoveItem"""
        print("\n=== Demostrando RemoveItem Use Case ===")
        
        # Crear un archivo temporal para eliminar
        temp_key = "ejemplos/archivo_temporal.txt"
        temp_content = "Este archivo será eliminado"
        await self.set_item_use_case.execute(temp_key, temp_content.encode('utf-8'))
        print(f"✅ Archivo temporal creado: {temp_key}")
        
        # Verificar que existe
        try:
            content = await self.get_item_use_case.execute(temp_key)
            print(f"✅ Archivo temporal existe: {content.decode('utf-8')}")
        except Exception as e:
            print(f"❌ Error al verificar archivo: {e}")
        
        # Eliminar el archivo
        await self.remove_item_use_case.execute(temp_key)
        print(f"✅ Archivo temporal eliminado: {temp_key}")
        
        # Verificar que ya no existe
        try:
            content = await self.get_item_use_case.execute(temp_key)
            print(f"❌ Error: El archivo aún existe: {content}")
        except Exception as e:
            print(f"✅ Confirmado: El archivo ya no existe (error esperado): {e}")
    
    async def demonstrate_error_handling(self):
        """Demostrar el manejo de errores"""
        print("\n=== Demostrando Manejo de Errores ===")
        
        # Intentar obtener un archivo que no existe
        non_existent_key = "archivo_que_no_existe.txt"
        try:
            content = await self.get_item_use_case.execute(non_existent_key)
            print(f"❌ Error: Se obtuvo contenido inesperado: {content}")
        except Exception as e:
            print(f"✅ Error manejado correctamente: {e}")
        
        # Intentar eliminar un archivo que no existe
        try:
            await self.remove_item_use_case.execute(non_existent_key)
            print(f"✅ Eliminación de archivo inexistente completada (no genera error)")
        except Exception as e:
            print(f"❌ Error inesperado al eliminar archivo inexistente: {e}")
    
    async def run_all_examples(self):
        """Ejecutar todos los ejemplos"""
        print("🚀 Iniciando demostración de casos de uso de S3 con LocalStack")
        print("=" * 60)
        
        try:
            await self.demonstrate_set_item()
            await self.demonstrate_get_item()
            await self.demonstrate_get_temp_url()
            await self.demonstrate_remove_item()
            await self.demonstrate_error_handling()
            
            print("\n" + "=" * 60)
            print("✅ Todos los casos de uso demostrados exitosamente")
            
        except Exception as e:
            print(f"\n❌ Error durante la demostración: {e}")
            print("Asegúrate de que LocalStack esté ejecutándose en http://localhost:4566")


async def main():
    """Función principal"""
    example = S3UseCasesExample()
    await example.run_all_examples()


if __name__ == "__main__":
    asyncio.run(main()) 
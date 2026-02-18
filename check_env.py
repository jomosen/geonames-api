#!/usr/bin/env python
"""
Script para verificar la configuración del entorno.
Verifica que todas las variables de entorno necesarias estén configuradas correctamente.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def check_env_var(var_name: str, required: bool = True) -> bool:
    """Verifica si una variable de entorno está configurada."""
    value = os.getenv(var_name)
    status = "✓" if value else "✗"
    required_str = "(requerida)" if required else "(opcional)"
    
    print(f"{status} {var_name}: {value or 'NO CONFIGURADA'} {required_str}")
    
    if required and not value:
        return False
    return True

def check_database_connection():
    """Verifica la conexión a la base de datos."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("✗ No se puede verificar la conexión (DATABASE_URL no configurada)")
        return False
    
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Conexión a la base de datos exitosa")
            return True
    except Exception as e:
        print(f"✗ Error de conexión a la base de datos: {e}")
        return False

def check_temp_directory():
    """Verifica que el directorio temporal existe."""
    temp_path = Path(os.getenv("TEMP_PATH", "./tmp"))
    if temp_path.exists():
        print(f"✓ Directorio temporal existe: {temp_path.absolute()}")
        return True
    else:
        print(f"✗ Directorio temporal NO existe: {temp_path.absolute()}")
        print(f"  Creando directorio...")
        temp_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Directorio temporal creado")
        return True

def main():
    print("=" * 60)
    print("Verificación de configuración del entorno - GeoNames API")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Verificar variables de entorno
    print("1. Variables de entorno:")
    print("-" * 60)
    all_ok &= check_env_var("DATABASE_URL", required=True)
    all_ok &= check_env_var("LOG_LEVEL", required=False)
    all_ok &= check_env_var("TEMP_PATH", required=False)
    print()
    
    # Verificar directorio temporal
    print("2. Directorio temporal:")
    print("-" * 60)
    all_ok &= check_temp_directory()
    print()
    
    # Verificar conexión a la base de datos
    print("3. Conexión a la base de datos:")
    print("-" * 60)
    all_ok &= check_database_connection()
    print()
    
    # Resultado final
    print("=" * 60)
    if all_ok:
        print("✓ Todas las verificaciones pasaron correctamente")
        print("✓ El entorno está configurado y listo para usar")
        return 0
    else:
        print("✗ Algunas verificaciones fallaron")
        print("✗ Por favor, revisa la configuración antes de continuar")
        return 1

if __name__ == "__main__":
    sys.exit(main())

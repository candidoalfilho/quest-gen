#!/usr/bin/env python3
"""
Script para configurar facilmente as variáveis de ambiente
"""

import os

def setup_environment():
    """
    Configura o arquivo .env com a chave da API do Gemini
    """
    env_file = ".env"
    
    print("🔧 Configuração do SimuladoAI API")
    print("=" * 40)
    
    # Verifica se já existe arquivo .env
    if os.path.exists(env_file):
        print(f"✅ Arquivo {env_file} já existe.")
        choice = input("Deseja sobrescrever? (s/N): ").lower().strip()
        if choice != 's':
            print("❌ Operação cancelada.")
            return
    
    print("\n📝 Para obter sua chave da API do Gemini:")
    print("1. Acesse: https://makersuite.google.com/app/apikey")
    print("2. Faça login com sua conta Google")
    print("3. Clique em 'Create API Key'")
    print("4. Copie a chave gerada")
    print()
    
    # Solicita a chave da API
    api_key = input("🔑 Cole sua chave da API do Gemini: ").strip()
    
    if not api_key or api_key == "sua_chave_gemini_aqui":
        print("❌ Chave inválida! Por favor, insira uma chave válida.")
        return
    
    # Cria o conteúdo do arquivo .env
    env_content = f"""# Configuração da API Gemini
GEMINI_API_KEY={api_key}

# Configuração do servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True
"""
    
    # Escreve o arquivo .env
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"✅ Arquivo {env_file} criado com sucesso!")
        print("\n🚀 Agora você pode executar a API:")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo {env_file}: {e}")

if __name__ == "__main__":
    setup_environment()

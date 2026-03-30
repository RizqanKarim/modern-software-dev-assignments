from mcp.server.fastmcp import FastMCP
import requests

# 1. Inisialisasi Server MCP
mcp = FastMCP("RickAndMorty")

# 2. Tool Pertama: Mencari Karakter
@mcp.tool()
def search_character(name: str) -> str:
    """Mencari data karakter Rick and Morty berdasarkan nama."""
    url = f"https://rickandmortyapi.com/api/character/?name={name}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Karakter dengan nama '{name}' tidak ditemukan."
    
    data = response.json()
    # Ambil hasil pertama saja agar simpel
    char = data["results"][0]
    return (f"Nama: {char['name']}\n"
            f"Status: {char['status']}\n"
            f"Spesies: {char['species']}\n"
            f"Asal: {char['origin']['name']}")

# 3. Tool Kedua: Mencari Lokasi
@mcp.tool()
def get_location_info(location_id: int) -> str:
    """Mendapatkan informasi lokasi/planet berdasarkan ID (1-126)."""
    url = f"https://rickandmortyapi.com/api/location/{location_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Lokasi tidak ditemukan. Coba ID antara 1 sampai 126."
    
    data = response.json()
    return (f"Lokasi: {data['name']}\n"
            f"Tipe: {data['type']}\n"
            f"Dimensi: {data['dimension']}")

if __name__ == "__main__":
    mcp.run()
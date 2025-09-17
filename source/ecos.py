import os
import pandas as pd

def build_eco_dict(eco_folder_path, output_path):
    """
    Carga los archivos .tsv de lichess chess-openings,
    construye un dict ECO_CODE -> Opening Name (name),
    y lo guarda como CSV en output_path.
    """
    eco_dict = {}

    for fname in os.listdir(eco_folder_path):
        if fname.endswith(".tsv"):
            path = os.path.join(eco_folder_path, fname)
            df = pd.read_csv(path, sep="\t", usecols=["eco", "name"])
            for _, row in df.iterrows():
                code = row["eco"]
                name = row["name"]
                if pd.notna(code) and pd.notna(name):
                    if code not in eco_dict:
                        eco_dict[code] = name

    # Guardar como DataFrame
    eco_df = pd.DataFrame(list(eco_dict.items()), columns=["eco", "name"])
    eco_df.to_csv(output_path, index=False)
    print(f"ECO dict guardado en {output_path} con {len(eco_df)} aperturas.")

    return eco_df


if __name__ == "__main__":
    # Ajusta las rutas según dónde corras el script
    eco_folder = "./data/ECOS"
    output_path = "./data/eco_dict.csv"

    build_eco_dict(eco_folder, output_path)
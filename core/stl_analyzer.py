import trimesh
import io

DENSITY = {
    "PLA": 1.24,
    "PETG": 1.27,
    "ABS": 1.04,
    "TPU": 1.21
}

def analyze_stl(
    file_bytes: bytes,
    material: str,
    infill_pct: int,
    speed_mm_s: int,
    nozzle_mm: float,
    layer_height: float = 0.2
):
    mesh = trimesh.load(io.BytesIO(file_bytes), file_type="stl", force="mesh")
    if mesh.is_empty:
        raise ValueError("Empty or invalid STL")

    volume_cm3 = mesh.volume / 1000
    effective_volume = volume_cm3 * (infill_pct / 100)

    weight_g = effective_volume * DENSITY[material]

    extrusion_rate = speed_mm_s * nozzle_mm * layer_height
    total_mm3 = effective_volume * 1000
    time_hr = round((total_mm3 / extrusion_rate) / 3600, 2)

    return {
        "Volume (cm³)": round(volume_cm3, 2),
        "Effective Volume (cm³)": round(effective_volume, 2),
        "Weight (g)": round(weight_g, 2),
        "Estimated Print Time (hr)": time_hr
    }

import io
import trimesh
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def slicer_volume_adjustment(mesh_volume_cm3, infill_percent=20, wall_percent=25):
    wall_fraction = wall_percent / 100
    infill_fraction = infill_percent / 100
    effective_volume = (mesh_volume_cm3 * wall_fraction) + (mesh_volume_cm3 * (1 - wall_fraction) * infill_fraction)
    return effective_volume

def estimate_print_time(effective_volume_cm3, layer_height=0.2, printer_speed_mm_s=60, nozzle_mm=0.4):
    extrusion_rate = printer_speed_mm_s * layer_height * nozzle_mm
    total_mm3 = effective_volume_cm3 * 1000
    if extrusion_rate == 0: return 0
    return round((total_mm3 / extrusion_rate) / 3600, 2)

def analyze_single_file_content(file_content, file_name, density, cost_per_kg, infill, walls, speed_mm_s, nozzle_mm):
    try:
        # Load directly from bytes (memory)
        file_obj = io.BytesIO(file_content)
        mesh = trimesh.load(file_obj, file_type='stl', force="mesh")
        
        if mesh.is_empty: raise ValueError("Empty mesh")
        
        volume_cm3 = mesh.volume / 1000.0
        effective_vol = slicer_volume_adjustment(volume_cm3, infill, walls)
        weight_g = effective_vol * density
        cost = (weight_g / 1000) * cost_per_kg
        time_hr = estimate_print_time(effective_vol, 0.2, speed_mm_s, nozzle_mm)
        
        return {
            "File Name": file_name,
            "Effective Volume (cm3)": round(effective_vol, 2),
            "Weight (g)": round(weight_g, 2),
            "Cost (₹)": round(cost, 2),
            "Print Time (hr)": time_hr
        }
    except Exception as e:
        return {"error": str(e), "File Name": file_name}

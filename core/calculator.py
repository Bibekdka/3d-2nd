def calculate_cost(
    filament_kg_price,
    filament_used_g,
    electricity_per_hr,
    print_time_hr,
    labour,
    delivery,
    machine_wear_per_hr,
    profit_pct,
    gst_pct
):
    filament_cost = (filament_used_g / 1000) * filament_kg_price
    electricity_cost = electricity_per_hr * print_time_hr
    machine_wear = machine_wear_per_hr * print_time_hr

    base = filament_cost + electricity_cost + labour + delivery + machine_wear
    profit = base * (profit_pct / 100)
    subtotal = base + profit
    gst = subtotal * (gst_pct / 100)
    final = subtotal + gst

    return {
        "Filament Cost": round(filament_cost, 2),
        "Electricity Cost": round(electricity_cost, 2),
        "Machine Wear": round(machine_wear, 2),
        "Base Cost": round(base, 2),
        "Profit": round(profit, 2),
        "GST": round(gst, 2),
        "Final Price": round(final, 2)
    }

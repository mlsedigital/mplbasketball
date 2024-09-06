nba_court_parameters = {
    "court_dims": [94.0, 50.0],
    # Hoop area
    "hoop_distance_from_edge": 5.25,
    "hoop_diameter": 0.75,
    "backboard_distance_from_edge": 4.0,
    "backboard_width": 6.0,
    "charge_circle_radius": 4.0,
    "charge_circle_side_length": 3.0,
    # Inbound lines
    "inbound_line_distance_from_edge": 28.0,
    "inbound_line_length": 3.0,
    "outbound_line_distance_from_center": 4.0 + 1 / 12.0,
    "outbound_line_length": 4.0,
    # Outer paint
    "outer_paint_dims": [18.0 + 5 / 6, 16 - 1 / 3],
    # Inner paint
    "inner_paint_dims": [18.0 + 5 / 6, 12 - 1 / 3],
    # Center circle
    "outer_circle_diameter": 6.0,
    "inner_circle_diameter": 2.0,
    # Three point area
    "three_point_arc_angle": 68.13,
    "three_point_arc_diameter": 47.5,
    "three_point_line_length": 14.0,
    "three_point_side_width": 3.0,
    # Hoop height
    "hoop_height": 10.0,
}

wnba_court_parameters = {
    "court_dims": [94.0, 50.0],
    # Hoop area
    "hoop_distance_from_edge": 5.25,
    "hoop_diameter": 0.75,
    "backboard_distance_from_edge": 4.0,
    "backboard_width": 6.0,
    "charge_circle_radius": 4.0,
    "charge_circle_side_length": 3.0,
    # Inbound lines
    "inbound_line_distance_from_edge": 28.0,
    "inbound_line_length": 3.0,
    "outbound_line_distance_from_center": 4.0 + 1 / 12.0,
    "outbound_line_length": 4.0,
    # Outer paint
    "outer_paint_dims": [18.0 + 5 / 6, 16 - 1 / 3],
    # Inner paint
    "inner_paint_dims": [18.0 + 5 / 6, 12 - 1 / 3],
    # Center circle
    "outer_circle_diameter": 6.0,
    "inner_circle_diameter": 2.0,
    # Three point area
    "three_point_arc_angle": 83.51692630710276,
    "three_point_arc_diameter": 44.365,
    "three_point_line_length": 7.75,
    "three_point_side_width": 3.0,
    # Hoop height
    "hoop_height": 10.0,
}

ncaa_court_parameters = {
    "court_dims": [94.0, 50.0],
    # Hoop area
    "hoop_distance_from_edge": 5.25,
    "hoop_diameter": 0.75,
    "backboard_distance_from_edge": 4.0,
    "backboard_width": 6.0,
    "charge_circle_radius": 4.0,
    "charge_circle_side_length": 3.0,
    # Inbound lines
    "inbound_line_distance_from_edge": 28.0,
    "inbound_line_length": 3.0,
    "outbound_line_distance_from_center": 4.0 + 1 / 12.0,
    "outbound_line_length": 4.0,
    # Outer paint
    "outer_paint_dims": [18.0 + 5 / 6, 12 - 1 / 3],
    # Inner paint
    "inner_paint_dims": [18.0 + 5 / 6, 12 - 1 / 3],
    # Center circle
    "outer_circle_diameter": 6.0,
    "inner_circle_diameter": 6.0,
    # Three point area
    "three_point_arc_angle": 78.95,
    "three_point_arc_diameter": 44.218,
    "three_point_line_length": 9.4,
    "three_point_side_width": 3.34375,
    # Hoop height
    "hoop_height": 10.0,
}


def _get_court_params_in_desired_units(court_type, desired_units):
    """
    Function to convert court parameters to units of choice.
    """
    assert court_type in ["nba", "wnba", "ncaa"], "Invalid court type"
    assert desired_units in ["m", "ft"], "Invalid units, Currently only 'm' and 'ft' are supported"

    if desired_units == "m":
        conversion_factor = 0.3048
    else:
        conversion_factor = 1.0

    if court_type == "nba":
        court_params = nba_court_parameters
    elif court_type == "wnba":
        court_params = wnba_court_parameters
    elif court_type == "ncaa":
        court_params = ncaa_court_parameters

    new_court_params = {}

    for key, value in court_params.items():
        if "angle" not in key.split("_"):
            if isinstance(value, list):
                new_court_params[key] = [val * conversion_factor for val in value]
            else:
                new_court_params[key] = value * conversion_factor
        else:
            new_court_params[key] = value

    return new_court_params

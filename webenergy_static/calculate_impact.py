def calculate_impact(device_type='laptop', content_type='text', connectivity_method='3G', duration=120):
    """
    Calculate the environmental impact of using digital media services based on the device type, content type, connectivity method, and duration.

    Parameters:
    device_type (str): The type of device used to access the media service. Options are 'phone', 'tablet', 'pc', 'laptop'. Default is 'laptop'.
    content_type (str): The type of content being accessed. Options are 'text' and 'video'. Default is 'text'.
    connectivity_method (str): The method of internet connectivity. Options are '3G', '5G', and 'WiFi'. Default is '3G'.
    duration (int): Duration of the media service usage in minutes. Default is 120.

    Returns:
    tuple: A tuple containing the total energy consumption in watt-hours (Wh), carbon emissions in grams, 
    equivalent driving meters in a petrol car, and the duration equivalent of powering 11W light bulbs.

    The function calculates the total energy consumption (in joules) based on the device's power consumption, 
    the data volume based on content type, the energy consumption of the servers and network based on the number of page loads, 
    and the energy consumption of the access network based on the connectivity method. 
    It then converts the total energy consumption to watt-hours, calculates the carbon emissions based on a coefficient, 
    and determines the equivalent distance driven by a petrol car and the equivalent duration of powering 11W light bulbs.
    """
    # Constants and coefficients
    device_power = {'phone': 1, 'tablet': 3, 'pc': 115, 'laptop': 32}
    data_volume_text = 8000000  # in bytes
    data_volume_video = 1100000  # in bytes per second
    e_origin_per_request = 306
    e_network_coeff = 0.000045
    wifi_energy_per_sec = 10
    e_acc_net_3G = 4.55e-05
    # https://www.globenewswire.com/news-release/2020/12/02/2138047/0/en/Nokia-confirms-5G-as-90-percent-more-energy-efficient.html
    e_acc_net_5G = wifi_energy_per_sec * 0.1  # 90% more efficient than WiFi;
    carbon_coeff = 0.525
    power_lightBulb = 11
    carEmissions = 0.20864

    # Calculate based on selections
    duration_secs = duration * 60
    p_device = device_power.get(device_type, 32)
    page_loads = 1 if content_type == 'video' else duration

    if content_type == 'video':
        data_volume = duration_secs * data_volume_video
        p_device *= 1.15
    else:
        data_volume = data_volume_text

    e_serv = (e_origin_per_request + 6.9e-6 * data_volume) * page_loads
    e_network = e_network_coeff * data_volume * page_loads

    if connectivity_method == '3G':
        e_acc_net = e_acc_net_3G * data_volume * page_loads
    elif connectivity_method == '5G':
        e_acc_net = e_acc_net_5G * duration_secs
    else:
        # Defaulting to WiFi
        e_acc_net = wifi_energy_per_sec * duration_secs

    e_user = p_device * duration_secs
    e_total_joule = e_serv + e_network + e_acc_net + e_user

    # Convert to watt-hours and calculate emissions
    e_total_wh = e_total_joule / 3600
    carbon = carbon_coeff * e_total_wh
    driving_meters_petrol_car = (carbon / carEmissions) * 1000
    light_bulbs_duration = e_total_joule / (power_lightBulb * duration_secs)

    return e_total_wh, carbon, driving_meters_petrol_car, light_bulbs_duration

# Example usage
print(calculate_impact('phone', 'video', '5G', 30, 'video'))


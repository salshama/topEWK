import os

def create_datacard(energy_type, variation, signal_processes, background_processes, output_dir, signal_base_path, background_base_path):
    """
    Creates a single data card for a specific energy type and variation.
    """
    # Construct paths for signal and background processes
    signal_paths = [
        f"{signal_base_path}/deviation_histogram_{energy_type}_{proc}_{variation}_TestSel.root"
        for proc in signal_processes
    ]
    background_paths = [
        f"{background_base_path}/{energy_type}_{proc.replace('SM', '')}_SM_TestSel.root"
        for proc in background_processes
    ]
    
    # Data card lines
    lines = [
        "imax    1 number of bins",
        "jmax    * number of processes minus 1",
        "kmax    * number of nuisance parameters",
        "--------------------------------------------------------------------------------",
    ]
    
    # Add shapes for signal processes
    for proc, path in zip(signal_processes, signal_paths):
        lines.append(f"shapes  {proc}    DH  {path}  deviation_hist_{energy_type}_{proc}_{variation}_TestSel")
    
    # Add shapes for background processes
    for proc, path in zip(background_processes, background_paths):
        lines.append(f"shapes  {proc}  DH  {path}  {energy_type}")
    
    # Add shapes for data_obs (assumes it's the same as one of the SM processes)
    lines.append(f"shapes  data_obs   DH  {background_paths[0]}  {energy_type}")
    
    lines.append("--------------------------------------------------------------------------------")
    lines.append("bin".ljust(15) + "DH")
    lines.append("observation".ljust(15) + "-1")
    lines.append("--------------------------------------------------------------------------------")
    
    # Add bin, process, and rate with consistent spacing
    all_processes = signal_processes + background_processes
    column_width = 15  # Consistent column width

    bins_line = "bin".ljust(column_width) + " ".join(["DH".ljust(column_width) for _ in all_processes])
    process_names_line = "process".ljust(column_width) + " ".join([proc.ljust(column_width) for proc in all_processes])
    process_ids_line = "process".ljust(column_width) + " ".join(
        [f"-{i+1}".ljust(column_width) for i in range(len(signal_processes))] +
        [f"{i+1}".ljust(column_width) for i in range(len(background_processes))]
    )
    rates_line = "rate".ljust(column_width) + " ".join(["-1".ljust(column_width) for _ in all_processes])
    
    lines.extend([bins_line, process_names_line, process_ids_line, rates_line])
    lines.append("--------------------------------------------------------------------------------")
    lines.append("free rateParam DH * 1.0")
    lines.append("* autoMCStats 1 1")

    # Write to file
    output_path = os.path.join(output_dir, f"datacard_{energy_type}_{variation}.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Data card written to {output_path}")

def generate_datacards(energy_types, variations, signal_processes, background_processes, output_dir, signal_base_path, background_base_path):
    """
    Generates data cards for all specified energy types and variations.
    
    Args:
    - energy_types (list): List of energy types (e.g., ["muon_pass_energy", "electron_pass_energy", "Emiss_energy"]).
    - variations (list): List of BSM variations (e.g., ["ta_ttAdown", "ta_ttAup"]).
    - signal_processes (list): List of signal processes.
    - background_processes (list): List of background processes.
    - output_dir (str): Directory to save the data cards.
    - signal_base_path (str): Base path for the signal root histogram files.
    - background_base_path (str): Base path for the background root histogram files.
    """
    for energy_type in energy_types:
        for variation in variations:
            create_datacard(energy_type, variation, signal_processes, background_processes, output_dir, signal_base_path, background_base_path)

if __name__ == "__main__":
    # Define inputs
    energy_types = ["muon_pass_energy", "electron_pass_energy", "Emiss_energy"]
    variations = ["ta_ttAdown", "ta_ttAup", "tv_ttAdown", "tv_ttAup", "vr_ttZup", "vr_ttZdown"]
    signal_processes = ["semilep", "fulllep", "fullhad"]
    background_processes = ["semilepSM", "fulllepSM", "fullhadSM"]
    output_dir = "./datacards"
    signal_base_path = "/ceph/salshamaily/topEWK_FCCee/root_hists/bsm_sm_dev_samples"
    background_base_path = "/ceph/salshamaily/topEWK_FCCee/root_hists/bsm_sm_samples"
    
    # generating datacards for all variables
    generate_datacards(energy_types, variations, signal_processes, background_processes, output_dir, signal_base_path, background_base_path)
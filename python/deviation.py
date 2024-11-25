# Importing required packages
import uproot
import numpy as np
import glob
import copy
import ROOT
import os

# Glob all .root BSM/SM hist files
root_files = glob.glob('/ceph/salshamaily/topEWK_FCCee/root_hists/bsm_sm_samples/*.root')

# Setting output directory for deviation histograms
output_directory = "/ceph/salshamaily/topEWK_FCCee/root_hists/bsm_sm_dev_samples"

# Saving deviation histogram plots
dev_plots_dir = "/ceph/salshamaily/topEWK_FCCee/plots"

# Extract variable from filename
def extract_variable(root_file):
    base_name = os.path.basename(root_file)
    if "Emiss_energy" in base_name:
        return "Emiss_energy"
    elif "muon_pass_energy" in base_name:
        return "muon_pass_energy"
    elif "electron_pass_energy" in base_name:
        return "electron_pass_energy"
    else:
        return ""

# Extract process type from filename
def extract_process(root_file):
    base_name = os.path.basename(root_file)
    if "semilep" in base_name:
        return "semilep"
    elif "fulllep" in base_name:
        return "fulllep"
    else:
        return "fullhad"
        
        # function to extract the variation (e.g., 'ttAdown') from the file name
def extract_variation(file_name):

    """
    Extracts the BSM variation from the file name.
    Parameters:
    - file_name: str, name of the .root file.
    Returns:
    - variation: str, extracted variation from the file name.
    If no variation is present, returns 'SM' for Standard Model.
    """
    
    base_name = os.path.basename(file_name)

    if "ta_ttAdown" in base_name:
        return "ta_ttAdown"
        
    if "ta_ttAup" in base_name:
        return "ta_ttAup"
        
    if "tv_ttAup" in base_name:
        return "tv_ttAup"
    
    if "tv_ttAdown" in base_name:
        return "tv_ttAdown"
    
    if "vr_ttZup" in base_name:
        return "vr_ttZup"
        
    if "vr_ttZdown" in base_name:
        return "vr_ttZdown"
        
    else:
        return 'SM'

# extract selection type from histogram or file name
def extract_selection(file_name):

    """
    Extracts the selection type ('NoSel' or 'TestSel') from the file name.
    Parameters:
    - file_name: str, name of the file.
    Returns:
    - selection: str, either 'NoSel' or 'TestSel'.
    """
    
    base_name = os.path.basename(file_name)

    if "NoSel" in base_name:
        return "NoSel"
        
    elif "TestSel" in base_name:
        return "TestSel"
        
    else:
        print(f"Warning: No selection found for {base_name}")
        return ""

def process_histograms():
    hist_sm_dict = {}

    # Loop through ROOT files to save SM histograms
    for root_file in root_files:
        variable = extract_variable(root_file)
        process = extract_process(root_file)
        variation = extract_variation(root_file)
        selection = extract_selection(root_file)

        # Only process SM files
        if variable in ['Emiss_energy', 'muon_pass_energy', 'electron_pass_energy'] and variation == "SM":
            file = ROOT.TFile.Open(root_file)
            hist_name = f"{variable}"
            hist_sm = file.Get(hist_name)

            # Verify histogram and type
            if not hist_sm or not isinstance(hist_sm, ROOT.TH1):
                print(f"Error: Histogram '{hist_name}' not found")
                file.Close()
                continue

            # Make a deep copy and store in dictionary
            hist_sm_copy = copy.deepcopy(hist_sm)
            hist_sm_copy.SetDirectory(0)

            # Save to dictionary by selection, process, and variable
            if selection not in hist_sm_dict:
                hist_sm_dict[selection] = {}
            if process not in hist_sm_dict[selection]:
                hist_sm_dict[selection][process] = {}
            hist_sm_dict[selection][process][variable] = hist_sm_copy

            file.Close()
            print(f"Processed SM histogram for {variable}, selection: {selection}, process: {process}")

    # Loop again for BSM files to calculate deviation
    for root_file in root_files:
        variable = extract_variable(root_file)
        process = extract_process(root_file)
        variation = extract_variation(root_file)
        selection = extract_selection(root_file)

        # Only process BSM files (skip SM and irrelevant variables)
        if variation == "SM" or variable not in ['Emiss_energy', 'muon_pass_energy', 'electron_pass_energy']:
            continue

        # Check if corresponding SM histogram exists and matches the variable
        if (
            selection not in hist_sm_dict or
            process not in hist_sm_dict[selection] or
            variable not in hist_sm_dict[selection][process]
        ):
            print(f"Warning: No corresponding SM histogram for variable '{variable}', selection: {selection}, process: {process}")
            continue

        hist_sm = hist_sm_dict[selection][process][variable]

        print('\nMoving on to BSM histograms...\n')

        # Open BSM file and get histogram
        file = ROOT.TFile.Open(root_file)
        hist_name = f"{variable}"
        hist_bsm = file.Get(hist_name)

        if not hist_bsm or not isinstance(hist_bsm, ROOT.TH1):
            print(f"Error: Histogram '{hist_name}' not found or is not a histogram in {root_file}")
            file.Close()
            continue

        # Calculate deviation histogram (BSM - SM)
        hist_deviation = hist_bsm.Clone(f"deviation_hist_{variable}_{process}_{variation}_{selection}")
        hist_deviation.Add(hist_sm, -1)  # BSM - SM

        # Save deviation histogram
        output_file_name = os.path.join(output_directory, f"deviation_histogram_{variable}_{process}_{variation}_{selection}.root")
        output_file = ROOT.TFile.Open(output_file_name, "RECREATE")
        hist_deviation.Write()
        output_file.Close()

        print(f"Saved deviation histogram: {output_file_name}")

        file.Close()

# plotting deviation histograms
def plot_dev_hists():
    dev_files = glob.glob(os.path.join(output_directory, "*.root"))
    
    ROOT.gROOT.SetBatch(True)
    
    for dev_file in dev_files:
        file = ROOT.TFile.Open(dev_file)
        if not file or file.IsZombie():
            print(f"Error: Could not open deviation file {dev_file}")
            continue

        # get histogram name
        hist_list = file.GetListOfKeys()
        hist_name = hist_list.At(0).GetName()
        hist_dev = file.Get(hist_name)

        c1 = ROOT.TCanvas("c1", "", 800, 600)
        
        # drawing histogram
        hist_dev.SetStats(0)
        hist_dev.SetLineColor(ROOT.kBlue)
        hist_dev.SetLineWidth(2) 
        hist_dev.SetTitle(f"Deviation Histogram: {hist_name}")
        hist_dev.GetXaxis().SetTitle("Energy [GeV]")
        hist_dev.GetYaxis().SetTitle("$\Delta$(BSM - SM)")
        #c1.SetLogy(True)
        hist_dev.Draw("h")
        
        # saving plots
        plot_name = os.path.splitext(os.path.basename(dev_file))[0]  # Base name without extension
        c1.SaveAs(os.path.join(dev_plots_dir, f"{plot_name}.png"))

        print(f"Saved plot for {hist_name}")

        # closing file and canvas
        file.Close()
        c1.Close()

# Run the process
process_histograms()

# Run the plot function
plot_dev_hists()
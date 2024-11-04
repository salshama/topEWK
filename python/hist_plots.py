# importing required packages
import uproot
import matplotlib.pyplot as plt
import numpy as np
import glob
import ROOT
import os

# glob all .root hist files
root_files = glob.glob('/ceph/salshamaily/topEWK_FCCee/analysis/final_output/*.root')

# output directory where ROOT histograms will be saved
output_dir = "/ceph/salshamaily/topEWK_FCCee/root_hists/bsm_sm_samples"

# saving histogram as ROOT file
def save_histogram_as_root(histogram_name, bin_edges, hist_values, output_dir, classification, variation, selection):

    """
    Save a histogram as a ROOT histogram.

    Parameters:
    - histogram_name: str, name of the histogram.
    - bin_edges: numpy array, array of bin edges from the histogram.
    - hist_values: numpy array, array of histogram values.
    - output_dir: str, directory where the ROOT file will be saved.
    - classification: str, the process to be plotted (to include in the file name).
    - variation: str, the BSM variation being plotted (to include in the file name).
    - selection: str, either 'nosel' or 'testsel' (to include in the file name).
    """
    
    # make sure directory exists to begin with
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # creating ROOT histogram object
    num_bins = len(bin_edges) - 1
    root_hist = ROOT.TH1F(histogram_name, histogram_name, num_bins, bin_edges)

    # filling histogram with values
    for i in range(num_bins):
        root_hist.SetBinContent(i + 1, hist_values[i])

    # output ROOT file path
    output_file = os.path.join(output_dir, f"{histogram_name}_{classification}_{variation}_{selection}.root")

    # Open a ROOT file to write the histogram
    root_file = ROOT.TFile(output_file, "RECREATE")  # "RECREATE" to overwrite an existing file
    root_hist.Write()
    root_file.Close()

    print(f"Histogram {histogram_name} saved to {output_file}\n")

# determine xlabel based on histogram name
def determine_xlabel(histogram_name):

    """
    Determines the appropriate x-axis label based on keywords in the histogram name.
    Parameters:
    - histogram_name: str, name of the histogram.
    Returns:
    - xlabel: str, the x-axis label.
    """
    
    keyword_to_label = {
        "energy": "Energy [GeV]",
        "pt": "p$_T$ [GeV]",
        "mass": "Mass [GeV]",
        "eta": "$\eta$",
        "phi": "$\phi$"
    }
    
    xlabel = "Value"
    
    for keyword, label in keyword_to_label.items():
        if keyword in histogram_name.lower():
            xlabel = label
            break
            
    return xlabel

# classify the file based on the filename
def classify_file(file_name):

    """
    Classifies the file as either semi-leptonic, fully hadronic, or fully leptonic based on the filename.
    Parameters:
    - file_name: str, name of the .root file.
    Returns:
    - classification: str, any of the above processes.
    """
    
    if "thadThad" in file_name:
        return 'fullhad'
        
    elif "tlepThad" in file_name or "thadTlep" in file_name:
        return 'semilep'
        
    elif "tlepTlep" in file_name:
        return 'fulllep'
        
    else:
        return 'unknown'

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
    
    if "vr_ttAup" in base_name:
        return "vr_ttAup"
        
    if "vr_ttAdown" in base_name:
        return "vr_ttAdown"
        
    if "ta_ttZdown" in base_name:
        return "ta_ttZdown"
        
    if "ta_ttZup" in base_name:
        return "ta_ttZup"
        
    if "tv_ttZup" in base_name:
        return "tv_ttZup"
    
    if "tv_ttZdown" in base_name:
        return "tv_ttZdown"
    
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

# reading histograms from .root files
def read_histogram_data(root_file, histogram_name):
    
    """
    Reads a histogram from a .root file and returns the bin edges and values.
    Parameters:
    - root_file: str, path to the .root file.
    - histogram_name: str, name of the histogram to be extracted.
    Returns:
    - bin_edges: numpy array of bin edges.
    - hist_values: numpy array of histogram values.
    """
    
    with uproot.open(root_file) as file:
    
        if histogram_name in file:
        
            histogram   = file[histogram_name]
            hist_values = histogram.values()
            bin_edges   = histogram.axes[0].edges()
            
            return bin_edges, hist_values
            
        else:
            print(f"Histogram {histogram_name} not found in file {root_file}")
            
            return None, None

# plot stacked histograms
def plot_stacked_histogram(histogram_name, semilep_histograms, fullhad_histograms, fulllep_histograms, variation, selection, output_dir):
    
    """
    Plots a stacked histogram for all processes.
    Parameters:
    - histogram_name: str, name of the histogram.
    - semilep_histograms: list of tuples (bin_edges, values) for semi-leptonic process.
    - fullhad_histograms: list of tuples (bin_edges, values) for fully hadronic process.
    - fulllep_histograms: list of tuples (bin_edges, values) for fully leptonic process.
    - variation: str, the BSM variation being plotted.
    - selection: str, either 'NoSel' or 'TestSel'.
    """

    plt.figure(figsize=(8, 6))
    
    # stacking histograms
    plt.hist([semilep_histograms[0][0][:-1],fullhad_histograms[0][0][:-1],fulllep_histograms[0][0][:-1]],
    weights=[semilep_histograms[0][1],fullhad_histograms[0][1],fulllep_histograms[0][1]],
    stacked=True,bins=np.linspace(10,140,20),label=["Semi-leptonic","Fully hadronic","Fully leptonic"],
    color=['silver','lightgreen','cornflowerblue'], edgecolor='black')

    xlabel = determine_xlabel(histogram_name)
    
    plt.xlabel(xlabel)
    plt.ylabel('Events')
    plt.ylim(1, None)
    plt.yscale('log')
    plt.title(f'{histogram_name} ({variation}) ({selection})')
    plt.legend()
    plt.grid(True)
    
    output_filename = f"{histogram_name[:-2]}_{variation}_{selection}.png"
    plt.savefig("/ceph/salshamaily/topEWK_FCCee/plots/"+output_filename)
    
    plt.show()
    plt.close()
    
    # overlaying histograms
    plt.figure(figsize=(8, 6))
    
    plt.hist(semilep_histograms[0][0][:-1], weights=semilep_histograms[0][1],
    bins=np.linspace(10, 140, 20), histtype='stepfilled', label="Semi-leptonic",
    color='silver', linewidth=2, alpha=0.7)
    
    plt.hist(fulllep_histograms[0][0][:-1], weights=fulllep_histograms[0][1],
    bins=np.linspace(10, 140, 20), histtype='stepfilled', label="Fully leptonic",
    color='cornflowerblue', linewidth=2, alpha=0.5)
    
    plt.hist(fullhad_histograms[0][0][:-1], weights=fullhad_histograms[0][1],
    bins=np.linspace(10, 140, 20), histtype='stepfilled', label="Fully hadronic",
    color='lightgreen', linewidth=2, alpha=0.5)
    
    plt.xlabel(xlabel)
    plt.ylabel('Events')
    plt.ylim(1, None)
    plt.yscale('log')
    plt.title(f'{histogram_name} ({variation}) ({selection})')
    plt.legend()
    plt.grid(True)

    output_filename_ol = f"{histogram_name[:-2]}_{variation}_{selection}_ol.png"
    plt.savefig("/ceph/salshamaily/topEWK_FCCee/plots/"+output_filename_ol)
    plt.show()
    plt.close()
    
    # saving histograms as ROOT files
    print('ROOT FILE FOR SEMI-LEPTONIC\n')
    save_histogram_as_root(f"{histogram_name[:-2]}",semilep_histograms[0][0],
    semilep_histograms[0][1],output_dir,"semilep",variation,selection)
    
    print('ROOT FILE FOR FULLY LEPTONIC\n')
    save_histogram_as_root(f"{histogram_name[:-2]}",fulllep_histograms[0][0],
    fulllep_histograms[0][1],output_dir,"fulllep",variation,selection)
    
    print('ROOT FILE FOR FULLY HADRONIC\n')
    save_histogram_as_root(f"{histogram_name[:-2]}",fullhad_histograms[0][0],
    fullhad_histograms[0][1],output_dir,"fullhad",variation,selection)

# processing multiple root files
def process_multiple_files(root_files, output_dir):
    histograms_by_variation = {}

    for root_file in root_files:
        classification = classify_file(root_file)
        variation      = extract_variation(root_file)
        selection      = extract_selection(root_file)

        print(f"Processing file: {root_file}\n")
        print(f"Classification: {classification}, Variation: {variation}, Selection: {selection}\n")

        if variation not in histograms_by_variation:
            histograms_by_variation[variation] = {'semilep': {}, 'fullhad': {}, 'fulllep':{}}

        with uproot.open(root_file) as file:
            histogram_names = [key for key in file.keys() if file[key].classname.startswith("TH")]

            for hist_name in histogram_names:
                print(f"Histogram: {hist_name}")
                bin_edges, hist_values = read_histogram_data(root_file, hist_name)

                if bin_edges is not None and hist_values is not None:
                    hist_data = (bin_edges, hist_values)

                    if hist_name not in histograms_by_variation[variation][classification]:
                            histograms_by_variation[variation][classification][hist_name] = {}
                            
                    if classification == 'semilep':
                        if selection in histograms_by_variation[variation]['semilep'][hist_name] and histograms_by_variation[variation]['semilep'][hist_name][selection]:
                            histograms_by_variation[variation]['semilep'][hist_name][selection] = (hist_data[0], hist_data[1]+histograms_by_variation[variation]['semilep'][hist_name][selection][1])
                        
                        else:
                            histograms_by_variation[variation]['semilep'][hist_name][selection] = hist_data
                    
                    else:
                        histograms_by_variation[variation][classification][hist_name][selection] = hist_data
    
    for variation, histograms in histograms_by_variation.items():
    
        if histograms['semilep'] and histograms['fullhad'] and histograms['fulllep']:

            for hist_name in histograms['semilep']:

                for selection in histograms['semilep'][hist_name]:

                    # check if the corresponding histograms exist for 'fullhad' and 'fulllep'
                    if hist_name in histograms['fullhad'] and selection in histograms['fullhad'][hist_name] and \
                       hist_name in histograms['fulllep'] and selection in histograms['fulllep'][hist_name]:

                        semilep_hist_data = histograms['semilep'][hist_name][selection]
                        fullhad_hist_data = histograms['fullhad'][hist_name][selection]
                        fulllep_hist_data = histograms['fulllep'][hist_name][selection]

                        # pass the histograms for all three processes to the plotting function
                        if semilep_hist_data is not None and fullhad_hist_data is not None and fulllep_hist_data is not None:
                            plot_stacked_histogram(hist_name, [semilep_hist_data], [fullhad_hist_data], [fulllep_hist_data], variation, selection, output_dir)
                            print(f"Plotting for histogram: {hist_name}, Variation: {variation}, Selection: {selection}\n")
                            
# Process files
process_multiple_files(root_files, output_dir)
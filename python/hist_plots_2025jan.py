# importing variables from analysis_final.py
import sys
sys.path.append('./analysis')
from analysis_final import procDictAdd, intLumi

# importing other packages
import glob
import ROOT
import os

# glob all .root hist files
root_files = glob.glob('/ceph/salshamaily/topEWK_FCCee/analysis/final_output/*.root')

# output directory where ROOT histograms will be saved
output_dir = "/ceph/salshamaily/topEWK_FCCee/samples/all"

# input directory for plotting function
plot_files = glob.glob("/ceph/salshamaily/topEWK_FCCee/samples/all/*.root")

# output directory for plotting function
outplot_dir = "/ceph/salshamaily/topEWK_FCCee/plots/distribution/stack_2025jan"

# determine xlabel based on histogram name
def get_xlabel(histogram_name):

    """
    Determines the appropriate x-axis label based on keywords in the histogram name.
    Parameters:
    - histogram_name: str, name of the histogram.
    Returns:
    - xlabel: str, the x-axis label.
    """
    
    keyword_to_label = {
        "energy": "Energy [GeV]",
        "pt": "p_{T} [GeV]",
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
    
def get_selection(root_file):

    """
        Obtains selection from the file name.
        Parameters: 
        - root_file: str, name of the file.
        Returns:
        - selection: str, selection.
        """
    
    components = root_file.split('_')
    
    if len(components) > 1:
        return components[-2]
    else:
        return 'unknown'
    
# function to extract the variation (e.g., 'ta_ttAdown') from the file name
def get_variation(root_file):

    """
    Obtains variation from the file name. If no BSM variation found, returns SM.
    Parameters: 
    - root_file: str, name of the file.
    Returns:
    - var: str, variation.
    """

    var_list = ["ta_ttAdown", "ta_ttAup","tv_ttAdown", "tv_ttAup","vr_ttZdown", "vr_ttZup","SM"]
    
    for var in var_list:
        if var in root_file:
            return var
            
def get_process(root_file):

    """
    Obtains variable from the file name.
    Parameters: 
    - root_file: str, name of the file.
    Returns:
    - variable: str, variable.
    """
    
    process_list = ["thadThad","tlepTlep","tlepThad","thadTlep"]
    
    for process in process_list:
        if process in root_file:
            return process

# reading histogram data from root files
def read_data(root_files):

    # function that parses file names to use in re-scaling
    def parse_data(filename):
        new_filename = filename[53:-len(filename.split("365")[-1])]
        return new_filename

    print('Processing ROOT files...')
    
    for file in root_files:
        f = ROOT.TFile.Open(file)
        
        variation = get_variation(file)
        selection = get_selection(file)
        process   = get_process(file)
    
        for key in f.GetListOfKeys():
            variable = key.ReadObj()
        
            if isinstance(variable, ROOT.TH1):
                hist = variable.Clone()  # cloning to avoid file deletion
                hist.SetDirectory(0)
                
                # from analysis_final.py
                parsed_filename = parse_data(file)
                SumOfWeights    = procDictAdd[parsed_filename]['sumOfWeights']
                N_exp           = procDictAdd[parsed_filename]['crossSection']*intLumi
                
                # re-scaling histogram for accuracy
                factor = hist.GetEntries()/hist.Integral() * (N_exp/SumOfWeights)
                hist.Scale(factor)
                
                # output histogram file names
                output_file = os.path.join(output_dir, f"{variable.GetName()}_{process}_{variation}_{selection}_histo.root")

            # create new root file to write histogram
            new_file = ROOT.TFile(output_file, "RECREATE")  # "RECREATE" to overwrite an existing file
            hist.Write()
            new_file.Close()

        f.Close()

# plotting root histograms
def plot_data(root_files):

    histograms = {}
    
    # color map for processes
    process_colors = {
        "thadThad": ROOT.kGreen-9,
        "tlepTlep": ROOT.kBlue-9,
        "tlepThad": ROOT.kGray,
        "thadTlep": ROOT.kMagenta-9
    }
    
    print('Processing plotting files...')
    
    for file in root_files:
        f = ROOT.TFile.Open(file)
        
        variation = get_variation(file)
        selection = get_selection(file)
        process   = get_process(file)
    
        for key in f.GetListOfKeys():
            variable = key.ReadObj()
        
            if isinstance(variable, ROOT.TH1):
                hist = variable.Clone()  # cloning to avoid file deletion
                hist.SetDirectory(0)
                hist.SetTitle('')
                
                # grouping histograms according to nested dictionaries
                variable_name = hist.GetName()
                
                if variation not in histograms:
                    histograms[variation] = {}
                if selection not in histograms[variation]:
                    histograms[variation][selection] = {}
                if variable_name not in histograms[variation][selection]:
                    histograms[variation][selection][variable_name] = []
                
                # adding process and histogram to the group
                histograms[variation][selection][variable_name].append((process, hist))
        
        f.Close()
    
    # plotting grouped histograms
    print('Starting to plot...')
    
    for variation, selection_dict in histograms.items():
        for selection, variable_dict in selection_dict.items():
            for variable_name, hist_list, in variable_dict.items():
            
                # sort the histograms by the number of entries for stacking
                hist_list.sort(key=lambda x: x[1].GetEntries(), reverse=True)

                # initializing canvas, stack, legend
                c1 = ROOT.TCanvas('c1', 'c1', 800, 600)
                l1 = ROOT.TLegend(0.7,0.7,0.9,0.9)
                s1 = ROOT.THStack(f'stack_{variable_name}', f'{variable_name} ({variation}, {selection})')
                
                # determining x-axis title based on variable name
                xlabel = get_xlabel(variable_name)
                
                # adding histogramas to the stack object
                for i, (process, hist) in enumerate(hist_list):
                    color = process_colors.get(process)
                    hist.SetLineColor(ROOT.kBlack)
                    hist.SetFillColor(color)
                    s1.Add(hist)
                    l1.AddEntry(hist, process, 'f')
                
                s1.Draw('hist')
                s1.GetXaxis().SetTitle(xlabel)
                s1.GetYaxis().SetTitle('Events')
                s1.SetTitle(f'{variable_name} ({variation}) ({selection})')
                l1.Draw()
                c1.Update()
                c1.SaveAs(os.path.join(outplot_dir, f"{variable_name}_{variation}_{selection}.png"))
                c1.Draw()
                
                print(f'Saved {variable_name} plot...')
               
read_data(root_files)
plot_data(plot_files)
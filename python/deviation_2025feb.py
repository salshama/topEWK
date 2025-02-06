# importing packages
import sys
import glob
import ROOT
import os

# importing other useful files
sys.path.append('./python')
sys.path.append('./analysis')
from hist_plots_2025jan import get_xlabel, get_selection, get_variation, get_process
from analysis_final import procDictAdd, intLumi

# glob all .root hist files
root_files = glob.glob('/ceph/salshamaily/topEWK_FCCee/samples/all/*.root')

# output directory where ROOT histograms will be saved
output_dir = "/ceph/salshamaily/topEWK_FCCee/samples/deviation"

# input directory for plotting function
plot_files = glob.glob("/ceph/salshamaily/topEWK_FCCee/samples/deviation/*.root")

# output directory for plotting function
outplot_dir = "/ceph/salshamaily/topEWK_FCCee/plots/deviation/stack_2025feb"

# original root files to use in parse_data() function
parse_dir = "ceph/salshamaily/topEWK_FCCee/analysis/final_output"
        
# calculating deviations
def calculate_deviations(root_files):
    
    print('Calculating deviations...')
    
    histograms = {}
    
    # function to manipulate file names from final output analysis used in re-scaling
    def pad_data(filename, process, variation):
    
            if variation == "SM":
                    return f"wzp6_ee_SM_tt_{process}_noCKMmix_keepPolInfo_ecm365"
            
            return f"wzp6_ee_SM_tt_{process}_noCKMmix_keepPolInfo_{variation}_ecm365"
    
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
                
                variable_name = hist.GetName()
                
                # from analysis_final.py
                parsed_filename = pad_data(file, process, variation)
                SumOfWeights    = procDictAdd[parsed_filename]['sumOfWeights']
                N_exp           = procDictAdd[parsed_filename]['crossSection']*intLumi
                
                # re-scaling histogram for accuracy
                factor = hist.GetEntries()/hist.Integral() * (N_exp/SumOfWeights)
                hist.Scale(factor)
                
                # group histograms using nested dictionaries
                if variable_name not in histograms:
                    histograms[variable_name] = {}
                    
                if process not in histograms[variable_name]:
                    histograms[variable_name][process] = {}
                    
                if selection not in histograms[variable_name][process]:
                    histograms[variable_name][process][selection] = {}
                    
                # adding groups to a list
                histograms[variable_name][process][selection][variation] = hist
                
        f.Close()
    
    # getting deviations for each variable, process, selection
    for variable_name, process_dict in histograms.items():
        for process, selection_dict in process_dict.items():
            for selection, variation_dict in selection_dict.items():
            
                sm_hist = variation_dict['SM']
            
                for variation, hist in variation_dict.items():
                    if variation == 'SM':
                        continue
                    
                    # subtracting SM from BSM histograms
                    deviation_hist = hist.Clone()
                    deviation_hist.Add(sm_hist,-1)
                
                    # saving deviation histogram to output file
                    output_file = os.path.join(output_dir, f'{variable_name}_{process}_{variation}_{selection}_devhisto.root')
                
                    output_root = ROOT.TFile(output_file, 'RECREATE')
                    deviation_hist.Write()
                    output_root.Close()
                
                    print(f'Saved {deviation_hist.GetName()} to {output_file}')
                
# plotting deviation histograms
def plot_deviations(root_files):

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
                c2 = ROOT.TCanvas('c2', 'c2', 800, 600)
                l2 = ROOT.TLegend(0.7,0.7,0.9,0.9)
                s2 = ROOT.THStack(f'stack_{variable_name}', f'{variable_name} ({variation}, {selection})')
                
                # determining x-axis title based on variable name
                xlabel = get_xlabel(variable_name)
                
                # adding histogramas to the stack object
                for i, (process, hist) in enumerate(hist_list):
                    color = process_colors.get(process)
                    hist.SetLineColor(ROOT.kBlack)
                    hist.SetFillColor(color)
                    s2.Add(hist)
                    l2.AddEntry(hist, process, 'f')
                
                s2.Draw('hist')
                s2.GetXaxis().SetTitle(xlabel)
                s2.GetYaxis().SetTitle('$\Delta$(mod - SM)')
                s2.SetTitle(f'{variable_name} ({variation}) ({selection})')
                l2.Draw()
                c2.Update()
                c2.SaveAs(os.path.join(outplot_dir, f"{variable_name}_{variation}_{selection}_devstack.png"))
                c2.Draw()
                
                print(f'Saved {variable_name} plot...')
                
calculate_deviations(root_files)
plot_deviations(plot_files)
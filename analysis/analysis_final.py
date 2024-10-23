#Input directory where the files produced at the stage1 level are
inputDir = "/ceph/salshamaily/topEWK_FCCee/analysis/stage2_output" #your stage2 directory

#Output directory where the files produced at the final-selection level are
outputDir = "/ceph/salshamaily/topEWK_FCCee/analysis/final_output" #your final directory

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 2.5e6 #pb^-1 #to be checked again for 240 gev

#Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = True

#Save event yields in a table (optional)
saveTabular = True

#Number of CPUs to use
nCPUS = 8

#produces ROOT TTrees, default is False
doTree = False

processList = {
			   "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ecm365": {},
               "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ecm365": {},
               "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ecm365": {},
               "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ecm365": {},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ta_ttAup_ecm365":   {},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_tv_ttAup_ecm365":   {},
             "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {},
             "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_vr_ttZup_ecm365":   {},
             "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {},
             "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ta_ttAup_ecm365":   {},
             "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {},
             "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_tv_ttAup_ecm365":   {},
             "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {},
             "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_vr_ttZup_ecm365":   {},
             "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {},

             "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ta_ttAup_ecm365":   {},
             "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {},
             "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_tv_ttAup_ecm365":   {},
             "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {},
             "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_vr_ttZup_ecm365":   {},
             "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {},

             "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ta_ttAup_ecm365":   {},
             "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {},
             "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_tv_ttAup_ecm365":   {},
             "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {},
             "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_vr_ttZup_ecm365":   {},
             "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {},
}

###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {
    #backgrounds
    'p8_ee_Zee_ecm91':"Z $\rightarrow$ ee",
    'p8_ee_Zmumu_ecm91':"Z $\rightarrow \mu \mu$",
    'p8_ee_Ztautau_ecm91':"Z $\rightarrow \tau \tau$",
    'p8_ee_Zbb_ecm91':"Z $\rightarrow$ bb",
    'p8_ee_Zcc_ecm91':"Z $\rightarrow$ cc",
    'p8_ee_Zud_ecm91':"Z $\rightarrow$ ud",
    'p8_ee_Zss_ecm91':"Z $\rightarrow$ ss",
    
}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ecm365": {"numberOfEvents": 6400000, "sumOfWeights": 6400000, "crossSection": 1.9E6 * 0.106 / 2.5E6 , "kfactor": 1.0, "matchingEfficiency": 1.0},
    "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ecm365": {"numberOfEvents": 6400000, "sumOfWeights": 6400000, "crossSection": 1.9E6 * 0.220 / 2.5E6 , "kfactor": 1.0, "matchingEfficiency": 1.0},
    "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ecm365": {"numberOfEvents": 6400000, "sumOfWeights": 6400000, "crossSection": 1.9E6 * 0.220 / 2.5E6 , "kfactor": 1.0, "matchingEfficiency": 1.0},
    "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ecm365": {"numberOfEvents": 6400000, "sumOfWeights": 6400000, "crossSection": 1.9E6 * 0.454 / 2.5E6 , "kfactor": 1.0, "matchingEfficiency": 1.0},

}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### no selection, just builds the histograms, it will not be shown in the latex table
    "NoSel":     "1>0",
    "TestSel":   "(n_muons_pass==1) or (n_electrons_pass==1)",
#    "dilep_s06_1b05":   "dilep_R5_cat==1   and n_btags==1 and jet_leadS_isS > 0.6",
#    "semilep_s06_1b05": "semilep_R5_cat==1 and n_btags==1 and jet_leadS_isS > 0.6",
#    "dihad_s06_1b05":   "dihad_R5_cat==1   and n_btags==1 and jet_leadS_isS > 0.6",

    ### here you can add your cuts and selections on the variables built in stage 1 and 2
    #"sel2RecoSF_vetoes": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0",
    #"sel2RecoSF_vetoes_notracks": "((n_RecoElectrons==2 && n_RecoMuons==0) || (n_RecoMuons==2 && n_RecoElectrons==0)) && ((Reco_charge.at(0)==1 && Reco_charge.at(1)==-1) || (Reco_charge.at(0)==-1 && Reco_charge.at(1)==1)) && n_RecoPhotons==0 && n_noLeptonTracks==0",
}

# Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well, it's only for the table ###
cutLabels = {
    "NoSel": "No selection",
    "TestSel": "Test",
#    "dilep_s06_1b05":   "dilep, s>0.6, 1 b>0.5",
#    "semilep_s06_1b05": "semilep, s>0.6, 1 b>0.5",
#    "dihad_s06_1b05":   "dihad, s>0.6, 1 b>0.5",
}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "muon_pass_energy":      {"name":"muon_pass_energy",       "title":"muon energy [GeV]",      "bin":90, "xmin":0 ,"xmax":180},
    "muon_pass_eta":         {"name":"muon_pass_eta",          "title":"muon eta",               "bin":60, "xmin":-3 ,"xmax":3},
    "muon_pass_pt":          {"name":"muon_pass_pt",           "title":"muon pt [GeV]",          "bin":100,"xmin":0 ,"xmax":100},
    "electron_pass_energy":  {"name":"electron_pass_energy",   "title":"electron energy [GeV]",  "bin":90, "xmin":0 ,"xmax":180},
    "electron_pass_eta":     {"name":"electron_pass_eta",      "title":"electron eta",           "bin":60, "xmin":-3 ,"xmax":3},
    "electron_pass_pt":      {"name":"electron_pass_pt",       "title":"electron pt [GeV]",      "bin":100,"xmin":0 ,"xmax":100},
    "Emiss_energy":          {"name":"Emiss_energy",           "title":"missing energy [GeV]",   "bin":90, "xmin":0, "xmax":180}
}
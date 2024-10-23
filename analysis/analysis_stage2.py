import os, copy # tagging

#Mandatory: List of processes
processList = {
               "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ecm365": {},
               "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ecm365": {},
               "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ecm365": {},
               "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ecm365": {},
             "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ta_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_tv_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_vr_ttZup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {'chunks':5},

              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ta_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_tv_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_vr_ttZup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {'chunks':5},

              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ta_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_tv_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_vr_ttZup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {'chunks':5},

              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ta_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ta_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_tv_ttAup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_tv_ttAdown_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_vr_ttZup_ecm365": {'chunks':5},
              "wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_vr_ttZdown_ecm365": {'chunks':5},

            }

#Optional: output directory, default is local running directory
inputDir = "/ceph/xzuo/FCC_ntuples/topEWK/ntuples_20240205"
outputDir   = "/ceph/salshamaily/topEWK_FCCee/analysis/stage2_output"

#EOS output directory for batch jobs
#outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topEWK/flatNtuples_20240108/winter2023"

#Optional
nCPUS       = 8
runBatch    = False
batchQueue  = "nextweek"
compGroup   = "group_u_FCC.local_gen"

# Additional/custom C++ functions, defined in header files
#includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

               .Define("muon_pass",         "(muon_energy > 13) * 1.0")
               .Define("muon_pass_px",      "muon_px[muon_pass==1]")
               .Define("muon_pass_py",      "muon_py[muon_pass==1]")
               .Define("muon_pass_pz",      "muon_pz[muon_pass==1]")
               .Define("muon_pass_pt",      "sqrt(muon_pass_px*muon_pass_px + muon_pass_py*muon_pass_py)")
               .Define("muon_pass_phi",     "muon_phi[muon_pass==1]")
               .Define("muon_pass_eta",     "muon_eta[muon_pass==1]")
               .Define("muon_pass_energy",  "muon_energy[muon_pass==1]")
               .Define("muon_pass_mass",    "muon_mass[muon_pass==1]")
               .Define("muon_pass_charge",  "muon_charge[muon_pass==1]")
               .Define("muon_pass_d0",      "muon_d0[muon_pass==1]")
               .Define("muon_pass_z0",      "muon_z0[muon_pass==1]")
               .Define("n_muons_pass",      "return int(muon_pass_energy.size())")
               
               .Define("electron_pass",         "(electron_energy > 13) * 1.0")
               .Define("electron_pass_px",      "electron_px[electron_pass==1]")
               .Define("electron_pass_py",      "electron_py[electron_pass==1]")
               .Define("electron_pass_pz",      "electron_pz[electron_pass==1]")
               .Define("electron_pass_pt",      "sqrt(electron_pass_px*electron_pass_px + electron_pass_py*electron_pass_py)")
               .Define("electron_pass_phi",     "electron_phi[electron_pass==1]")
               .Define("electron_pass_eta",     "electron_eta[electron_pass==1]")
               .Define("electron_pass_energy",  "electron_energy[electron_pass==1]")
               .Define("electron_pass_mass",    "electron_mass[electron_pass==1]")
               .Define("electron_pass_charge",  "electron_charge[electron_pass==1]")
               .Define("electron_pass_d0",      "electron_d0[electron_pass==1]")
               .Define("electron_pass_z0",      "electron_z0[electron_pass==1]")
               .Define("n_electrons_pass",      "return int(electron_pass_energy.size())")
               
               .Filter("n_muons_pass==1 or n_electrons_pass==1") # only takes boolean value
               .Filter("Emiss_energy.at(0) > 23")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "muon_pass_px", "muon_pass_py", "muon_pass_pz", "muon_pass_pt",
                 "muon_pass_phi", "muon_pass_eta", "muon_pass_energy", "muon_pass_mass",
                 "muon_pass_charge","n_muons_pass", "electron_pass", "electron_pass_px",
                 "electron_pass_py","electron_pass_pz", "electron_pass_pt",
                 "electron_pass_phi","electron_pass_eta", "electron_pass_energy",
                 "electron_pass_mass","electron_pass_charge","n_electrons_pass",
                 "Emiss_energy","Emiss_px","Emiss_py","Emiss_pz","Emiss_phi","Emiss_eta",
#                 "n_genTops", "n_genWs", "n_genBottoms", "n_genStranges", "n_genMuons", "n_genElectrons", 
#                 "Wp_elenu", "Wp_munu", "Wp_taunu", "Wp_d", "Wp_s", "Wp_b",
#                 "Wm_elenu", "Wm_munu", "Wm_taunu", "Wm_d", "Wm_s", "Wm_b",
#                 "genW_px", "genW_py", "genW_pz", "genW_phi", "genW_eta", "genW_energy", "genW_mass", "genW_charge",
#                 "n_muons", "n_electrons", "n_photons",
#                 "muon_px", "muon_py", "muon_pz", "muon_phi", "muon_eta", "muon_energy", "muon_mass", "muon_charge",
#                 "electron_px", "electron_py", "electron_pz", "electron_phi", "electron_eta", "electron_energy", "electron_mass", "electron_charge",
#                 "photon_px", "photon_py", "photon_pz", "photon_phi", "photon_eta", "photon_energy", "photon_mass",
#                 "recoEmiss_px", "recoEmiss_py", "recoEmiss_pz", "recoEmiss_e"
                 ]

        return branchList
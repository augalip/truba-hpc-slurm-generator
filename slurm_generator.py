import os

def provide_header(use_mail: bool):
    text_p1 = """#!/bin/bash
#SBATCH -p {hpc_set}
#SBATCH -A {user_id}
#SBATCH -J {job_alias}
#SBATCH --time={duration}
#SBATCH -n {core_count}
#SBATCH -N {node_count} 
#SBATCH --mail-type=ALL
#SBATCH --mail-user={mail_to} 
#SBATCH --output={output_file}
#SBATCH --error={error_file}

##########################################################
##########################################################
##########################################################
############### LOAD MODULES AND LIBRARIES ###############
##########################################################
"""
    text_p1_nomail = """#!/bin/bash
#SBATCH -p {hpc_set}
#SBATCH -A {user_id}
#SBATCH -J {job_alias}
#SBATCH --time={duration}
#SBATCH -n {core_count}
#SBATCH -N {node_count} 
#SBATCH --output={output_file}
#SBATCH --error={error_file}

##########################################################
##########################################################
##########################################################
############### LOAD MODULES AND LIBRARIES ###############
##########################################################
"""  
    if (use_mail == True):
        return text_p1
    else:
        return text_p1_nomail
    
def provide_code_area_seperator():
    text_p2 = """
##########################################################
##########################################################
##########################################################
######################## RUN CODE ########################
##########################################################
"""
    return text_p2

def hpc_name_verification(hpc_name: str):
    hpc_name = hpc_name.lower()
    terminated_clusters = ["Short", "mid1"]
    
    for cluster in terminated_clusters:
        if hpc_name == cluster:
            print("Short ve mid1 kurukları 1 Aralık 2021 tarihinde kapatılmıştır. İş yükü önerilen \"hamsi\" sunucusuna aktarıldı.")
            hpc_name = "hamsi"
            return hpc_name
        
    available_names = ["single", "debug", "mid2", "long", "interactive", "smp", "sardalya", "barbun", "barbun-cuda", "akya-cuda", "palamut-cuda", "hamsi", "orfoz"]
    for name in available_names:
        if hpc_name == name:
            return hpc_name
    raise Exception("Girilmiş olan küme adı, Truba üzerindeki küme isimleri ile eşleşmiyor.") 

def duration_correction(duration_text: str):
    if "-" not in duration_text:
        raise Exception("Süre metni için gün değeri boş bırakılamaz. Örnek format: G-SS:DD:ss")
    if ":" not in duration_text:
        raise Exception("Süre metni hatalı. Örnek format: G-SS:DD:ss")
    
    duration_parts_day = duration_text.split("-")[0]
    duration_parts_remaining = duration_text.split("-")[1].split(":")
    duration_parts = [duration_parts_day, *duration_parts_remaining]
    duration_parts = [int(x) for x in duration_parts]    
    duration_day, duration_hour, duration_minute, duration_second = duration_parts
    if duration_second >= 60:
        excess_min = duration_second // 60
        duration_second %= 60
        duration_minute += excess_min
        
    if duration_minute >= 60:
        excess_hour = duration_minute // 60
        duration_minute %= 60
        duration_hour += excess_hour
        
    if duration_hour >= 24:
        excess_day = duration_hour // 24
        duration_hour %= 24
        duration_day += excess_day
        
    return str(duration_day) + "-" + str(duration_hour).zfill(2) + ":" + str(duration_minute).zfill(2) + ":" + str(duration_second).zfill(2)

def duration_to_seconds(duration_to_convert: str):
    duration_parts_day = duration_to_convert.split("-")[0]
    duration_parts_remaining = duration_to_convert.split("-")[1].split(":")
    duration_parts = [duration_parts_day, *duration_parts_remaining]
    duration_parts = [int(x) for x in duration_parts]
    seconds_to_return = duration_parts[0] * 86400 + duration_parts[1] * 3600 + duration_parts[2] * 60 + duration_parts[3]
    return seconds_to_return

def max_duration_verification(hpc_name: str, duration_text: str):
    hpc_name = hpc_name.lower()
    
    #reverify to be safe
    duration_text = duration_correction(duration_text = duration_text)
    if hpc_name_verification(hpc_name = hpc_name) == False:
        raise Exception("Küme adı doğrulanamadı.")
    
    #checking the max duration
    
    max_durations = {"single": "15-00:00:00", "debug": "00-00:15:00", "mid2": "08-00:00:00", "long": "15-00:00:00", "interactive": "15-00:00:00",
                    "smp": "08-00:00:00", "sardalya": "15-00:00:00", "barbun": "15-00:00:00", "barbun-cuda": "15-00:00:00", 
                    "akya-cuda": "15-00:00:00", "palamut-cuda": "03-00:00:00", "hamsi": "03-00:00:00", "orfoz": "03-00:00:00"}
    current_max = max_durations[hpc_name]
    current_max_seconds = duration_to_seconds(duration_to_convert=current_max)
    requested_seconds = duration_to_seconds(duration_to_convert=duration_text)
    
    if requested_seconds > current_max_seconds:
        return current_max
    else:
        return duration_text
    
def requested_core_node_verification(hpc_name: str, core_count: int, node_count: int):
    hpc_name = hpc_name.lower()    
    #reverify to be safe
    if hpc_name_verification(hpc_name = hpc_name) == False:
        raise Exception("Küme adı doğrulanamadı.")
    
    min_core = {"single": 1, "debug": 1, "mid2": 4, "long": 4, "interactive": 1, "smp": 4, "sardalya": 4, "barbun": 4, "barbun-cuda": 20, 
                    "akya-cuda": 10, "palamut-cuda": 16, "hamsi": 28, "orfoz": 56}
    max_node_count = {"single": 8, "debug": 238, "mid2": 189, "long": 189, "interactive": 14, "smp": 1, "sardalya": 100, "barbun": 119, "barbun-cuda": 24, 
                    "akya-cuda": 24, "palamut-cuda": 9, "hamsi": 144, "orfoz": 504}
    
    current_min_core = min_core[hpc_name]
    current_max_node = max_node_count[hpc_name]

    if (node_count > current_max_node):
        node_count = current_max_node
        
    elif (node_count < 1):
        node_count = 1
    
    if core_count < 1:
        core_count = 1
    
    requested_core_per_node = core_count // node_count
    
    if (requested_core_per_node < current_min_core):
        core_count = current_min_core * node_count    
    return core_count, node_count

def add_exports(script_text_to_use: str, exports: [str]):
    for export in exports:
        script_text_to_use += (export + "\n")
    
    script_text_to_use += provide_code_area_seperator()
    return script_text_to_use

    
def add_codes(script_text_to_use: str, codes: [str]):
    for code in codes:
        script_text_to_use += (code + "\n")
    return script_text_to_use


def change_script_extension(save_path_to_use: str, new_extension: str):
    if "." not in save_path_to_use:
        return save_path_to_use + "." + str(new_extension)
    else:
        path_elements = save_path_to_use.split(".")
        path_elements[-1] = new_extension
        new_save_path = ".".join(path_elements)
        return new_save_path           


def save_script(save_path: str, script_text_to_use: str):
    save_path = change_script_extension(save_path_to_use = save_path, new_extension="sh")
    with open(save_path, "w") as text_file:
        text_file.write(script_text_to_use)
        

def slurm_betik_olusturucu(script_kayit_dizini: str, kume_adi: str, kullanici_adi: str, is_adi: str, sure: str, cekirdek_sayisi: int, node_sayisi: int,
                          cikti_dizini: str, hata_dizini: str, exports: [str] = [], kodlar: [str] = [], mail_adresi: str = ""):
    script_text = ""
    if mail_adresi == "":
        script_text = provide_header(use_mail = False)
    else:
        script_text = provide_header(use_mail = True)
        script_text = script_text.replace("{mail_to}", mail_adresi)
    
    kume_adi = hpc_name_verification(hpc_name = kume_adi)
    sure = duration_correction(duration_text = sure)
    sure = max_duration_verification(hpc_name = kume_adi, duration_text = sure)
    cekirdek_sayisi, node_sayisi = requested_core_node_verification(hpc_name= kume_adi, core_count= cekirdek_sayisi, node_count= node_sayisi)
        
    script_text = script_text.replace("{hpc_set}", kume_adi)
    script_text = script_text.replace("{user_id}", kullanici_adi)
    script_text = script_text.replace("{job_alias}", is_adi)
    script_text = script_text.replace("{duration}", sure)
    script_text = script_text.replace("{core_count}", str(cekirdek_sayisi))
    script_text = script_text.replace("{node_count}", str(node_sayisi))
    script_text = script_text.replace("{output_file}", cikti_dizini)
    script_text = script_text.replace("{error_file}", hata_dizini)
    
    script_text = add_exports(script_text_to_use= script_text, exports= exports)
    script_text += provide_code_area_seperator()
    script_text = add_codes(script_text_to_use= script_text, codes= kodlar)
    
    save_script(save_path= script_kayit_dizini, script_text_to_use= script_text)
    
    return script_text


# -*- coding: utf-8 -*-
"""
Created on Wed May 29 20:03:55 2024

@author: aparn
"""


import os
from kegg_file import KgmlFile
from pathway_component import  PathwayComponent
from geometry_annotation import GeometryAnnotation
from annotation_setting_ap import ANNOTATION_SETTINGS
from pathlib import Path


class Pathway:
    DATA_DIR = os.environ['KEGG_MAP_WIZARD_DATA']
    def __init__(self, map_id:str,file_types:list):
        self.map_id = map_id        
        self.__kegg_files = []
        self.__org_file = []              
        self._file_types = file_types          

    @property
    def kegg_files(self):
        if not self.__kegg_files:
            self.__kegg_files = self.__create_kegg_files()
        return self.__kegg_files
       
    @property
    def org_file(self):
        if not self.__org_file:
            self.__org_file = self.__create_org_file()
        return self.__org_file
    
    @property
    def pathway_components(self):
        return  self.__create_pathway_components()
    
    @property
    def title(self):
        title = set()
        files = self.kegg_files + self.org_file
        for file in files:            
            title.add(file.title)        
    
        return '/'.join(title)
    
    @property
    def pathway_number(self):
        pathway_number = set()
        files = self.kegg_files + self.org_file
        for file in files:            
            pathway_number.add(file.pathway_number)         
        return '/'.join(pathway_number)
    
    @property
    def org(self):
        org = []
        files = self.kegg_files + self.org_file
        for file in files:           
            if file.organism is not None:            
                org.append(file.organism)
        org = "_".join(org) 
        return org       
   
    def __create_kegg_files(self):
        kegg_files = []   
        kegg_file_types = [element for element in self._file_types if element != 'orgs']
        for file_type in kegg_file_types:
            kegg_files.append(KgmlFile(self.map_id[-5:], file_type, self.DATA_DIR))            
        return kegg_files
    
    def __create_org_file(self):     
        org_file = []        
        if 'orgs' in self._file_types:          
            org_file.append(KgmlFile(self.map_id, 'orgs', self.DATA_DIR))
        return org_file    
        

 #######################################   
    def __create_pathway_components(self):
        files = self.kegg_files + self.org_file
        if len(self.org_file) == 0 :
            organism=None
        else:
            organism = self.org_file[0].organism   
        merged_data = {}  
        
        for file in files:
            for entry in file.entries:
                graphics = entry.find('graphics')
                entry_data = {
                    "id": entry.get('id'),
                    "name": [entry.get('name')],
                    "type": [entry.get('type')],
                    "graphics": {
                        "type": graphics.get('type'),
                        "x": graphics.get('x'),
                        "y": graphics.get('y'),
                        "height": graphics.get('height'),
                        "width": graphics.get('width'),
                        "coords": graphics.get('coords')
                    }
                }
                
                pathway_component = PathwayComponent(entry_data)
                pathway_component.retrive_pathway_annotation_data()
                equivalent_pathway_component = pathway_component.is_equivalent(merged_data)
                if equivalent_pathway_component is not None:
                    updated_pathway_component = pathway_component.merge_pathway_components(equivalent_pathway_component)
                    merged_data.update(updated_pathway_component)
                else:
                    merged_data.update({pathway_component.pathway_component_id: pathway_component})
                    
        pathway_components = []
       
        annotations = self.__provide_annotations(organism)
        for key, value in merged_data.items():
            annotation_object = GeometryAnnotation(organism)
            geometry_annotation =  annotation_object.get_annotation(value.pathway_annotation_data,annotations)

            value.pathway_annotation_data = geometry_annotation
            
            pathway_components.append(value)
        return pathway_components

    def __provide_annotations(self, organism):
        annotations = {}

        for key, value in ANNOTATION_SETTINGS.items():
                       
            data_dict = {}
            
            rest_file = value['rest_file']
            if rest_file == 'org':
                rest_file = organism
            if rest_file != '':
                file_path = self.DATA_DIR / Path('rest_data') / Path(f"{rest_file}.txt")
            # Open the rest file and store it in a variable with the same name as the key
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        data = line.strip().split('\t')
                        if len(data) < 2:
                            key_anno = data[0]
                            value_anno = ""
                        else:
                            if key =='Gene':
                                key_anno = data[0]
                                value_anno = data[3]
                            else:
                                key_anno = data[0]
                                value_anno = data[1]
                                

                        data_dict[key_anno] = value_anno
                        
            except FileNotFoundError:
                data_dict[key] = ''
            exec(f"{key} = {data_dict}")
            
            annotations.update({key: data_dict})
            
        return annotations
            
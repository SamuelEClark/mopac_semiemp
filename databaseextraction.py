#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for extracting experimental values.

@author: mark
"""

import numpy as np
import scipy.stats as scistats
import logging
import phasexmlparser.parsers.xmlvalidation as xmlvalidation

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARN)

HUNTER_DB_NAMESPACE_DICT = {"hunterdb":"http://www-hunter.ch.cam.ac.uk/HunterDatabase"}

def extract_mol_info_from_db(database_etree, inchikey):
    """This extracts informaiuton
    """
    molecule_etree = extract_molecule(database_etree, inchikey)
    if molecule_etree != None:
        return inchikey, extract_mol_info(molecule_etree)
    else:
        raise IndexError("inchikey not in database")

def extract_mol_info(molecule_etree):
    """This extracts the alpha and betas to use, plus the smiles.
    """
    smiles = extract_smiles(molecule_etree)
    alpha = extract_and_check_alpha(molecule_etree)
    beta = extract_and_check_beta(molecule_etree)
    return smiles, alpha, beta

def extract_and_check_alpha(molecule_etree):
    """This read the alphas and then performs checks, getting the accepted (most common) value
    """
    alpha_etrees = extract_expt_alphas(molecule_etree)
    LOGGER.debug("alpha Etree")
    LOGGER.debug(len(alpha_etrees))
    LOGGER.debug(type(alpha_etrees))
    exp_alpha_data = process_exp_values(alpha_etrees)
    return check_expt_values(exp_alpha_data)
    
def extract_and_check_beta(molecule_etree):
    """This read the betas and then performs checks, getting the accepted (most common) value
    """
    beta_etrees = extract_exp_betas(molecule_etree)
    exp_beta_data = process_exp_values(beta_etrees)
    selected_value = check_expt_values(exp_beta_data)
    #update to add sign for beta so alpha and beta can be plotted on same scale.
    if selected_value != None:
        selected_value = (-selected_value[0], selected_value[1], selected_value[2])
    return selected_value

def check_expt_values(exp_values_data):
    """This checks the number of entries, and then performs checks on variance: most common value is selected if preferred does not exist.
    """
    
    #if only one value exists select that
    if len(exp_values_data) == 1:
        return exp_values_data[0]
    elif len(exp_values_data) == 0:
        return None
    #Else look for preferred value
    for exp_value in exp_values_data:
        if exp_value[2]:
            return exp_value
    #If no preferred value, take most common value.
    modal_value = get_modal_value(exp_values_data)
    for exp_value in exp_values_data:
        if np.abs(modal_value-exp_value[0])<0.01:
            return exp_value
    
def get_modal_value(exp_data_list):
    """This returns the modal value of the data.
    """
    value_array = np.array([exp_data_list[i][0] for i in range(len(exp_data_list))])
    return scistats.mode(value_array)[0][0]

def process_exp_values(exp_data_list):
    """This extracts each value and doi. This also extracts the value of preferred attribute tag.
    """
    exp_data_values = []
    for exp_data in exp_data_list:
        exp_data_values.append(process_exp_value(exp_data))
    return exp_data_values

def process_exp_value(exp_data):
    """This extracts the value, and doi for the molecule.
    """
    VALUE_XPATH = 'hunterdb:Value/child::text()'
    DOI_XPATH = 'hunterdb:Source/hunterdb:DOI/child::text()'
    PREFERRED_XPATH = '@hunterdb:preferredValue'
    doi_values = exp_data.xpath(DOI_XPATH, namespaces=HUNTER_DB_NAMESPACE_DICT)
    values_values = exp_data.xpath(VALUE_XPATH, namespaces=HUNTER_DB_NAMESPACE_DICT)
    preferred = exp_data.xpath(PREFERRED_XPATH, namespaces=HUNTER_DB_NAMESPACE_DICT)
    if len(preferred) == 1:
        preferred = bool(preferred[0])
    else:
        preferred= False
    if len(doi_values) == 1 & len(values_values) == 1:
        return (float(values_values[0]), doi_values[0], preferred)
    else:
        LOGGER.debug("values: {}", values_values)
        LOGGER.debug("doi_values: {}", doi_values)

def extract_expt_alphas(molecule_etree):
    """This extracts experimental alphas.
    """
    ALPHA_XPATH = 'hunterdb:ExperimentalProperties/hunterdb:Property[@hunterdb:name="alpha_expt"]'
    return molecule_etree.xpath(ALPHA_XPATH, namespaces=HUNTER_DB_NAMESPACE_DICT)

def extract_exp_betas(molecule_etree):
    """This extracts the experiemental betas.
    """
    BETA_XPATH = 'hunterdb:ExperimentalProperties/hunterdb:Property[@hunterdb:name="beta_expt"]'
    return molecule_etree.xpath(BETA_XPATH, namespaces=HUNTER_DB_NAMESPACE_DICT)

def extract_smiles(molecule_etree):
    """This extracts the smiles of the molecule.
    """
    SMILES_XPATH = 'hunterdb:Structure/hunterdb:CanonicalSmiles/child::text()'
    return molecule_etree.xpath(SMILES_XPATH, namespaces=HUNTER_DB_NAMESPACE_DICT)[0]

def extract_molecule(database_etree, inchikey):
    """This extracts the molecule xml from the complete dataset.
    """
    molecule_list = database_etree.xpath(create_xpath_for_molecule(inchikey), namespaces=HUNTER_DB_NAMESPACE_DICT)
    if len(molecule_list) == 1:
        return molecule_list[0]

def create_xpath_for_molecule(inchikey):
    """This is to extract the molecule entry.
    """
    return '/hunterdb:MoleculeList/hunterdb:Molecule[@hunterdb:inchikey="{:s}"]'.format(inchikey)


def read_and_validate_file(filename):
    """This reads and validates the file to an etree.
    """
    return xmlvalidation.validate_and_read_xml_file(filename, xmlvalidation.HUNTER_DB_SCHEMA)


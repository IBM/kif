# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef

# flake8: noqa


class SEMSCI(DefinedNamespace):
    """The Semanticscience Integrated Ontology (SIO).

    See <https://github.com/MaastrichtU-IDS/semanticscience>.
    """

    _NS = Namespace('http://semanticscience.org/resource/')
    CHEMINF_000140: URIRef
    CHEMINF_000334: URIRef
    CHEMINF_000335: URIRef
    CHEMINF_000338: URIRef
    CHEMINF_000339: URIRef
    CHEMINF_000372: URIRef
    CHEMINF_000376: URIRef
    CHEMINF_000379: URIRef
    CHEMINF_000382: URIRef
    CHEMINF_000390: URIRef
    CHEMINF_000395: URIRef
    CHEMINF_000396: URIRef
    CHEMINF_000399: URIRef
    CHEMINF_000407: URIRef
    CHEMINF_000412: URIRef
    CHEMINF_000446: URIRef
    CHEMINF_000461: URIRef
    CHEMINF_000477: URIRef
    CHEMINF_000478: URIRef
    CHEMINF_000480: URIRef
    CHEMINF_000482: URIRef
    CHEMINF_000561: URIRef

    SIO_000008: URIRef
    SIO_000011: URIRef
    SIO_000300: URIRef


class CHEMINF:
    """The SEMSCI's CHEMINF namespace.

    See <http://doi.org/10.1186/s13321-015-0084-4>.
    """
    canonical_smiles_generated_by_OEChem = SEMSCI.CHEMINF_000376
    CAS_registry_number = SEMSCI.CHEMINF_000446
    ChEBI_identifier = SEMSCI.CHEMINF_000407
    ChEMBL_identifier = SEMSCI.CHEMINF_000412
    drug_trade_name = SEMSCI.CHEMINF_000561
    exact_mass_calculated_by_pubchem_software_library = SEMSCI.CHEMINF_000338
    has_component = SEMSCI.CHEMINF_000478
    has_component_with_uncharged_counterpart = SEMSCI.CHEMINF_000480
    has_PubChem_normalized_counterpart = SEMSCI.CHEMINF_000477
    InChI_calculated_by_library_version_1_0_4 = SEMSCI.CHEMINF_000396
    InChIKey_generated_by_software_version_1_0_4 = SEMSCI.CHEMINF_000399
    is_stereoisomer_of = SEMSCI.CHEMINF_000461
    isomeric_SMILES_generated_by_OEChem = SEMSCI.CHEMINF_000379
    isotope_atom_count_generated_by_pubchem_software_library = SEMSCI.CHEMINF_000372
    IUPAC_Name_generated_by_LexiChem = SEMSCI.CHEMINF_000382
    molecular_formula_calculated_by_the_pubchem_software_library = SEMSCI.CHEMINF_000335
    molecular_weight_calculated_by_the_pubchem_software_library = SEMSCI.CHEMINF_000334
    PubChem_compound_identifier_CID = SEMSCI.CHEMINF_000140
    pubchem_depositor_supplied_molecular_entity_name = SEMSCI.CHEMINF_000339
    similar_to_by_PubChem_2D_similarity_algorithm = SEMSCI.CHEMINF_000482
    structure_complexity_calculated_by_cactvs = SEMSCI.CHEMINF_000390
    xlogp3_calculated_by_the_xlogp3_software = SEMSCI.CHEMINF_000395


class SIO:
    """The SEMSCI's SIO namespace."""
    has_attribute = SEMSCI.SIO_000008
    has_value = SEMSCI.SIO_000300
    is_attribute_of = SEMSCI.SIO_000011

# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import DefinedNamespace, Namespace, URIRef
from ..typing import Final


class UNIPROT(DefinedNamespace):
    """UniProt RDF schema ontology.

    See <https://purl.uniprot.org/html/index-en.html#>.
    """

    _NS = Namespace('http://purl.uniprot.org/core/')

    Taxon: URIRef
    Taxonomic_Rank_Biotype: URIRef
    Taxonomic_Rank_Class: URIRef
    Taxonomic_Rank_Cohort: URIRef
    Taxonomic_Rank_Domain: URIRef
    Taxonomic_Rank_Family: URIRef
    Taxonomic_Rank_Forma: URIRef
    Taxonomic_Rank_Forma_Specialis: URIRef
    Taxonomic_Rank_Genotype: URIRef
    Taxonomic_Rank_Genus: URIRef
    Taxonomic_Rank_Infraclass: URIRef
    Taxonomic_Rank_Infraorder: URIRef
    Taxonomic_Rank_Isolate: URIRef
    Taxonomic_Rank_Kingdom: URIRef
    Taxonomic_Rank_Morph: URIRef
    Taxonomic_Rank_Order: URIRef
    Taxonomic_Rank_Parvorder: URIRef
    Taxonomic_Rank_Pathogroup: URIRef
    Taxonomic_Rank_Phylum: URIRef
    Taxonomic_Rank_Realm: URIRef
    Taxonomic_Rank_Serogroup: URIRef
    Taxonomic_Rank_Serotype: URIRef
    Taxonomic_Rank_Species: URIRef
    Taxonomic_Rank_Species_Group: URIRef
    Taxonomic_Rank_Species_Subgroup: URIRef
    Taxonomic_Rank_Strain: URIRef
    Taxonomic_Rank_Subclass: URIRef
    Taxonomic_Rank_Subcohort: URIRef
    Taxonomic_Rank_Subfamily: URIRef
    Taxonomic_Rank_Subgenus: URIRef
    Taxonomic_Rank_Subkingdom: URIRef
    Taxonomic_Rank_Suborder: URIRef
    Taxonomic_Rank_Subphylum: URIRef
    Taxonomic_Rank_Subspecies: URIRef
    Taxonomic_Rank_Subtribe: URIRef
    Taxonomic_Rank_Subvarietas: URIRef
    Taxonomic_Rank_Superclass: URIRef
    Taxonomic_Rank_Superfamily: URIRef
    Taxonomic_Rank_Superorder: URIRef
    Taxonomic_Rank_Superphylum: URIRef
    Taxonomic_Rank_Tribe: URIRef
    Taxonomic_Rank_Varietas: URIRef

    otherName: URIRef
    rank: URIRef
    scientificName: URIRef


class UniProt(Namespace):
    """The UniProt namespace."""

    TAXONOMY: Final[Namespace] = Namespace('http://purl.uniprot.org/taxonomy/')

    namespaces: Final[dict[str, Namespace]] = {
        str(TAXONOMY): TAXONOMY,
    }

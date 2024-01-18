# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing import Optional

from ..model import Entity
from .registry import WikidataEntityRegistry

_registry = WikidataEntityRegistry()
Q = _registry.Q  # type: ignore
P = _registry.P  # type: ignore
L = _registry.L  # type: ignore


def get_entity_label(entity: Entity) -> Optional[str]:
    return _registry.get(entity, 'label')


def get_entity_description(entity: Entity) -> Optional[str]:
    return _registry.get(entity, 'description')

# autopep8: off
# flake8: noqa

# items
Adam = Q(70899, 'Adam')
aromatic_hydrocarbon = Q(230731, 'aromatic hydrocarbon')
Atlantic_Ocean = Q(97, 'Atlantic Ocean')
autobahn_in_Germany = Q(313301, 'autobahn in Germany')
benzene = Q(2270, 'benzene')
Brazil = Q(155, 'Brazil')
Brazilian_Sign_Language = Q(3436689, 'Brazilian Sign Language')
CAS_Common_Chemistry = Q(18907859, 'CAS Common Chemistry')
chemical_compound = Q(11173, 'chemical compound')
chemical_entity = Q(43460564, 'chemical entity')
ChemIDplus = Q(20593, 'ChemIDplus')
ChemSpider = Q(2311683, 'ChemSpider')
continent_ = Q(5107, 'continent')
country_ = Q(6256, 'country')
dalton = Q(483261, 'dalton')
degree_Celsius = Q(25267, 'degree Celsius')
degree_Fahrenheit = Q(42289, 'degree Fahrenheit')
dopamine = Q(170304, 'dopamine')
ECHA_Substance_Infocard_database = Q(59911453, 'ECHA Substance Infocard database')
electronvolt = Q(83327, 'electronvolt')
English = Q(1860, 'English')
English_Wikipedia = Q(328, 'English Wikipedia')
Eve = Q(830183, 'Eve')
exact_match = Q(39893449, 'exact match')
feminine = Q(1775415, 'feminine')
Garden_of_Eden = Q(19014, 'Garden of Eden')
Germany = Q(183, 'Germany')
Global_Substance_Registration_System = Q(116031405, 'Global Substance Registration System')
gram_per_100_gram_of_solvent = Q(21127659, 'gram per 100 gram of solvent')
gram_per_cubic_centimetre = Q(13147228, 'gram per cubic centimetre')
gram_per_mole = Q(28924752, 'gram per mole')
Hazardous_Substances_Data_Bank = Q(5687720, 'Hazardous Substances Data Bank')
human = Q(5, 'human')
inhalation = Q(840343, 'inhalation')
intravenous_infusion_and_defusion = Q(640448, 'intravenous infusion and defusion') 
joule_per_mole_kelvin_difference = Q(69427692, 'joule per mole kelvin difference')
kelvin = Q(11579, 'kelvin')
kilogram = Q(11570, 'kilogram')
kind_of_quantity = Q(110653654, 'kind of quantity')
laboratory_rat = Q(3089676, 'laboratory rat')
Latin_America = Q(12585, 'Latin America')
lion = Q(140, 'lion')
liquid = Q(11435, 'liquid')
mammal = Q(7377, 'mammal')
masculine = Q(499327, 'masculine')
methanol = Q(14982, 'methanol')
metre = Q(11573, 'metre')
milligram_per_kilogram = Q(21091747, 'milligram per kilogram')
minute = Q(7727, 'minute')
oral_administration = Q(285166, 'oral administration')
part = Q(15989253, 'part')
parts_per_million = Q(21006887, 'parts per million')
patent = Q(253623, 'patent')
Pico_da_Neblina = Q(739484, 'Pico da Neblina')
Portuguese = Q(5146, 'Portuguese')
proleptic_Gregorian_calendar = Q(1985727, 'proleptic Gregorian calendar')
proleptic_Julian_calendar = Q(1985786, 'proleptic Julian calendar')
PubChem = Q(278487, 'PubChem')
rabbit = Q(9394, 'rabbit')
report = Q(10870555, 'report')
second = Q(11574, 'second')
South_America = Q(18, 'South America')
Supercalifragilisticexpialidocious = Q(103, 'Supercalifragilisticexpialidocious')
type_of_a_chemical_entity = Q(113145171, 'type of a chemical entity')
unit_of_mass = Q(3647172, 'unit of mass')
water = Q(283, 'water')
Wikidata = Q(2013, 'Wikidata')
Wikidata_property_for_physical_quantities = Q(21077852, 'Wikidata property for physical quantities') 
Wikidata_property_related_to_medicine = Q(19887775, 'Wikidata property related to medicine')
Wikidata_property_to_identify_substances = Q(19833835, 'Wikidata property to identify substances')

# properties
afflicts = P(689)
applies_to_part = P(518)
assessment = P(5021)
author_name_string = P(2093)
canonical_SMILES = P(233)
CAS_Registry_Number = P(231)
ChEBI_ID = P(683)
chemical_structure = P(117)
continent = P(30)
country = P(17)
country_of_citizenship = P(27)
date_of_birth = P(569)
date_of_death = P(570)
demonym = P(1549)
density = P(2054)
described_by_source = P(1343)
duration = P(2047)
elevation_above_sea_level = P(2044)
end_time = P(582)
exact_match = Q(39893449)
family_name = P(734)
father = P(22)
highest_point = P(610)
HSDB_ID = P(2062)
imported_from_Wikimedia_project = P(143)
inception = P(571)
InChI = P(234)
InChIKey = P(235)
instance_of = P(31)
ionization_energy = P(2260)
language_of_work_or_name = P(407)
lowest_point = P(1589)
main_subject = P(921)
mass = P(2067)
median_lethal_dose = P(2240)
member_of = P(463)
minimal_lethal_dose = P(2300)
mother = P(25)
official_language = P(37)
official_name = P(1448)
part_of = P(361)
patent_number = P(1246)
phase_of_matter = P(515)
place_of_birth = P(19)
position_held = P(39)
PubChem_CID = P(662)
publication_date = P(577)
reference_URL = P(854)
related_property = P(1659)
retrieved = P(813)
route_of_administration = P(636)
safety_classification_and_labelling = P(4952)
solubility = P(2177)
specific_heat_capacity = P(2056)
speed_limit = P(3086)
sponsor = P(859)
spouse = P(26)
start_time = P(580)
stated_in = P(248)
statement_supported_by = P(3680)
subclass_of = P(279)
temperature = P(2076)
time_index = P(4895)
title = P(1476)
type_of_unit_for_this_property = P(2876)
valid_in_place = P(3005)
Wikidata_item_of_this_property = P(1629)
Wikidata_property = P(1687)
YouTube_video_ID = P(1651)

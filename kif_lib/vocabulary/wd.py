# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..model import Entity
from ..typing import Optional
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
business = Q(4830453, 'business')
CAS_Common_Chemistry = Q(18907859, 'CAS Common Chemistry')
characterization = Q(2165586, 'characterization')
chemical_compound = Q(11173, 'chemical compound')
chemical_entity = Q(43460564, 'chemical entity')
ChemIDplus = Q(20593, 'ChemIDplus')
ChemSpider = Q(2311683, 'ChemSpider')
child = Q(7569, 'child')
comma_separated_values = Q(935809, 'comma-separated values')
continent_ = Q(5107, 'continent')
country_ = Q(6256, 'country')
dalton = Q(483261, 'dalton')
data_set = Q(1172284, 'data set')
degree_Celsius = Q(25267, 'degree Celsius')
degree_Fahrenheit = Q(42289, 'degree Fahrenheit')
dog = Q(144, 'dog')
dopamine = Q(170304, 'dopamine')
ECHA_Substance_Infocard_database = Q(59911453, 'ECHA Substance Infocard database')
electronvolt = Q(83327, 'electronvolt')
English = Q(1860, 'English')
English_Wikipedia = Q(328, 'English Wikipedia')
Eve = Q(830183, 'Eve')
exact_match = Q(39893449, 'exact match')
FDA_approved = Q(111972129, 'FDA-approved')
female_human = Q(84048852, 'female human')
feminine = Q(1775415, 'feminine')
flame_retardant = Q(902863, 'flame retardant')
frog = Q(3116510, 'frog')
Garden_of_Eden = Q(19014, 'Garden of Eden')
Germany = Q(183, 'Germany')
Global_Substance_Registration_System = Q(116031405, 'Global Substance Registration System')
gram_per_100_gram_of_solvent = Q(21127659, 'gram per 100 gram of solvent')
gram_per_cubic_centimetre = Q(13147228, 'gram per cubic centimetre')
gram_per_kilogram = Q(21061369, 'gram per kilogram')
gram_per_mole = Q(28924752, 'gram per mole')
Guinea_pig = Q(286088, 'Guinea pig')
Hazardous_Substances_Data_Bank = Q(5687720, 'Hazardous Substances Data Bank')
human = Q(5, 'human')
IBM = Q(37156, 'IBM')
infant = Q(998, 'infant')
inhalation = Q(840343, 'inhalation')
intraperitoneal_injection = Q(1400536, 'intraperitoneal injection')
intravenous_infusion_and_defusion = Q(640448, 'intravenous infusion and defusion') 
intravenous_injection = Q(1369403, 'intravenous injection')
joule_per_mole_kelvin_difference = Q(69427692, 'joule per mole kelvin difference')
kelvin = Q(11579, 'kelvin')
kilogram = Q(11570, 'kilogram')
kind_of_quantity = Q(110653654, 'kind of quantity')
laboratory_mouse = Q(2842787, 'laboratory mouse')
laboratory_rat = Q(3089676, 'laboratory rat')
Latin_America = Q(12585, 'Latin America')
lion = Q(140, 'lion')
liquid = Q(11435, 'liquid')
machine_learning = Q(2539, 'machine learning')
male_human = Q(84048850, 'male human')
mammal = Q(7377, 'mammal')
man = Q(8441, 'man')
masculine = Q(499327, 'masculine')
methanol = Q(14982, 'methanol')
metre = Q(11573, 'metre')
microgram_per_kilogram = Q(107313731, 'microgram per kilogram')
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
rectal_administration = Q(419892, 'rectal administration')
report = Q(10870555, 'report')
second = Q(11574, 'second')
skin_absorption = Q(4669896, 'skin absorption')
sodium_bicarbonate = Q(179731, 'sodium bicarbonate')
South_America = Q(18, 'South America')
subcutaneous_injection = Q(2035485, 'subcutaneous injection')
Supercalifragilisticexpialidocious = Q(103, 'Supercalifragilisticexpialidocious')
type_of_a_chemical_entity = Q(113145171, 'type of a chemical entity')
unit_of_mass = Q(3647172, 'unit of mass')
verb = Q(24905, 'verb')
water = Q(283, 'water')
Wikidata = Q(2013, 'Wikidata')
Wikidata_property_for_physical_quantities = Q(21077852, 'Wikidata property for physical quantities') 
Wikidata_property_related_to_chemistry = Q(21294996, 'Wikidata property related to chemistry')
Wikidata_property_related_to_medicine = Q(19887775, 'Wikidata property related to medicine')
Wikidata_property_to_identify_substances = Q(19833835, 'Wikidata property to identify substances')
woman = Q(467, 'woman')


# properties
afflicts = P(689)
applies_to_part = P(518)
assessment = P(5021)
author_name_string = P(2093)
based_on_heuristic = P(887)
canonical_SMILES = P(233)
CAS_Registry_Number = P(231)
CAS_Registry_Number = P(231)
ChEBI_ID = P(683)
ChEMBL_ID = P(592)
chemical_formula = P(274)
chemical_structure = P(117)
contains = P(4330)
continent = P(30)
country = P(17)
country_of_citizenship = P(27)
date_of_birth = P(569)
date_of_death = P(570)
demonym = P(1549)
density = P(2054)
described_at_URL = P(973)
described_by_source = P(1343)
download_link = P(4945)
duration = P(2047)
elevation_above_sea_level = P(2044)
end_time = P(582)
exact_match = Q(39893449)
family_name = P(734)
father = P(22)
file_format = P(2701)
has_effect = P(1542)
has_part = P(527)
has_use = P(366)
highest_point = P(610)
HSDB_ID = P(2062)
imported_from_Wikimedia_project = P(143)
inception = P(571)
InChI = P(234)
InChIKey = P(235)
instance_of = P(31)
ionization_energy = P(2260)
isomeric_SMILES = P(2017)
language_of_work_or_name = P(407)
legal_status = P(3493)
lowest_point = P(1589)
main_subject = P(921)
manufacturer = P(176)
mass = P(2067)
median_lethal_dose = P(2240)
member_of = P(463)
minimal_lethal_dose = P(2300)
mother = P(25)
name_in_native_language = P(1559)
official_language = P(37)
official_name = P(1448)
official_website = P(856)
part_of = P(361)
partition_coefficient_water_octanol = P(2993)
patent_number = P(1246)
phase_of_matter = P(515)
pKa = P(1117)
place_of_birth = P(19)
position_held = P(39)
PubChem_CID = P(662)
publication_date = P(577)
reference_URL = P(854)
related_property = P(1659)
retrieved = P(813)
route_of_administration = P(636)
safety_classification_and_labelling = P(4952)
short_name = P(1813)
solubility = P(2177)
specific_heat_capacity = P(2056)
speed_limit = P(3086)
sponsor = P(859)
spouse = P(26)
start_time = P(580)
stated_in = P(248)
statement_supported_by = P(3680)
stereoisomer_of = P(3364)
subclass_of = P(279)
subproperty_of = P(1647)
temperature = P(2076)
time_index = P(4895)
title = P(1476)
trading_name = P(6427)
type_of_unit_for_this_property = P(2876)
valid_in_place = P(3005)
Wikidata_item_of_this_property = P(1629)
Wikidata_property = P(1687)
YouTube_video_ID = P(1651)

# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# $Id$
#
# ** GENERATED FILE: DO NOT EDIT! **

from __future__ import annotations

from ...model import (
    ExternalIdDatatype,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    LexemeDatatype,
    Property,
    PropertyDatatype,
    QuantityDatatype,
    StringDatatype,
    Text,
    TextDatatype,
    TimeDatatype,
)

# pyright: ignore
# autopep8: off
# flake8: noqa

_1st_carry = Property(IRI('https://database.factgrid.de/entity/P546'), QuantityDatatype()).register(labels=[Text('1st carry', 'en')], range=QuantityDatatype())
_2nd_carry = Property(IRI('https://database.factgrid.de/entity/P547'), QuantityDatatype()).register(labels=[Text('2nd carry', 'en')], range=QuantityDatatype())
_2nd_Qualifier = Property(IRI('https://database.factgrid.de/entity/P913'), StringDatatype()).register(labels=[Text('2nd Qualifier', 'en')], range=StringDatatype())
_3D_model_external = Property(IRI('https://database.factgrid.de/entity/P1034'), IRI_Datatype()).register(labels=[Text('3D model  (external)', 'en')], range=IRI_Datatype())
_3D_model_Wikimadia_Commons = Property(IRI('https://database.factgrid.de/entity/P1232'), StringDatatype()).register(labels=[Text('3D model (Wikimadia Commons)', 'en')], range=StringDatatype())
Abbot = Property(IRI('https://database.factgrid.de/entity/P474'), ItemDatatype()).register(labels=[Text('Abbot', 'en')], range=ItemDatatype())
Abbreviation = Property(IRI('https://database.factgrid.de/entity/P1266'), TextDatatype()).register(labels=[Text('Abbreviation', 'en')], range=TextDatatype())
Ability = Property(IRI('https://database.factgrid.de/entity/P976'), ItemDatatype()).register(labels=[Text('Ability', 'en')], range=ItemDatatype())
Absent = Property(IRI('https://database.factgrid.de/entity/P259'), ItemDatatype()).register(labels=[Text('Absent', 'en')], range=ItemDatatype())
Accessibility = Property(IRI('https://database.factgrid.de/entity/P125'), ItemDatatype()).register(labels=[Text('Accessibility', 'en')], range=ItemDatatype())
Accession_number = Property(IRI('https://database.factgrid.de/entity/P804'), StringDatatype()).register(labels=[Text('Accession number', 'en')], range=StringDatatype())
Accounts_held_in = Property(IRI('https://database.factgrid.de/entity/P686'), ItemDatatype()).register(labels=[Text('Accounts held in', 'en')], range=ItemDatatype())
Accusation_of = Property(IRI('https://database.factgrid.de/entity/P507'), ItemDatatype()).register(labels=[Text('Accusation of', 'en')], range=ItemDatatype())
Accuser = Property(IRI('https://database.factgrid.de/entity/P1101'), ItemDatatype()).register(labels=[Text('Accuser', 'en')], range=ItemDatatype())
Acquired_name = Property(IRI('https://database.factgrid.de/entity/P56'), StringDatatype()).register(labels=[Text('Acquired name', 'en')], range=StringDatatype())
Active_ingredient = Property(IRI('https://database.factgrid.de/entity/P1270'), ItemDatatype()).register(labels=[Text('Active ingredient', 'en')], range=ItemDatatype())
Actual_statement = Property(IRI('https://database.factgrid.de/entity/P579'), ItemDatatype()).register(labels=[Text('Actual statement', 'en')], range=ItemDatatype())
Actually_addressed_to = Property(IRI('https://database.factgrid.de/entity/P27'), ItemDatatype()).register(labels=[Text('Actually addressed to', 'en')], range=ItemDatatype())
ADB_Wikisource = Property(IRI('https://database.factgrid.de/entity/P741'), ExternalIdDatatype()).register(labels=[Text('ADB (Wikisource)', 'en')], range=ExternalIdDatatype())
Additional_name_attributes = Property(IRI('https://database.factgrid.de/entity/P784'), TextDatatype()).register(labels=[Text('Additional name attributes', 'en')], range=TextDatatype())
Addressees_of_deliveries = Property(IRI('https://database.factgrid.de/entity/P1211'), ItemDatatype()).register(labels=[Text('Addressees of deliveries', 'en')], range=ItemDatatype())
Adjectivisation = Property(IRI('https://database.factgrid.de/entity/P1280'), ItemDatatype()).register(labels=[Text('Adjectivisation', 'en')], range=ItemDatatype())
Administrative_localisation = Property(IRI('https://database.factgrid.de/entity/P1069'), ItemDatatype()).register(labels=[Text('Administrative localisation', 'en')], range=ItemDatatype())
Admission_requirement_required_membership = Property(IRI('https://database.factgrid.de/entity/P863'), ItemDatatype()).register(labels=[Text('Admission requirement / required membership', 'en')], range=ItemDatatype())
Adversary = Property(IRI('https://database.factgrid.de/entity/P664'), ItemDatatype()).register(labels=[Text('Adversary', 'en')], range=ItemDatatype())
Age_from = Property(IRI('https://database.factgrid.de/entity/P866'), QuantityDatatype()).register(labels=[Text('Age from', 'en')], range=QuantityDatatype())
Age_statement = Property(IRI('https://database.factgrid.de/entity/P492'), QuantityDatatype()).register(labels=[Text('Age statement', 'en')], range=QuantityDatatype())
Age_up_to = Property(IRI('https://database.factgrid.de/entity/P867'), QuantityDatatype()).register(labels=[Text('Age up to', 'en')], range=QuantityDatatype())
Agency_or_person_that_gave_the_records = Property(IRI('https://database.factgrid.de/entity/P229'), ItemDatatype()).register(labels=[Text('Agency or person that gave the records', 'en')], range=ItemDatatype())
Agents_Agencies_involved = Property(IRI('https://database.factgrid.de/entity/P929'), ItemDatatype()).register(labels=[Text('Agents /Agencies involved', 'en')], range=ItemDatatype())
Akademie_der_Künste_Berlin_Member_ID = Property(IRI('https://database.factgrid.de/entity/P1151'), ExternalIdDatatype()).register(labels=[Text('Akademie der Künste Berlin Member ID', 'en')], range=ExternalIdDatatype())
Album_Academicum_Altorphinum_ID = Property(IRI('https://database.factgrid.de/entity/P1374'), ExternalIdDatatype()).register(labels=[Text('Album Academicum Altorphinum ID', 'en')], range=ExternalIdDatatype())
Alleged_member_of = Property(IRI('https://database.factgrid.de/entity/P455'), ItemDatatype()).register(labels=[Text('Alleged member of', 'en')], range=ItemDatatype())
Alternate_shelfmark = Property(IRI('https://database.factgrid.de/entity/P802'), StringDatatype()).register(labels=[Text('Alternate shelfmark', 'en')], range=StringDatatype())
Alternatively = Property(IRI('https://database.factgrid.de/entity/P516'), ItemDatatype()).register(labels=[Text('Alternatively', 'en')], range=ItemDatatype())
Amburger_database_ID = Property(IRI('https://database.factgrid.de/entity/P533'), ExternalIdDatatype()).register(labels=[Text('Amburger database ID', 'en')], range=ExternalIdDatatype())
Amount_in_dispute = Property(IRI('https://database.factgrid.de/entity/P1107'), QuantityDatatype()).register(labels=[Text('Amount in dispute', 'en')], range=QuantityDatatype())
Amount_of_punishment = Property(IRI('https://database.factgrid.de/entity/P1192'), QuantityDatatype()).register(labels=[Text('Amount of punishment', 'en')], range=QuantityDatatype())
Amount_of_the_penalty_payment = Property(IRI('https://database.factgrid.de/entity/P1109'), QuantityDatatype()).register(labels=[Text('Amount of the penalty payment', 'en')], range=QuantityDatatype())
Annex = Property(IRI('https://database.factgrid.de/entity/P104'), StringDatatype()).register(labels=[Text('Annex', 'en')], range=StringDatatype())
Answer_on = Property(IRI('https://database.factgrid.de/entity/P65'), ItemDatatype()).register(labels=[Text('Answer on', 'en')], range=ItemDatatype())
Answered_with = Property(IRI('https://database.factgrid.de/entity/P205'), ItemDatatype()).register(labels=[Text('Answered with', 'en')], range=ItemDatatype())
Apartment = Property(IRI('https://database.factgrid.de/entity/P886'), ItemDatatype()).register(labels=[Text('Apartment', 'en')], range=ItemDatatype())
API_endpoint_URL = Property(IRI('https://database.factgrid.de/entity/P923'), IRI_Datatype()).register(labels=[Text('API endpoint URL', 'en')], range=IRI_Datatype())
Applied_means = Property(IRI('https://database.factgrid.de/entity/P1122'), ItemDatatype()).register(labels=[Text('Applied means', 'en')], range=ItemDatatype())
Apprenticeship_at = Property(IRI('https://database.factgrid.de/entity/P330'), ItemDatatype()).register(labels=[Text('Apprenticeship at', 'en')], range=ItemDatatype())
Appropriate_clothing = Property(IRI('https://database.factgrid.de/entity/P895'), ItemDatatype()).register(labels=[Text('Appropriate clothing', 'en')], range=ItemDatatype())
Approved_by = Property(IRI('https://database.factgrid.de/entity/P729'), ItemDatatype()).register(labels=[Text('Approved by', 'en')], range=ItemDatatype())
Archaeological_Project = Property(IRI('https://database.factgrid.de/entity/P1074'), IRI_Datatype()).register(labels=[Text('Archaeological Project', 'en')], range=IRI_Datatype())
Archival_collection = Property(IRI('https://database.factgrid.de/entity/P439'), ItemDatatype()).register(labels=[Text('Archival collection', 'en')], range=ItemDatatype())
Archived_at_the_URL = Property(IRI('https://database.factgrid.de/entity/P1361'), IRI_Datatype()).register(labels=[Text('Archived at the URL', 'en')], range=IRI_Datatype())
Archives_at = Property(IRI('https://database.factgrid.de/entity/P185'), ItemDatatype()).register(labels=[Text('Archives at', 'en')], range=ItemDatatype())
Area = Property(IRI('https://database.factgrid.de/entity/P1020'), QuantityDatatype()).register(labels=[Text('Area', 'en')], range=QuantityDatatype())
Area_changes_to = Property(IRI('https://database.factgrid.de/entity/P1338'), ItemDatatype()).register(labels=[Text('Area changes to', 'en')], range=ItemDatatype())
Area_ID = Property(IRI('https://database.factgrid.de/entity/P1033'), StringDatatype()).register(labels=[Text('Area ID', 'en')], range=StringDatatype())
Aristocratic_tenures = Property(IRI('https://database.factgrid.de/entity/P215'), ItemDatatype()).register(labels=[Text('Aristocratic tenures', 'en')], range=ItemDatatype())
Aristocratic_title = Property(IRI('https://database.factgrid.de/entity/P26'), ItemDatatype()).register(labels=[Text('Aristocratic title', 'en')], range=ItemDatatype())
Arolsen_Archives_Document_ID = Property(IRI('https://database.factgrid.de/entity/P1375'), ExternalIdDatatype()).register(labels=[Text('Arolsen Archives Document ID', 'en')], range=ExternalIdDatatype())
Arolsen_Archives_Persons_ID = Property(IRI('https://database.factgrid.de/entity/P1207'), ExternalIdDatatype()).register(labels=[Text('Arolsen Archives Persons ID', 'en')], range=ExternalIdDatatype())
Arrival = Property(IRI('https://database.factgrid.de/entity/P996'), ItemDatatype()).register(labels=[Text('Arrival', 'en')], range=ItemDatatype())
Art_and_Architecture_Thesaurus_ID = Property(IRI('https://database.factgrid.de/entity/P710'), ExternalIdDatatype()).register(labels=[Text('Art & Architecture Thesaurus ID', 'en')], range=ExternalIdDatatype())
Article = Property(IRI('https://database.factgrid.de/entity/P98'), ItemDatatype()).register(labels=[Text('Article', 'en')], range=ItemDatatype())
Article_literal = Property(IRI('https://database.factgrid.de/entity/P1008'), StringDatatype()).register(labels=[Text('Article [literal]', 'en')], range=StringDatatype())
Asiatic_Brethren_code_name_of = Property(IRI('https://database.factgrid.de/entity/P531'), ItemDatatype()).register(labels=[Text('Asiatic Brethren code name of', 'en')], range=ItemDatatype())
Associated_person = Property(IRI('https://database.factgrid.de/entity/P1136'), StringDatatype()).register(labels=[Text('* Associated person', 'en')], range=StringDatatype())
Associated_place = Property(IRI('https://database.factgrid.de/entity/P434'), ItemDatatype()).register(labels=[Text('Associated place', 'en')], range=ItemDatatype())
Authenticated_by = Property(IRI('https://database.factgrid.de/entity/P734'), ItemDatatype()).register(labels=[Text('Authenticated by', 'en')], range=ItemDatatype())
Authenticity_of_the_document_confirmed_by = Property(IRI('https://database.factgrid.de/entity/P928'), ItemDatatype()).register(labels=[Text('Authenticity of the document confirmed by', 'en')], range=ItemDatatype())
Author = Property(IRI('https://database.factgrid.de/entity/P21'), ItemDatatype()).register(labels=[Text('Author', 'en')], range=ItemDatatype())
Author_as_strangely_stated = Property(IRI('https://database.factgrid.de/entity/P20'), ItemDatatype()).register(labels=[Text('Author as strangely stated', 'en')], range=ItemDatatype())
Autobiography_diaries = Property(IRI('https://database.factgrid.de/entity/P244'), ItemDatatype()).register(labels=[Text('Autobiography / diaries', 'en')], range=ItemDatatype())
Average = Property(IRI('https://database.factgrid.de/entity/P955'), QuantityDatatype()).register(labels=[Text('Average', 'en')], range=QuantityDatatype())
BAG_code_for_Dutch_places_of_residence = Property(IRI('https://database.factgrid.de/entity/P1352'), ExternalIdDatatype()).register(labels=[Text('BAG code for Dutch places of residence', 'en')], range=ExternalIdDatatype())
Ballots_cast = Property(IRI('https://database.factgrid.de/entity/P1310'), QuantityDatatype()).register(labels=[Text('Ballots cast', 'en')], range=QuantityDatatype())
Banns_of_marriage_date = Property(IRI('https://database.factgrid.de/entity/P1079'), TimeDatatype()).register(labels=[Text('Banns of marriage, date', 'en')], range=TimeDatatype())
Barcode = Property(IRI('https://database.factgrid.de/entity/P805'), StringDatatype()).register(labels=[Text('Barcode', 'en')], range=StringDatatype())
BARTOC_Vocabularies_ID = Property(IRI('https://database.factgrid.de/entity/P932'), ExternalIdDatatype()).register(labels=[Text('BARTOC Vocabularies ID', 'en')], range=ExternalIdDatatype())
Based_on = Property(IRI('https://database.factgrid.de/entity/P702'), ItemDatatype()).register(labels=[Text('Based on', 'en')], range=ItemDatatype())
Bavarikon_ID = Property(IRI('https://database.factgrid.de/entity/P1226'), ExternalIdDatatype()).register(labels=[Text('Bavarikon ID', 'en')], range=ExternalIdDatatype())
Bayrisches_Musiker_Lexikon_Online_ID = Property(IRI('https://database.factgrid.de/entity/P1333'), ExternalIdDatatype()).register(labels=[Text('Bayrisches Musiker-Lexikon Online-ID', 'en')], range=ExternalIdDatatype())
BDTNS_ID = Property(IRI('https://database.factgrid.de/entity/P959'), ExternalIdDatatype()).register(labels=[Text('BDTNS ID', 'en')], range=ExternalIdDatatype())
Bearer = Property(IRI('https://database.factgrid.de/entity/P732'), ItemDatatype()).register(labels=[Text('Bearer', 'en')], range=ItemDatatype())
Bearer_of_the_Coat_of_Arms = Property(IRI('https://database.factgrid.de/entity/P1316'), ItemDatatype()).register(labels=[Text('Bearer of the Coat of Arms', 'en')], range=ItemDatatype())
Begin_date = Property(IRI('https://database.factgrid.de/entity/P49'), TimeDatatype()).register(labels=[Text('Begin date', 'en')], range=TimeDatatype())
Begin_date_terminus_ante_quem = Property(IRI('https://database.factgrid.de/entity/P1124'), TimeDatatype()).register(labels=[Text('Begin date (terminus ante quem)', 'en')], range=TimeDatatype())
Begin_date_terminus_post_quem = Property(IRI('https://database.factgrid.de/entity/P1126'), TimeDatatype()).register(labels=[Text('Begin date (terminus post quem)', 'en')], range=TimeDatatype())
Begin_text_span = Property(IRI('https://database.factgrid.de/entity/P1208'), StringDatatype()).register(labels=[Text('Begin text span', 'en')], range=StringDatatype())
Beginning_of_composition = Property(IRI('https://database.factgrid.de/entity/P39'), TimeDatatype()).register(labels=[Text('Beginning of composition', 'en')], range=TimeDatatype())
Best_practice_notice = Property(IRI('https://database.factgrid.de/entity/P598'), TextDatatype()).register(labels=[Text('Best practice notice', 'en')], range=TextDatatype())
Bestellnummer_of_books_printed_in_the_GDR = Property(IRI('https://database.factgrid.de/entity/P1092'), StringDatatype()).register(labels=[Text('Bestellnummer (of books printed in the GDR)', 'en')], range=StringDatatype())
Binding = Property(IRI('https://database.factgrid.de/entity/P800'), StringDatatype()).register(labels=[Text('* Binding', 'en')], range=StringDatatype())
Biographical_notes = Property(IRI('https://database.factgrid.de/entity/P173'), StringDatatype()).register(labels=[Text('Biographical notes', 'en')], range=StringDatatype())
Biographisches_Portal_der_Rabbiner_ID = Property(IRI('https://database.factgrid.de/entity/P1390'), ExternalIdDatatype()).register(labels=[Text('Biographisches Portal der Rabbiner ID', 'en')], range=ExternalIdDatatype())
Blood_type = Property(IRI('https://database.factgrid.de/entity/P641'), ItemDatatype()).register(labels=[Text('Blood type', 'en')], range=ItemDatatype())
Blueness_of_the_sky = Property(IRI('https://database.factgrid.de/entity/P777'), ItemDatatype()).register(labels=[Text('Blueness of the sky', 'en')], range=ItemDatatype())
BNE_ID = Property(IRI('https://database.factgrid.de/entity/P652'), ExternalIdDatatype()).register(labels=[Text('BNE-ID', 'en')], range=ExternalIdDatatype())
BnF_ID = Property(IRI('https://database.factgrid.de/entity/P367'), ExternalIdDatatype()).register(labels=[Text('BnF ID', 'en')], range=ExternalIdDatatype())
Body_form = Property(IRI('https://database.factgrid.de/entity/P1396'), ItemDatatype()).register(labels=[Text('Body form', 'en')], range=ItemDatatype())
Bookbinding = Property(IRI('https://database.factgrid.de/entity/P916'), ItemDatatype()).register(labels=[Text('Bookbinding', 'en')], range=ItemDatatype())
Bookbinding_by = Property(IRI('https://database.factgrid.de/entity/P318'), ItemDatatype()).register(labels=[Text('Bookbinding by', 'en')], range=ItemDatatype())
Bossu_ID = Property(IRI('https://database.factgrid.de/entity/P610'), ExternalIdDatatype()).register(labels=[Text('Bossu ID', 'en')], range=ExternalIdDatatype())
Buchenwald_satellite_camp_ID = Property(IRI('https://database.factgrid.de/entity/P1325'), ExternalIdDatatype()).register(labels=[Text('Buchenwald satellite camp ID', 'en')], range=ExternalIdDatatype())
Building_history = Property(IRI('https://database.factgrid.de/entity/P281'), ItemDatatype()).register(labels=[Text('Building history', 'en')], range=ItemDatatype())
Business_partner_of = Property(IRI('https://database.factgrid.de/entity/P776'), ItemDatatype()).register(labels=[Text('Business partner of', 'en')], range=ItemDatatype())
Can_mean = Property(IRI('https://database.factgrid.de/entity/P110'), ItemDatatype()).register(labels=[Text('Can mean', 'en')], range=ItemDatatype())
Canonization_status = Property(IRI('https://database.factgrid.de/entity/P1147'), ItemDatatype()).register(labels=[Text('Canonization status', 'en')], range=ItemDatatype())
Capacity = Property(IRI('https://database.factgrid.de/entity/P717'), QuantityDatatype()).register(labels=[Text('Capacity', 'en')], range=QuantityDatatype())
Capital = Property(IRI('https://database.factgrid.de/entity/P465'), ItemDatatype()).register(labels=[Text('Capital', 'en')], range=ItemDatatype())
Capital_burden = Property(IRI('https://database.factgrid.de/entity/P1014'), QuantityDatatype()).register(labels=[Text('Capital burden', 'en')], range=QuantityDatatype())
Capital_of = Property(IRI('https://database.factgrid.de/entity/P466'), ItemDatatype()).register(labels=[Text('Capital of', 'en')], range=ItemDatatype())
Capital_return_of_the_property = Property(IRI('https://database.factgrid.de/entity/P1019'), QuantityDatatype()).register(labels=[Text('Capital return of the property', 'en')], range=QuantityDatatype())
Career_aspiration = Property(IRI('https://database.factgrid.de/entity/P1260'), ItemDatatype()).register(labels=[Text('Career aspiration', 'en')], range=ItemDatatype())
Career_statement = Property(IRI('https://database.factgrid.de/entity/P165'), ItemDatatype()).register(labels=[Text('Career statement', 'en')], range=ItemDatatype())
CARLA_ID = Property(IRI('https://database.factgrid.de/entity/P1233'), ExternalIdDatatype()).register(labels=[Text('CARLA ID', 'en')], range=ExternalIdDatatype())
Catalogus_Professorum_Dresdensis_ID = Property(IRI('https://database.factgrid.de/entity/P1385'), ExternalIdDatatype()).register(labels=[Text('Catalogus Professorum Dresdensis ID', 'en')], range=ExternalIdDatatype())
Catalogus_Professorum_Halensis_ID = Property(IRI('https://database.factgrid.de/entity/P1055'), ExternalIdDatatype()).register(labels=[Text('Catalogus Professorum Halensis ID', 'en')], range=ExternalIdDatatype())
Catalogus_Professorum_Hamburgensis_ID = Property(IRI('https://database.factgrid.de/entity/P1387'), ExternalIdDatatype()).register(labels=[Text('Catalogus Professorum Hamburgensis ID', 'en')], range=ExternalIdDatatype())
Catholic_Hierarchy_ID = Property(IRI('https://database.factgrid.de/entity/P462'), ExternalIdDatatype()).register(labels=[Text('Catholic Hierarchy ID', 'en')], range=ExternalIdDatatype())
Catholic_religious_name = Property(IRI('https://database.factgrid.de/entity/P302'), ItemDatatype()).register(labels=[Text('Catholic religious name', 'en')], range=ItemDatatype())
Catholic_religious_name_of = Property(IRI('https://database.factgrid.de/entity/P373'), ItemDatatype()).register(labels=[Text('Catholic religious name of', 'en')], range=ItemDatatype())
Cause_of_end = Property(IRI('https://database.factgrid.de/entity/P506'), ItemDatatype()).register(labels=[Text('Cause of end', 'en')], range=ItemDatatype())
Cause_of_loss = Property(IRI('https://database.factgrid.de/entity/P347'), ItemDatatype()).register(labels=[Text('Cause of loss', 'en')], range=ItemDatatype())
CDLI_ID = Property(IRI('https://database.factgrid.de/entity/P692'), ExternalIdDatatype()).register(labels=[Text('CDLI ID', 'en')], range=ExternalIdDatatype())
CDLI_ID2 = Property(IRI('https://database.factgrid.de/entity/P694'), ExternalIdDatatype()).register(labels=[Text('CDLI ID2', 'en')], range=ExternalIdDatatype())
Celebrating = Property(IRI('https://database.factgrid.de/entity/P935'), ItemDatatype()).register(labels=[Text('Celebrating', 'en')], range=ItemDatatype())
CERL_Thesaurus_ID = Property(IRI('https://database.factgrid.de/entity/P537'), ExternalIdDatatype()).register(labels=[Text('CERL Thesaurus ID', 'en')], range=ExternalIdDatatype())
Check = Property(IRI('https://database.factgrid.de/entity/P856'), ItemDatatype()).register(labels=[Text('Check', 'en')], range=ItemDatatype())
Chemical_formula = Property(IRI('https://database.factgrid.de/entity/P954'), StringDatatype()).register(labels=[Text('Chemical formula', 'en')], range=StringDatatype())
Child = Property(IRI('https://database.factgrid.de/entity/P150'), ItemDatatype()).register(labels=[Text('Child', 'en')], range=ItemDatatype())
Child_raised = Property(IRI('https://database.factgrid.de/entity/P257'), ItemDatatype()).register(labels=[Text('Child raised', 'en')], range=ItemDatatype())
Choice_of_title_in_Prozent = Property(IRI('https://database.factgrid.de/entity/P1311'), QuantityDatatype()).register(labels=[Text('Choice of title (in Prozent)', 'en')], range=QuantityDatatype())
Chronology = Property(IRI('https://database.factgrid.de/entity/P1350'), TimeDatatype()).register(labels=[Text('Chronology', 'en')], range=TimeDatatype())
CIDOC_CRM_class = Property(IRI('https://database.factgrid.de/entity/P1317'), ItemDatatype()).register(labels=[Text('CIDOC CRM class', 'en')], range=ItemDatatype())
CIDOC_CRM_property = Property(IRI('https://database.factgrid.de/entity/P1318'), ExternalIdDatatype()).register(labels=[Text('CIDOC CRM property', 'en')], range=ExternalIdDatatype())
Circumcision_Date_religious = Property(IRI('https://database.factgrid.de/entity/P1060'), TimeDatatype()).register(labels=[Text('Circumcision Date (religious)', 'en')], range=TimeDatatype())
Circumstances_of_death = Property(IRI('https://database.factgrid.de/entity/P885'), ItemDatatype()).register(labels=[Text('Circumstances of death', 'en')], range=ItemDatatype())
Cite_as = Property(IRI('https://database.factgrid.de/entity/P950'), TextDatatype()).register(labels=[Text('Cite as', 'en')], range=TextDatatype())
Citizen_of = Property(IRI('https://database.factgrid.de/entity/P617'), ItemDatatype()).register(labels=[Text('Citizen of', 'en')], range=ItemDatatype())
City_Wiki_Dresden_ID = Property(IRI('https://database.factgrid.de/entity/P1327'), ExternalIdDatatype()).register(labels=[Text('City Wiki Dresden ID', 'en')], range=ExternalIdDatatype())
Claimbase_ID = Property(IRI('https://database.factgrid.de/entity/P1341'), ExternalIdDatatype()).register(labels=[Text('Claimbase ID', 'en')], range=ExternalIdDatatype())
Classification_by = Property(IRI('https://database.factgrid.de/entity/P1399'), ItemDatatype()).register(labels=[Text('Classification by', 'en')], range=ItemDatatype())
classification_of_the_data_provider = Property(IRI('https://database.factgrid.de/entity/P1300'), ItemDatatype()).register(labels=[Text('classification of the data provider', 'en')], range=ItemDatatype())
Coat_of_arms = Property(IRI('https://database.factgrid.de/entity/P725'), StringDatatype()).register(labels=[Text('Coat of arms', 'en')], range=StringDatatype())
Coat_of_arms_family = Property(IRI('https://database.factgrid.de/entity/P1383'), ItemDatatype()).register(labels=[Text('Coat of arms family', 'en')], range=ItemDatatype())
Coding_key = Property(IRI('https://database.factgrid.de/entity/P113'), ItemDatatype()).register(labels=[Text('Coding key', 'en')], range=ItemDatatype())
Coin_equivalents = Property(IRI('https://database.factgrid.de/entity/P836'), QuantityDatatype()).register(labels=[Text('Coin equivalents', 'en')], range=QuantityDatatype())
Collation = Property(IRI('https://database.factgrid.de/entity/P704'), StringDatatype()).register(labels=[Text('Collation', 'en')], range=StringDatatype())
Collected_by = Property(IRI('https://database.factgrid.de/entity/P159'), ItemDatatype()).register(labels=[Text('Collected by', 'en')], range=ItemDatatype())
Collects_information_about = Property(IRI('https://database.factgrid.de/entity/P561'), ItemDatatype()).register(labels=[Text('Collects information about', 'en')], range=ItemDatatype())
Colour = Property(IRI('https://database.factgrid.de/entity/P697'), ItemDatatype()).register(labels=[Text('Colour', 'en')], range=ItemDatatype())
Columns = Property(IRI('https://database.factgrid.de/entity/P755'), StringDatatype()).register(labels=[Text('Column(s)', 'en')], range=StringDatatype())
Commemorative_date = Property(IRI('https://database.factgrid.de/entity/P779'), TimeDatatype()).register(labels=[Text('Commemorative date', 'en')], range=TimeDatatype())
Commentator = Property(IRI('https://database.factgrid.de/entity/P730'), ItemDatatype()).register(labels=[Text('Commentator', 'en')], range=ItemDatatype())
Commissioned_by = Property(IRI('https://database.factgrid.de/entity/P273'), ItemDatatype()).register(labels=[Text('Commissioned by', 'en')], range=ItemDatatype())
Competent_Jurisdiction = Property(IRI('https://database.factgrid.de/entity/P1009'), ItemDatatype()).register(labels=[Text('Competent Jurisdiction', 'en')], range=ItemDatatype())
Complementary_term_for_the_theoretical_collective = Property(IRI('https://database.factgrid.de/entity/P1284'), ItemDatatype()).register(labels=[Text('Complementary term for the theoretical collective', 'en')], range=ItemDatatype())
Complete_Bible_Genealogy_ID = Property(IRI('https://database.factgrid.de/entity/P502'), ExternalIdDatatype()).register(labels=[Text('Complete Bible Genealogy-ID', 'en')], range=ExternalIdDatatype())
Completeness = Property(IRI('https://database.factgrid.de/entity/P900'), ItemDatatype()).register(labels=[Text('Completeness', 'en')], range=ItemDatatype())
Complex_Evaluation = Property(IRI('https://database.factgrid.de/entity/P1143'), StringDatatype()).register(labels=[Text('Complex Evaluation', 'en')], range=StringDatatype())
Composer = Property(IRI('https://database.factgrid.de/entity/P539'), ItemDatatype()).register(labels=[Text('Composer', 'en')], range=ItemDatatype())
Composite_ID = Property(IRI('https://database.factgrid.de/entity/P1083'), StringDatatype()).register(labels=[Text('Composite ID', 'en')], range=StringDatatype())
Compulsory_obligation_towards = Property(IRI('https://database.factgrid.de/entity/P1015'), ItemDatatype()).register(labels=[Text('Compulsory obligation towards', 'en')], range=ItemDatatype())
Conceptual_ramification = Property(IRI('https://database.factgrid.de/entity/P283'), ItemDatatype()).register(labels=[Text('Conceptual ramification', 'en')], range=ItemDatatype())
Conference_participations = Property(IRI('https://database.factgrid.de/entity/P349'), ItemDatatype()).register(labels=[Text('Conference participations', 'en')], range=ItemDatatype())
Confirmed_by = Property(IRI('https://database.factgrid.de/entity/P731'), ItemDatatype()).register(labels=[Text('Confirmed by', 'en')], range=ItemDatatype())
Conflict_parties = Property(IRI('https://database.factgrid.de/entity/P715'), ItemDatatype()).register(labels=[Text('Conflict parties', 'en')], range=ItemDatatype())
Connection_to_preceding = Property(IRI('https://database.factgrid.de/entity/P234'), ItemDatatype()).register(labels=[Text('Connection to preceding', 'en')], range=ItemDatatype())
Constituted_by = Property(IRI('https://database.factgrid.de/entity/P362'), ItemDatatype()).register(labels=[Text('Constituted by', 'en')], range=ItemDatatype())
constraint_scope = Property(IRI('https://database.factgrid.de/entity/P1046'), ItemDatatype()).register(labels=[Text('constraint scope', 'en')], range=ItemDatatype())
Contact_person = Property(IRI('https://database.factgrid.de/entity/P949'), ItemDatatype()).register(labels=[Text('Contact person', 'en')], range=ItemDatatype())
Contains_documents_of = Property(IRI('https://database.factgrid.de/entity/P1054'), StringDatatype()).register(labels=[Text('* Contains documents of', 'en')], range=StringDatatype())
Contains_documents_of = Property(IRI('https://database.factgrid.de/entity/P324'), ItemDatatype()).register(labels=[Text('Contains documents of', 'en')], range=ItemDatatype())
Contemporary_witness_document = Property(IRI('https://database.factgrid.de/entity/P32'), ItemDatatype()).register(labels=[Text('Contemporary witness document', 'en')], range=ItemDatatype())
contemporary_witnesses_in_the_audience = Property(IRI('https://database.factgrid.de/entity/P1291'), ItemDatatype()).register(labels=[Text('contemporary witnesses/in the audience', 'en')], range=ItemDatatype())
Context = Property(IRI('https://database.factgrid.de/entity/P437'), ItemDatatype()).register(labels=[Text('Context', 'en')], range=ItemDatatype())
Continuation_of = Property(IRI('https://database.factgrid.de/entity/P6'), ItemDatatype()).register(labels=[Text('Continuation of', 'en')], range=ItemDatatype())
Continued_by = Property(IRI('https://database.factgrid.de/entity/P7'), ItemDatatype()).register(labels=[Text('Continued by', 'en')], range=ItemDatatype())
Contributor = Property(IRI('https://database.factgrid.de/entity/P511'), ItemDatatype()).register(labels=[Text('Contributor', 'en')], range=ItemDatatype())
Contributor_to = Property(IRI('https://database.factgrid.de/entity/P649'), ItemDatatype()).register(labels=[Text('Contributor to', 'en')], range=ItemDatatype())
Conversion_rates = Property(IRI('https://database.factgrid.de/entity/P396'), QuantityDatatype()).register(labels=[Text('Conversion rate(s)', 'en')], range=QuantityDatatype())
Coordinate_location = Property(IRI('https://database.factgrid.de/entity/P48'), StringDatatype()).register(labels=[Text('Coordinate location', 'en')], range=StringDatatype())
Copy_of = Property(IRI('https://database.factgrid.de/entity/P16'), ItemDatatype()).register(labels=[Text('Copy of', 'en')], range=ItemDatatype())
Copy_of_this = Property(IRI('https://database.factgrid.de/entity/P252'), ItemDatatype()).register(labels=[Text('Copy of this', 'en')], range=ItemDatatype())
Copyright_holder = Property(IRI('https://database.factgrid.de/entity/P1303'), ItemDatatype()).register(labels=[Text('Copyright holder', 'en')], range=ItemDatatype())
Correlation = Property(IRI('https://database.factgrid.de/entity/P736'), ItemDatatype()).register(labels=[Text('Correlation', 'en')], range=ItemDatatype())
Cosignatory_in = Property(IRI('https://database.factgrid.de/entity/P167'), ItemDatatype()).register(labels=[Text('Cosignatory in', 'en')], range=ItemDatatype())
Country_of_citizenship = Property(IRI('https://database.factgrid.de/entity/P616'), ItemDatatype()).register(labels=[Text('Country of citizenship', 'en')], range=ItemDatatype())
Court_Tribunal = Property(IRI('https://database.factgrid.de/entity/P1111'), ItemDatatype()).register(labels=[Text('Court/Tribunal', 'en')], range=ItemDatatype())
Cousin = Property(IRI('https://database.factgrid.de/entity/P505'), ItemDatatype()).register(labels=[Text('Cousin', 'en')], range=ItemDatatype())
Creator = Property(IRI('https://database.factgrid.de/entity/P1134'), StringDatatype()).register(labels=[Text('* Creator', 'en')], range=StringDatatype())
Creator = Property(IRI('https://database.factgrid.de/entity/P845'), ItemDatatype()).register(labels=[Text('Creator', 'en')], range=ItemDatatype())
Credit_receiver_of = Property(IRI('https://database.factgrid.de/entity/P609'), ItemDatatype()).register(labels=[Text('Credit receiver of', 'en')], range=ItemDatatype())
CTHS_ID_person = Property(IRI('https://database.factgrid.de/entity/P656'), ExternalIdDatatype()).register(labels=[Text('CTHS ID person', 'en')], range=ExternalIdDatatype())
CTHS_ID_society = Property(IRI('https://database.factgrid.de/entity/P678'), ExternalIdDatatype()).register(labels=[Text('CTHS ID society', 'en')], range=ExternalIdDatatype())
Currency = Property(IRI('https://database.factgrid.de/entity/P1355'), ItemDatatype()).register(labels=[Text('Currency', 'en')], range=ItemDatatype())
Curriculum_Vitae = Property(IRI('https://database.factgrid.de/entity/P1131'), TimeDatatype()).register(labels=[Text('Curriculum Vitae', 'en')], range=TimeDatatype())
Customer = Property(IRI('https://database.factgrid.de/entity/P559'), ItemDatatype()).register(labels=[Text('Customer', 'en')], range=ItemDatatype())
Customer_of = Property(IRI('https://database.factgrid.de/entity/P1098'), ItemDatatype()).register(labels=[Text('Customer of', 'en')], range=ItemDatatype())
Czech_municipality_ID = Property(IRI('https://database.factgrid.de/entity/P963'), ExternalIdDatatype()).register(labels=[Text('Czech municipality ID', 'en')], range=ExternalIdDatatype())
Dachau_Memorial_Database = Property(IRI('https://database.factgrid.de/entity/P1255'), ExternalIdDatatype()).register(labels=[Text('Dachau Memorial Database', 'en')], range=ExternalIdDatatype())
Dansk_Biografisk_Leksikon_ID = Property(IRI('https://database.factgrid.de/entity/P1298'), ExternalIdDatatype()).register(labels=[Text('Dansk-Biografisk-Leksikon ID', 'en')], range=ExternalIdDatatype())
Data_BnF_ID = Property(IRI('https://database.factgrid.de/entity/P500'), ExternalIdDatatype()).register(labels=[Text('Data BnF ID', 'en')], range=ExternalIdDatatype())
Data_download_link = Property(IRI('https://database.factgrid.de/entity/P250'), IRI_Datatype()).register(labels=[Text('Data download link', 'en')], range=IRI_Datatype())
Data_format = Property(IRI('https://database.factgrid.de/entity/P903'), ItemDatatype()).register(labels=[Text('Data format', 'en')], range=ItemDatatype())
Data_set_wanting_a_statement_on = Property(IRI('https://database.factgrid.de/entity/P496'), PropertyDatatype()).register(labels=[Text('Data set wanting a statement on', 'en')], range=PropertyDatatype())
Data_size = Property(IRI('https://database.factgrid.de/entity/P1321'), QuantityDatatype()).register(labels=[Text('Data size', 'en')], range=QuantityDatatype())
database_of_Austrian_deportees_in_Auschwitz_ID = Property(IRI('https://database.factgrid.de/entity/P1188'), ExternalIdDatatype()).register(labels=[Text('database of Austrian deportees in Auschwitz ID', 'en')], range=ExternalIdDatatype())
Database_of_Salon_Artists_person_ID = Property(IRI('https://database.factgrid.de/entity/P849'), ExternalIdDatatype()).register(labels=[Text('Database of Salon Artists person ID', 'en')], range=ExternalIdDatatype())
Dataset = Property(IRI('https://database.factgrid.de/entity/P648'), ItemDatatype()).register(labels=[Text('Dataset', 'en')], range=ItemDatatype())
Dataset_complaint = Property(IRI('https://database.factgrid.de/entity/P17'), ItemDatatype()).register(labels=[Text('Dataset complaint', 'en')], range=ItemDatatype())
Dataset_editing = Property(IRI('https://database.factgrid.de/entity/P1302'), ItemDatatype()).register(labels=[Text('Dataset editing', 'en')], range=ItemDatatype())
Dataset_status = Property(IRI('https://database.factgrid.de/entity/P799'), ItemDatatype()).register(labels=[Text('Dataset status', 'en')], range=ItemDatatype())
Datatype = Property(IRI('https://database.factgrid.de/entity/P1217'), ItemDatatype()).register(labels=[Text('Datatype', 'en')], range=ItemDatatype())
Date = Property(IRI('https://database.factgrid.de/entity/P106'), TimeDatatype()).register(labels=[Text('Date', 'en')], range=TimeDatatype())
Date_after = Property(IRI('https://database.factgrid.de/entity/P41'), TimeDatatype()).register(labels=[Text('Date after', 'en')], range=TimeDatatype())
Date_as_stated = Property(IRI('https://database.factgrid.de/entity/P112'), StringDatatype()).register(labels=[Text('* Date as stated', 'en')], range=StringDatatype())
Date_as_stated = Property(IRI('https://database.factgrid.de/entity/P96'), TimeDatatype()).register(labels=[Text('Date as stated', 'en')], range=TimeDatatype())
Date_before = Property(IRI('https://database.factgrid.de/entity/P43'), TimeDatatype()).register(labels=[Text('Date before', 'en')], range=TimeDatatype())
Date_of_artifact = Property(IRI('https://database.factgrid.de/entity/P536'), TimeDatatype()).register(labels=[Text('Date of artifact', 'en')], range=TimeDatatype())
Date_of_baptism = Property(IRI('https://database.factgrid.de/entity/P37'), TimeDatatype()).register(labels=[Text('Date of baptism', 'en')], range=TimeDatatype())
Date_of_birth = Property(IRI('https://database.factgrid.de/entity/P77'), TimeDatatype()).register(labels=[Text('Date of birth', 'en')], range=TimeDatatype())
Date_of_Blessing = Property(IRI('https://database.factgrid.de/entity/P1371'), TimeDatatype()).register(labels=[Text('Date of Blessing', 'en')], range=TimeDatatype())
Date_of_burial = Property(IRI('https://database.factgrid.de/entity/P40'), TimeDatatype()).register(labels=[Text('Date of burial', 'en')], range=TimeDatatype())
Date_of_confirmation = Property(IRI('https://database.factgrid.de/entity/P182'), TimeDatatype()).register(labels=[Text('Date of confirmation', 'en')], range=TimeDatatype())
Date_of_consecration_ordination = Property(IRI('https://database.factgrid.de/entity/P321'), TimeDatatype()).register(labels=[Text('Date of consecration / ordination', 'en')], range=TimeDatatype())
Date_of_creation = Property(IRI('https://database.factgrid.de/entity/P412'), TimeDatatype()).register(labels=[Text('Date of creation', 'en')], range=TimeDatatype())
Date_of_death = Property(IRI('https://database.factgrid.de/entity/P38'), TimeDatatype()).register(labels=[Text('Date of death', 'en')], range=TimeDatatype())
Date_of_discovery_or_invention = Property(IRI('https://database.factgrid.de/entity/P303'), TimeDatatype()).register(labels=[Text('Date of discovery or invention', 'en')], range=TimeDatatype())
Date_of_disputation = Property(IRI('https://database.factgrid.de/entity/P392'), TimeDatatype()).register(labels=[Text('Date of disputation', 'en')], range=TimeDatatype())
Date_of_ennoblement = Property(IRI('https://database.factgrid.de/entity/P394'), TimeDatatype()).register(labels=[Text('Date of ennoblement', 'en')], range=TimeDatatype())
Date_of_finding = Property(IRI('https://database.factgrid.de/entity/P432'), TimeDatatype()).register(labels=[Text('Date of finding', 'en')], range=TimeDatatype())
Date_of_first_publication = Property(IRI('https://database.factgrid.de/entity/P1152'), TimeDatatype()).register(labels=[Text('Date of first publication', 'en')], range=TimeDatatype())
Date_of_last_will = Property(IRI('https://database.factgrid.de/entity/P214'), TimeDatatype()).register(labels=[Text('Date of last will', 'en')], range=TimeDatatype())
Date_of_premiere = Property(IRI('https://database.factgrid.de/entity/P551'), TimeDatatype()).register(labels=[Text('Date of premiere', 'en')], range=TimeDatatype())
Date_of_publication = Property(IRI('https://database.factgrid.de/entity/P222'), TimeDatatype()).register(labels=[Text('Date of publication', 'en')], range=TimeDatatype())
Date_of_receipt = Property(IRI('https://database.factgrid.de/entity/P44'), TimeDatatype()).register(labels=[Text('Date of receipt', 'en')], range=TimeDatatype())
Date_of_retirement = Property(IRI('https://database.factgrid.de/entity/P459'), TimeDatatype()).register(labels=[Text('Date of retirement', 'en')], range=TimeDatatype())
Date_of_verdict = Property(IRI('https://database.factgrid.de/entity/P1104'), TimeDatatype()).register(labels=[Text('Date of verdict', 'en')], range=TimeDatatype())
Daughter_lodges = Property(IRI('https://database.factgrid.de/entity/P335'), ItemDatatype()).register(labels=[Text('Daughter lodge(s)', 'en')], range=ItemDatatype())
Dedicated_day = Property(IRI('https://database.factgrid.de/entity/P266'), ItemDatatype()).register(labels=[Text('Dedicated day', 'en')], range=ItemDatatype())
Dedicatee = Property(IRI('https://database.factgrid.de/entity/P391'), ItemDatatype()).register(labels=[Text('Dedicatee', 'en')], range=ItemDatatype())
Dedicatee = Property(IRI('https://database.factgrid.de/entity/P662'), StringDatatype()).register(labels=[Text('* Dedicatee', 'en')], range=StringDatatype())
Defender = Property(IRI('https://database.factgrid.de/entity/P1113'), ItemDatatype()).register(labels=[Text('Defender', 'en')], range=ItemDatatype())
Defined_equivalent = Property(IRI('https://database.factgrid.de/entity/P835'), QuantityDatatype()).register(labels=[Text('Defined equivalent', 'en')], range=QuantityDatatype())
Definition = Property(IRI('https://database.factgrid.de/entity/P423'), TextDatatype()).register(labels=[Text('Definition', 'en')], range=TextDatatype())
Degree_system = Property(IRI('https://database.factgrid.de/entity/P357'), ItemDatatype()).register(labels=[Text('Degree system', 'en')], range=ItemDatatype())
Degree_to_which_this_is_the_case = Property(IRI('https://database.factgrid.de/entity/P284'), ItemDatatype()).register(labels=[Text('Degree to which this is the case', 'en')], range=ItemDatatype())
Degrees_worked = Property(IRI('https://database.factgrid.de/entity/P361'), ItemDatatype()).register(labels=[Text('Degrees worked', 'en')], range=ItemDatatype())
Den_Store_Danske_ID = Property(IRI('https://database.factgrid.de/entity/P1297'), ExternalIdDatatype()).register(labels=[Text('Den-Store-Danske ID', 'en')], range=ExternalIdDatatype())
Departure = Property(IRI('https://database.factgrid.de/entity/P997'), ItemDatatype()).register(labels=[Text('Departure', 'en')], range=ItemDatatype())
Deportation_extradition_to = Property(IRI('https://database.factgrid.de/entity/P1182'), ItemDatatype()).register(labels=[Text('Deportation / extradition to', 'en')], range=ItemDatatype())
Depth_thickness = Property(IRI('https://database.factgrid.de/entity/P61'), QuantityDatatype()).register(labels=[Text('Depth, thickness', 'en')], range=QuantityDatatype())
Design_features = Property(IRI('https://database.factgrid.de/entity/P575'), ItemDatatype()).register(labels=[Text('Design features', 'en')], range=ItemDatatype())
Design_planning = Property(IRI('https://database.factgrid.de/entity/P552'), ItemDatatype()).register(labels=[Text('Design / planning', 'en')], range=ItemDatatype())
Designed_to_state = Property(IRI('https://database.factgrid.de/entity/P587'), ItemDatatype()).register(labels=[Text('Designed to state', 'en')], range=ItemDatatype())
Destination = Property(IRI('https://database.factgrid.de/entity/P29'), ItemDatatype()).register(labels=[Text('Destination', 'en')], range=ItemDatatype())
Deutsche_Biographie_GND_ID = Property(IRI('https://database.factgrid.de/entity/P622'), ExternalIdDatatype()).register(labels=[Text('Deutsche Biographie (GND) ID', 'en')], range=ExternalIdDatatype())
Deutsche_Digitale_Bibliothek_Item_ID = Property(IRI('https://database.factgrid.de/entity/P924'), ExternalIdDatatype()).register(labels=[Text('Deutsche Digitale Bibliothek Item ID', 'en')], range=ExternalIdDatatype())
Deutsche_Digitale_Bibliothek_Person_ID = Property(IRI('https://database.factgrid.de/entity/P772'), ExternalIdDatatype()).register(labels=[Text('Deutsche Digitale Bibliothek Person ID', 'en')], range=ExternalIdDatatype())
Deutsche_Fotothek_object_ID = Property(IRI('https://database.factgrid.de/entity/P1202'), ExternalIdDatatype()).register(labels=[Text('Deutsche Fotothek object-ID', 'en')], range=ExternalIdDatatype())
Deutsche_Inschriften_Online_ID = Property(IRI('https://database.factgrid.de/entity/P1059'), ExternalIdDatatype()).register(labels=[Text('Deutsche Inschriften Online ID', 'en')], range=ExternalIdDatatype())
Deutsches_Literaturarchiv_Marbach_ID = Property(IRI('https://database.factgrid.de/entity/P1149'), ExternalIdDatatype()).register(labels=[Text('Deutsches Literaturarchiv Marbach ID', 'en')], range=ExternalIdDatatype())
Deutsches_Rechtswörterbuch = Property(IRI('https://database.factgrid.de/entity/P882'), ExternalIdDatatype()).register(labels=[Text('Deutsches Rechtswörterbuch', 'en')], range=ExternalIdDatatype())
Dewey_Decimal_Classification = Property(IRI('https://database.factgrid.de/entity/P1306'), ExternalIdDatatype()).register(labels=[Text('Dewey Decimal Classification', 'en')], range=ExternalIdDatatype())
DFG_subject_classification = Property(IRI('https://database.factgrid.de/entity/P1027'), ItemDatatype()).register(labels=[Text('DFG subject classification', 'en')], range=ItemDatatype())
Diameter = Property(IRI('https://database.factgrid.de/entity/P690'), QuantityDatatype()).register(labels=[Text('Diameter', 'en')], range=QuantityDatatype())
Diccionari_de_la_Literatura_Catalana_ID = Property(IRI('https://database.factgrid.de/entity/P1330'), ExternalIdDatatype()).register(labels=[Text('Diccionari de la Literatura Catalana ID', 'en')], range=ExternalIdDatatype())
Dictionary_of_Swedish_National_Biography_ID = Property(IRI('https://database.factgrid.de/entity/P377'), ExternalIdDatatype()).register(labels=[Text('Dictionary of Swedish National Biography ID', 'en')], range=ExternalIdDatatype())
Dictionnaire_des_journalistes_1600_1789_ID = Property(IRI('https://database.factgrid.de/entity/P1287'), ExternalIdDatatype()).register(labels=[Text('Dictionnaire des journalistes (1600-1789) ID', 'en')], range=ExternalIdDatatype())
Digest = Property(IRI('https://database.factgrid.de/entity/P724'), TextDatatype()).register(labels=[Text('Digest', 'en')], range=TextDatatype())
Diocese = Property(IRI('https://database.factgrid.de/entity/P1003'), ItemDatatype()).register(labels=[Text('Diocese', 'en')], range=ItemDatatype())
Discovered_invented_developed_by = Property(IRI('https://database.factgrid.de/entity/P618'), ItemDatatype()).register(labels=[Text('Discovered / invented / developed by', 'en')], range=ItemDatatype())
Dissertation = Property(IRI('https://database.factgrid.de/entity/P387'), ItemDatatype()).register(labels=[Text('Dissertation', 'en')], range=ItemDatatype())
Distance_between_addresses = Property(IRI('https://database.factgrid.de/entity/P793'), QuantityDatatype()).register(labels=[Text('Distance between addresses', 'en')], range=QuantityDatatype())
Distant_participants = Property(IRI('https://database.factgrid.de/entity/P831'), ItemDatatype()).register(labels=[Text('Distant participants', 'en')], range=ItemDatatype())
DNB_Info_ID = Property(IRI('https://database.factgrid.de/entity/P668'), ExternalIdDatatype()).register(labels=[Text('DNB-Info ID', 'en')], range=ExternalIdDatatype())
Docker_Hub_repository = Property(IRI('https://database.factgrid.de/entity/P1320'), ExternalIdDatatype()).register(labels=[Text('Docker Hub repository', 'en')], range=ExternalIdDatatype())
Doctoral_supervisor = Property(IRI('https://database.factgrid.de/entity/P145'), ItemDatatype()).register(labels=[Text('Doctoral supervisor', 'en')], range=ItemDatatype())
Document_attested_by = Property(IRI('https://database.factgrid.de/entity/P927'), ItemDatatype()).register(labels=[Text('Document attested by', 'en')], range=ItemDatatype())
Documented_list_of_members = Property(IRI('https://database.factgrid.de/entity/P327'), ItemDatatype()).register(labels=[Text('Documented list of members', 'en')], range=ItemDatatype())
Documented_object = Property(IRI('https://database.factgrid.de/entity/P371'), ItemDatatype()).register(labels=[Text('Documented object', 'en')], range=ItemDatatype())
Documented_use_case = Property(IRI('https://database.factgrid.de/entity/P938'), ItemDatatype()).register(labels=[Text('Documented use case', 'en')], range=ItemDatatype())
DOI = Property(IRI('https://database.factgrid.de/entity/P634'), ExternalIdDatatype()).register(labels=[Text('DOI', 'en')], range=ExternalIdDatatype())
Donations_received = Property(IRI('https://database.factgrid.de/entity/P1236'), QuantityDatatype()).register(labels=[Text('Donations received', 'en')], range=QuantityDatatype())
Download_link = Property(IRI('https://database.factgrid.de/entity/P1161'), IRI_Datatype()).register(labels=[Text('Download link', 'en')], range=IRI_Datatype())
Duration = Property(IRI('https://database.factgrid.de/entity/P398'), QuantityDatatype()).register(labels=[Text('Duration', 'en')], range=QuantityDatatype())
Duration_of_the_prison_sentence = Property(IRI('https://database.factgrid.de/entity/P1108'), QuantityDatatype()).register(labels=[Text('Duration of the prison sentence', 'en')], range=QuantityDatatype())
Earnings_before_interest_and_taxes = Property(IRI('https://database.factgrid.de/entity/P1237'), QuantityDatatype()).register(labels=[Text('Earnings before interest and taxes', 'en')], range=QuantityDatatype())
Ears = Property(IRI('https://database.factgrid.de/entity/P1398'), ItemDatatype()).register(labels=[Text('Ears', 'en')], range=ItemDatatype())
eBL_ID = Property(IRI('https://database.factgrid.de/entity/P1173'), ExternalIdDatatype()).register(labels=[Text('eBL ID', 'en')], range=ExternalIdDatatype())
Ecclesiastical_province = Property(IRI('https://database.factgrid.de/entity/P463'), PropertyDatatype()).register(labels=[Text('Ecclesiastical province', 'en')], range=PropertyDatatype())
Eckard_Rolf_class_of_functional_text_types = Property(IRI('https://database.factgrid.de/entity/P894'), ItemDatatype()).register(labels=[Text('Eckard Rolf class of functional text types', 'en')], range=ItemDatatype())
Economic_sector_of_the_career_statement = Property(IRI('https://database.factgrid.de/entity/P626'), ItemDatatype()).register(labels=[Text('Economic sector of the career statement', 'en')], range=ItemDatatype())
Editions_series_productions = Property(IRI('https://database.factgrid.de/entity/P839'), ItemDatatype()).register(labels=[Text('Editions / series productions', 'en')], range=ItemDatatype())
Editor_of = Property(IRI('https://database.factgrid.de/entity/P305'), ItemDatatype()).register(labels=[Text('Editor of', 'en')], range=ItemDatatype())
Editorial_responsibility = Property(IRI('https://database.factgrid.de/entity/P176'), ItemDatatype()).register(labels=[Text('Editorial responsibility', 'en')], range=ItemDatatype())
Educating_institution = Property(IRI('https://database.factgrid.de/entity/P160'), ItemDatatype()).register(labels=[Text('Educating institution', 'en')], range=ItemDatatype())
Education_level_academic_degree = Property(IRI('https://database.factgrid.de/entity/P170'), ItemDatatype()).register(labels=[Text('Education level / academic degree', 'en')], range=ItemDatatype())
Edvard_Munchs_correspondance_person_ID = Property(IRI('https://database.factgrid.de/entity/P699'), ExternalIdDatatype()).register(labels=[Text("Edvard Munch's correspondance person ID", 'en')], range=ExternalIdDatatype())
Effect_of = Property(IRI('https://database.factgrid.de/entity/P464'), ItemDatatype()).register(labels=[Text('Effect of', 'en')], range=ItemDatatype())
EHAK_ID = Property(IRI('https://database.factgrid.de/entity/P1213'), ExternalIdDatatype()).register(labels=[Text('EHAK-ID', 'en')], range=ExternalIdDatatype())
EHRI_camps_ID = Property(IRI('https://database.factgrid.de/entity/P1189'), ExternalIdDatatype()).register(labels=[Text('EHRI camps ID', 'en')], range=ExternalIdDatatype())
EHRI_ghetto_ID = Property(IRI('https://database.factgrid.de/entity/P1194'), ExternalIdDatatype()).register(labels=[Text('EHRI ghetto ID', 'en')], range=ExternalIdDatatype())
Einkaufspreis = Property(IRI('https://database.factgrid.de/entity/P1167'), QuantityDatatype()).register(labels=[Text('Einkaufspreis', 'en')], range=QuantityDatatype())
Election_results_by_candidate = Property(IRI('https://database.factgrid.de/entity/P1304'), ItemDatatype()).register(labels=[Text('Election results by candidate', 'en')], range=ItemDatatype())
Elevation_above_sea_level = Property(IRI('https://database.factgrid.de/entity/P1271'), QuantityDatatype()).register(labels=[Text('Elevation above sea level', 'en')], range=QuantityDatatype())
Eligible_voters = Property(IRI('https://database.factgrid.de/entity/P1308'), QuantityDatatype()).register(labels=[Text('Eligible voters', 'en')], range=QuantityDatatype())
Email_contact_page = Property(IRI('https://database.factgrid.de/entity/P722'), IRI_Datatype()).register(labels=[Text('Email / contact page', 'en')], range=IRI_Datatype())
Employed_at = Property(IRI('https://database.factgrid.de/entity/P315'), ItemDatatype()).register(labels=[Text('Employed at', 'en')], range=ItemDatatype())
Employers_status = Property(IRI('https://database.factgrid.de/entity/P675'), ItemDatatype()).register(labels=[Text("Employer's status", 'en')], range=ItemDatatype())
Encounter = Property(IRI('https://database.factgrid.de/entity/P231'), ItemDatatype()).register(labels=[Text('Encounter', 'en')], range=ItemDatatype())
End_date = Property(IRI('https://database.factgrid.de/entity/P50'), TimeDatatype()).register(labels=[Text('End date', 'en')], range=TimeDatatype())
End_date_terminus_ante_quem = Property(IRI('https://database.factgrid.de/entity/P1123'), TimeDatatype()).register(labels=[Text('End date (terminus ante quem)', 'en')], range=TimeDatatype())
End_date_terminus_post_quem = Property(IRI('https://database.factgrid.de/entity/P1125'), TimeDatatype()).register(labels=[Text('End date (terminus post quem)', 'en')], range=TimeDatatype())
End_of_events_reported = Property(IRI('https://database.factgrid.de/entity/P46'), TimeDatatype()).register(labels=[Text('End of events reported', 'en')], range=TimeDatatype())
End_text_span = Property(IRI('https://database.factgrid.de/entity/P1209'), StringDatatype()).register(labels=[Text('End text span', 'en')], range=StringDatatype())
Enzyklopädie_der_Russlanddeutschen_ID = Property(IRI('https://database.factgrid.de/entity/P1154'), ExternalIdDatatype()).register(labels=[Text('Enzyklopädie der Russlanddeutschen ID', 'en')], range=ExternalIdDatatype())
epidat_ID = Property(IRI('https://database.factgrid.de/entity/P1063'), ExternalIdDatatype()).register(labels=[Text('epidat ID', 'en')], range=ExternalIdDatatype())
EPN = Property(IRI('https://database.factgrid.de/entity/P1165'), ExternalIdDatatype()).register(labels=[Text('EPN', 'en')], range=ExternalIdDatatype())
Equivalent_class = Property(IRI('https://database.factgrid.de/entity/P966'), IRI_Datatype()).register(labels=[Text('Equivalent class', 'en')], range=IRI_Datatype())
Equivalent_in_grams_of_copper = Property(IRI('https://database.factgrid.de/entity/P682'), QuantityDatatype()).register(labels=[Text('Equivalent in grams of copper', 'en')], range=QuantityDatatype())
Equivalent_in_grams_of_gold = Property(IRI('https://database.factgrid.de/entity/P681'), QuantityDatatype()).register(labels=[Text('Equivalent in grams of gold', 'en')], range=QuantityDatatype())
Equivalent_in_grams_of_silver = Property(IRI('https://database.factgrid.de/entity/P680'), QuantityDatatype()).register(labels=[Text('Equivalent in grams of silver', 'en')], range=QuantityDatatype())
Equivalent_in_other_organizations = Property(IRI('https://database.factgrid.de/entity/P265'), ItemDatatype()).register(labels=[Text('Equivalent in other organizations', 'en')], range=ItemDatatype())
Equivalent_multilingual_item = Property(IRI('https://database.factgrid.de/entity/P796'), ItemDatatype()).register(labels=[Text('Equivalent multilingual item', 'en')], range=ItemDatatype())
Equivalent_property_elsewhere = Property(IRI('https://database.factgrid.de/entity/P965'), IRI_Datatype()).register(labels=[Text('Equivalent property elsewhere', 'en')], range=IRI_Datatype())
Escape_emigration_to = Property(IRI('https://database.factgrid.de/entity/P580'), ItemDatatype()).register(labels=[Text('Escape / emigration to', 'en')], range=ItemDatatype())
Espacenet_ID_for_patents = Property(IRI('https://database.factgrid.de/entity/P384'), ExternalIdDatatype()).register(labels=[Text('Espacenet ID for patents', 'en')], range=ExternalIdDatatype())
ESTC_ID = Property(IRI('https://database.factgrid.de/entity/P585'), ExternalIdDatatype()).register(labels=[Text('ESTC-ID', 'en')], range=ExternalIdDatatype())
Ethnic_background = Property(IRI('https://database.factgrid.de/entity/P212'), ItemDatatype()).register(labels=[Text('Ethnic background', 'en')], range=ItemDatatype())
Etymological_components = Property(IRI('https://database.factgrid.de/entity/P987'), ItemDatatype()).register(labels=[Text('Etymological components', 'en')], range=ItemDatatype())
Etymological_explanation = Property(IRI('https://database.factgrid.de/entity/P988'), TextDatatype()).register(labels=[Text('Etymological explanation', 'en')], range=TextDatatype())
EU_Knowledge_Graph_item_ID = Property(IRI('https://database.factgrid.de/entity/P968'), ExternalIdDatatype()).register(labels=[Text('EU Knowledge Graph item ID', 'en')], range=ExternalIdDatatype())
EU_Transparency_Register_ID = Property(IRI('https://database.factgrid.de/entity/P1286'), ExternalIdDatatype()).register(labels=[Text('EU Transparency Register ID', 'en')], range=ExternalIdDatatype())
Europeana_Entity = Property(IRI('https://database.factgrid.de/entity/P385'), ExternalIdDatatype()).register(labels=[Text('Europeana Entity', 'en')], range=ExternalIdDatatype())
Events_attended = Property(IRI('https://database.factgrid.de/entity/P119'), ItemDatatype()).register(labels=[Text('Events attended', 'en')], range=ItemDatatype())
Events_in_the_sequence = Property(IRI('https://database.factgrid.de/entity/P224'), ItemDatatype()).register(labels=[Text('Events in the sequence', 'en')], range=ItemDatatype())
Events_mentioned = Property(IRI('https://database.factgrid.de/entity/P532'), ItemDatatype()).register(labels=[Text('Events mentioned', 'en')], range=ItemDatatype())
Events_witnessed = Property(IRI('https://database.factgrid.de/entity/P242'), ItemDatatype()).register(labels=[Text('Events witnessed', 'en')], range=ItemDatatype())
EVZ_ID = Property(IRI('https://database.factgrid.de/entity/P1180'), ExternalIdDatatype()).register(labels=[Text('EVZ ID', 'en')], range=ExternalIdDatatype())
Example = Property(IRI('https://database.factgrid.de/entity/P440'), ItemDatatype()).register(labels=[Text('Example', 'en')], range=ItemDatatype())
Excipit = Property(IRI('https://database.factgrid.de/entity/P602'), StringDatatype()).register(labels=[Text('Excipit', 'en')], range=StringDatatype())
Exclusion_criterion_incompatible_with_Membership_in = Property(IRI('https://database.factgrid.de/entity/P864'), ItemDatatype()).register(labels=[Text('Exclusion criterion / incompatible with Membership in', 'en')], range=ItemDatatype())
Executor = Property(IRI('https://database.factgrid.de/entity/P416'), ItemDatatype()).register(labels=[Text('Executor', 'en')], range=ItemDatatype())
Exemplary_FactGrid_item = Property(IRI('https://database.factgrid.de/entity/P364'), ItemDatatype()).register(labels=[Text('Exemplary FactGrid item', 'en')], range=ItemDatatype())
Exlibris_of = Property(IRI('https://database.factgrid.de/entity/P413'), ItemDatatype()).register(labels=[Text('Exlibris of', 'en')], range=ItemDatatype())
External_matching = Property(IRI('https://database.factgrid.de/entity/P898'), ItemDatatype()).register(labels=[Text('External matching', 'en')], range=ItemDatatype())
External_tutorial = Property(IRI('https://database.factgrid.de/entity/P978'), ItemDatatype()).register(labels=[Text('External tutorial', 'en')], range=ItemDatatype())
Extra_stemmatic_relationship = Property(IRI('https://database.factgrid.de/entity/P740'), ItemDatatype()).register(labels=[Text('Extra-stemmatic relationship', 'en')], range=ItemDatatype())
Extract = Property(IRI('https://database.factgrid.de/entity/P204'), ItemDatatype()).register(labels=[Text('Extract', 'en')], range=ItemDatatype())
Extramarital_relationship_to_procure_a_child = Property(IRI('https://database.factgrid.de/entity/P495'), ItemDatatype()).register(labels=[Text('Extramarital relationship to procure a child', 'en')], range=ItemDatatype())
Eye_colour = Property(IRI('https://database.factgrid.de/entity/P637'), ItemDatatype()).register(labels=[Text('Eye colour', 'en')], range=ItemDatatype())
Fabrication_method = Property(IRI('https://database.factgrid.de/entity/P1367'), ItemDatatype()).register(labels=[Text('Fabrication method', 'en')], range=ItemDatatype())
Face_shape = Property(IRI('https://database.factgrid.de/entity/P1393'), ItemDatatype()).register(labels=[Text('Face shape', 'en')], range=ItemDatatype())
Facebook_username = Property(IRI('https://database.factgrid.de/entity/P1163'), ExternalIdDatatype()).register(labels=[Text('Facebook username', 'en')], range=ExternalIdDatatype())
Facial_hair = Property(IRI('https://database.factgrid.de/entity/P644'), ItemDatatype()).register(labels=[Text('Facial hair', 'en')], range=ItemDatatype())
FactGrid_Collection_of_Information = Property(IRI('https://database.factgrid.de/entity/P261'), IRI_Datatype()).register(labels=[Text('FactGrid Collection of Information', 'en')], range=IRI_Datatype())
FactGrid_Dokumentseite = Property(IRI('https://database.factgrid.de/entity/P251'), IRI_Datatype()).register(labels=[Text('FactGrid Dokumentseite', 'en')], range=IRI_Datatype())
FactGrid_keyword = Property(IRI('https://database.factgrid.de/entity/P1132'), ItemDatatype()).register(labels=[Text('FactGrid keyword', 'en')], range=ItemDatatype())
FactGrid_List = Property(IRI('https://database.factgrid.de/entity/P720'), IRI_Datatype()).register(labels=[Text('FactGrid List', 'en')], range=IRI_Datatype())
FactGrid_list_of_Items_designed_for_this_property = Property(IRI('https://database.factgrid.de/entity/P310'), IRI_Datatype()).register(labels=[Text('FactGrid list of Items designed for this property', 'en')], range=IRI_Datatype())
FactGrid_list_of_members = Property(IRI('https://database.factgrid.de/entity/P320'), IRI_Datatype()).register(labels=[Text('FactGrid list of members', 'en')], range=IRI_Datatype())
FactGrid_locality_type = Property(IRI('https://database.factgrid.de/entity/P1335'), ItemDatatype()).register(labels=[Text('FactGrid locality type', 'en')], range=ItemDatatype())
FactGrid_map_House_numbers = Property(IRI('https://database.factgrid.de/entity/P679'), IRI_Datatype()).register(labels=[Text('FactGrid map: House numbers', 'en')], range=IRI_Datatype())
FactGrid_merger_candidate = Property(IRI('https://database.factgrid.de/entity/P262'), ItemDatatype()).register(labels=[Text('FactGrid merger candidate', 'en')], range=ItemDatatype())
FactGrid_project_space = Property(IRI('https://database.factgrid.de/entity/P852'), IRI_Datatype()).register(labels=[Text('FactGrid project space', 'en')], range=IRI_Datatype())
FactGrid_properties_in_which_this_item_can_serve_as_an_answer = Property(IRI('https://database.factgrid.de/entity/P184'), PropertyDatatype()).register(labels=[Text('FactGrid properties in which this item can serve as an answer', 'en')], range=PropertyDatatype())
FactGrid_properties_under_which_this_property_can_serve_as_a_qualifier = Property(IRI('https://database.factgrid.de/entity/P92'), PropertyDatatype()).register(labels=[Text('FactGrid properties under which this property can serve as a qualifier', 'en')], range=PropertyDatatype())
FactGrid_property = Property(IRI('https://database.factgrid.de/entity/P548'), PropertyDatatype()).register(labels=[Text('FactGrid property', 'en')], range=PropertyDatatype())
FactGrid_property_complaint = Property(IRI('https://database.factgrid.de/entity/P381'), ItemDatatype()).register(labels=[Text('FactGrid property complaint', 'en')], range=ItemDatatype())
FactGrid_Property_to_use_instead = Property(IRI('https://database.factgrid.de/entity/P334'), PropertyDatatype()).register(labels=[Text('FactGrid Property to use instead', 'en')], range=PropertyDatatype())
FactGrid_table_of_contents = Property(IRI('https://database.factgrid.de/entity/P309'), IRI_Datatype()).register(labels=[Text('FactGrid table of contents', 'en')], range=IRI_Datatype())
FactGrid_user_page = Property(IRI('https://database.factgrid.de/entity/P163'), IRI_Datatype()).register(labels=[Text('FactGrid user page', 'en')], range=IRI_Datatype())
FactGrid_visualisation = Property(IRI('https://database.factgrid.de/entity/P693'), IRI_Datatype()).register(labels=[Text('FactGrid visualisation', 'en')], range=IRI_Datatype())
Falk_Regiment_ID = Property(IRI('https://database.factgrid.de/entity/P969'), ExternalIdDatatype()).register(labels=[Text('Falk Regiment ID', 'en')], range=ExternalIdDatatype())
Family = Property(IRI('https://database.factgrid.de/entity/P586'), ItemDatatype()).register(labels=[Text('Family', 'en')], range=ItemDatatype())
family_database_Juden_im_Deutschen_Reich_ID = Property(IRI('https://database.factgrid.de/entity/P1068'), ExternalIdDatatype()).register(labels=[Text('family database "Juden im Deutschen Reich" ID', 'en')], range=ExternalIdDatatype())
Family_name = Property(IRI('https://database.factgrid.de/entity/P247'), ItemDatatype()).register(labels=[Text('Family name', 'en')], range=ItemDatatype())
Family_various = Property(IRI('https://database.factgrid.de/entity/P629'), ItemDatatype()).register(labels=[Text('Family various', 'en')], range=ItemDatatype())
Father = Property(IRI('https://database.factgrid.de/entity/P141'), ItemDatatype()).register(labels=[Text('Father', 'en')], range=ItemDatatype())
Fathers_status = Property(IRI('https://database.factgrid.de/entity/P615'), ItemDatatype()).register(labels=[Text("Father's status", 'en')], range=ItemDatatype())
Feldpost_number = Property(IRI('https://database.factgrid.de/entity/P1166'), StringDatatype()).register(labels=[Text('Feldpost number', 'en')], range=StringDatatype())
Fellow_student = Property(IRI('https://database.factgrid.de/entity/P485'), ItemDatatype()).register(labels=[Text('Fellow student', 'en')], range=ItemDatatype())
Female_form_of_label = Property(IRI('https://database.factgrid.de/entity/P888'), TextDatatype()).register(labels=[Text('Female form of label', 'en')], range=TextDatatype())
Feudal_obligation = Property(IRI('https://database.factgrid.de/entity/P1013'), QuantityDatatype()).register(labels=[Text('Feudal obligation', 'en')], range=QuantityDatatype())
Fictionalises_stages = Property(IRI('https://database.factgrid.de/entity/P761'), ItemDatatype()).register(labels=[Text('Fictionalises / stages', 'en')], range=ItemDatatype())
Fief_leasehold_property = Property(IRI('https://database.factgrid.de/entity/P1293'), ItemDatatype()).register(labels=[Text('Fief / leasehold property', 'en')], range=ItemDatatype())
Field_of_engagement_expertise = Property(IRI('https://database.factgrid.de/entity/P452'), ItemDatatype()).register(labels=[Text('Field of engagement / expertise', 'en')], range=ItemDatatype())
Field_of_knowledge = Property(IRI('https://database.factgrid.de/entity/P608'), ItemDatatype()).register(labels=[Text('Field of knowledge', 'en')], range=ItemDatatype())
Field_of_offices_in_the_Roman_Catholic_Church = Property(IRI('https://database.factgrid.de/entity/P1018'), ItemDatatype()).register(labels=[Text('Field of offices in the Roman Catholic Church', 'en')], range=ItemDatatype())
Field_of_research = Property(IRI('https://database.factgrid.de/entity/P97'), ItemDatatype()).register(labels=[Text('Field of research', 'en')], range=ItemDatatype())
Final_destination = Property(IRI('https://database.factgrid.de/entity/P1028'), ItemDatatype()).register(labels=[Text('Final destination', 'en')], range=ItemDatatype())
Financed_by = Property(IRI('https://database.factgrid.de/entity/P67'), ItemDatatype()).register(labels=[Text('Financed by', 'en')], range=ItemDatatype())
Find_a_Grave_memorial_ID = Property(IRI('https://database.factgrid.de/entity/P985'), ExternalIdDatatype()).register(labels=[Text('Find a Grave memorial ID', 'en')], range=ExternalIdDatatype())
Finding_spot = Property(IRI('https://database.factgrid.de/entity/P695'), ItemDatatype()).register(labels=[Text('Finding spot', 'en')], range=ItemDatatype())
Fineness_1000 = Property(IRI('https://database.factgrid.de/entity/P405'), QuantityDatatype()).register(labels=[Text('Fineness (/1000)', 'en')], range=QuantityDatatype())
First_documented_date = Property(IRI('https://database.factgrid.de/entity/P290'), TimeDatatype()).register(labels=[Text('First documented date', 'en')], range=TimeDatatype())
First_documented_in = Property(IRI('https://database.factgrid.de/entity/P631'), ItemDatatype()).register(labels=[Text('First documented in', 'en')], range=ItemDatatype())
Fiscal_revenue = Property(IRI('https://database.factgrid.de/entity/P1239'), QuantityDatatype()).register(labels=[Text('Fiscal revenue', 'en')], range=QuantityDatatype())
Flag = Property(IRI('https://database.factgrid.de/entity/P759'), StringDatatype()).register(labels=[Text('Flag', 'en')], range=StringDatatype())
Fly_leaf_Fly_leaves = Property(IRI('https://database.factgrid.de/entity/P756'), StringDatatype()).register(labels=[Text('Fly leaf/ Fly leaves', 'en')], range=StringDatatype())
Folios = Property(IRI('https://database.factgrid.de/entity/P100'), StringDatatype()).register(labels=[Text('Folio(s)', 'en')], range=StringDatatype())
Follower_of = Property(IRI('https://database.factgrid.de/entity/P300'), ItemDatatype()).register(labels=[Text('Follower of', 'en')], range=ItemDatatype())
Font_size = Property(IRI('https://database.factgrid.de/entity/P1299'), QuantityDatatype()).register(labels=[Text('Font size', 'en')], range=QuantityDatatype())
Footnote = Property(IRI('https://database.factgrid.de/entity/P102'), StringDatatype()).register(labels=[Text('Footnote', 'en')], range=StringDatatype())
Form_of_address = Property(IRI('https://database.factgrid.de/entity/P1185'), ItemDatatype()).register(labels=[Text('Form of address', 'en')], range=ItemDatatype())
Form_of_government = Property(IRI('https://database.factgrid.de/entity/P758'), ItemDatatype()).register(labels=[Text('Form of government', 'en')], range=ItemDatatype())
Form_of_punishment = Property(IRI('https://database.factgrid.de/entity/P1103'), ItemDatatype()).register(labels=[Text('Form of punishment', 'en')], range=ItemDatatype())
Format = Property(IRI('https://database.factgrid.de/entity/P93'), ItemDatatype()).register(labels=[Text('Format', 'en')], range=ItemDatatype())
format_as_a_regular_expression = Property(IRI('https://database.factgrid.de/entity/P1044'), StringDatatype()).register(labels=[Text('format as a regular expression', 'en')], range=StringDatatype())
Formatter_URL = Property(IRI('https://database.factgrid.de/entity/P236'), StringDatatype()).register(labels=[Text('Formatter URL', 'en')], range=StringDatatype())
Formed_a_set_with = Property(IRI('https://database.factgrid.de/entity/P409'), ItemDatatype()).register(labels=[Text('Formed a set with', 'en')], range=ItemDatatype())
Forum_München_ID = Property(IRI('https://database.factgrid.de/entity/P728'), ExternalIdDatatype()).register(labels=[Text('Forum München ID', 'en')], range=ExternalIdDatatype())
Founding_members = Property(IRI('https://database.factgrid.de/entity/P338'), ItemDatatype()).register(labels=[Text('Founding members', 'en')], range=ItemDatatype())
Francke_Foundations_Archives_Orphanage_Registry = Property(IRI('https://database.factgrid.de/entity/P1264'), ExternalIdDatatype()).register(labels=[Text('Francke Foundations Archives Orphanage Registry', 'en')], range=ExternalIdDatatype())
Francke_Foundations_Bio_ID = Property(IRI('https://database.factgrid.de/entity/P998'), ExternalIdDatatype()).register(labels=[Text('Francke Foundations Bio ID', 'en')], range=ExternalIdDatatype())
Franckes_Schulen_Database_ID = Property(IRI('https://database.factgrid.de/entity/P1265'), ExternalIdDatatype()).register(labels=[Text('Franckes Schulen Database ID', 'en')], range=ExternalIdDatatype())
Frankfurter_Personenlexikon = Property(IRI('https://database.factgrid.de/entity/P716'), ExternalIdDatatype()).register(labels=[Text('Frankfurter Personenlexikon', 'en')], range=ExternalIdDatatype())
Frauen_in_Bewegung_1848_1938_ID = Property(IRI('https://database.factgrid.de/entity/P667'), ExternalIdDatatype()).register(labels=[Text('Frauen in Bewegung 1848–1938 ID', 'en')], range=ExternalIdDatatype())
FRBR_entity_class = Property(IRI('https://database.factgrid.de/entity/P843'), ItemDatatype()).register(labels=[Text('FRBR entity class', 'en')], range=ItemDatatype())
Friends_with = Property(IRI('https://database.factgrid.de/entity/P192'), ItemDatatype()).register(labels=[Text('Friends with', 'en')], range=ItemDatatype())
From_place_as_mentioned = Property(IRI('https://database.factgrid.de/entity/P295'), ItemDatatype()).register(labels=[Text('From (place as mentioned)', 'en')], range=ItemDatatype())
Fruitbearing_Society_Member_ID = Property(IRI('https://database.factgrid.de/entity/P794'), ExternalIdDatatype()).register(labels=[Text('Fruitbearing Society Member ID', 'en')], range=ExternalIdDatatype())
Fundamental_sentiment = Property(IRI('https://database.factgrid.de/entity/P1127'), ItemDatatype()).register(labels=[Text('Fundamental sentiment', 'en')], range=ItemDatatype())
Funeral_speech_by = Property(IRI('https://database.factgrid.de/entity/P470'), ItemDatatype()).register(labels=[Text('Funeral speech by', 'en')], range=ItemDatatype())
fuzzy_sl_ID = Property(IRI('https://database.factgrid.de/entity/P1215'), ExternalIdDatatype()).register(labels=[Text('fuzzy-sl ID', 'en')], range=ExternalIdDatatype())
Gallica_ID = Property(IRI('https://database.factgrid.de/entity/P1002'), ExternalIdDatatype()).register(labels=[Text('Gallica ID', 'en')], range=ExternalIdDatatype())
GEDBAS_genealogy_person_ID = Property(IRI('https://database.factgrid.de/entity/P1377'), ExternalIdDatatype()).register(labels=[Text('GEDBAS genealogy person ID', 'en')], range=ExternalIdDatatype())
Gender = Property(IRI('https://database.factgrid.de/entity/P154'), ItemDatatype()).register(labels=[Text('Gender', 'en')], range=ItemDatatype())
Genealogycom_ID = Property(IRI('https://database.factgrid.de/entity/P1090'), ExternalIdDatatype()).register(labels=[Text('Genealogy.com-ID', 'en')], range=ExternalIdDatatype())
Genicom_profile_ID = Property(IRI('https://database.factgrid.de/entity/P374'), ExternalIdDatatype()).register(labels=[Text('Geni.com profile ID', 'en')], range=ExternalIdDatatype())
Geographic_compatriot_of = Property(IRI('https://database.factgrid.de/entity/P814'), ItemDatatype()).register(labels=[Text('Geographic compatriot of', 'en')], range=ItemDatatype())
Geographical_outreach = Property(IRI('https://database.factgrid.de/entity/P429'), ItemDatatype()).register(labels=[Text('Geographical outreach', 'en')], range=ItemDatatype())
Geographical_treated = Property(IRI('https://database.factgrid.de/entity/P286'), ItemDatatype()).register(labels=[Text('Geographical treated', 'en')], range=ItemDatatype())
Geomorphology = Property(IRI('https://database.factgrid.de/entity/P951'), ItemDatatype()).register(labels=[Text('Geomorphology', 'en')], range=ItemDatatype())
Geonames_Feature_Code = Property(IRI('https://database.factgrid.de/entity/P1006'), ItemDatatype()).register(labels=[Text('Geonames Feature Code', 'en')], range=ItemDatatype())
GeoNames_ID = Property(IRI('https://database.factgrid.de/entity/P418'), ExternalIdDatatype()).register(labels=[Text('GeoNames ID', 'en')], range=ExternalIdDatatype())
Geoshape = Property(IRI('https://database.factgrid.de/entity/P508'), StringDatatype()).register(labels=[Text('Geoshape', 'en')], range=StringDatatype())
GEPRIS_Historical_ID_Person = Property(IRI('https://database.factgrid.de/entity/P782'), ExternalIdDatatype()).register(labels=[Text('GEPRIS-Historical ID (Person)', 'en')], range=ExternalIdDatatype())
German_Lobbyregister_ID = Property(IRI('https://database.factgrid.de/entity/P1285'), ExternalIdDatatype()).register(labels=[Text('German Lobbyregister ID', 'en')], range=ExternalIdDatatype())
German_municipality_key = Property(IRI('https://database.factgrid.de/entity/P1072'), ExternalIdDatatype()).register(labels=[Text('German municipality key', 'en')], range=ExternalIdDatatype())
Germania_Sacra_database_of_persons_ID = Property(IRI('https://database.factgrid.de/entity/P472'), ExternalIdDatatype()).register(labels=[Text('Germania Sacra database of persons ID', 'en')], range=ExternalIdDatatype())
Getty_Thesaurus_of_Geographic_Names_ID = Property(IRI('https://database.factgrid.de/entity/P624'), ExternalIdDatatype()).register(labels=[Text('Getty Thesaurus of Geographic Names ID', 'en')], range=ExternalIdDatatype())
GitHub_username = Property(IRI('https://database.factgrid.de/entity/P719'), ExternalIdDatatype()).register(labels=[Text('GitHub username', 'en')], range=ExternalIdDatatype())
Given_names = Property(IRI('https://database.factgrid.de/entity/P248'), ItemDatatype()).register(labels=[Text('Given name(s)', 'en')], range=ItemDatatype())
GKW_ID = Property(IRI('https://database.factgrid.de/entity/P768'), ExternalIdDatatype()).register(labels=[Text('GKW-ID', 'en')], range=ExternalIdDatatype())
Glottolog_ID = Property(IRI('https://database.factgrid.de/entity/P1326'), ExternalIdDatatype()).register(labels=[Text('Glottolog ID', 'en')], range=ExternalIdDatatype())
GND_ID = Property(IRI('https://database.factgrid.de/entity/P76'), ExternalIdDatatype()).register(labels=[Text('GND ID', 'en')], range=ExternalIdDatatype())
GND_input_field = Property(IRI('https://database.factgrid.de/entity/P701'), ExternalIdDatatype()).register(labels=[Text('GND input field', 'en')], range=ExternalIdDatatype())
GND_network_graph = Property(IRI('https://database.factgrid.de/entity/P878'), ExternalIdDatatype()).register(labels=[Text('GND network graph', 'en')], range=ExternalIdDatatype())
Godfather_of_the_confirmand = Property(IRI('https://database.factgrid.de/entity/P504'), ItemDatatype()).register(labels=[Text('Godfather of the confirmand', 'en')], range=ItemDatatype())
Gold_content_g = Property(IRI('https://database.factgrid.de/entity/P395'), QuantityDatatype()).register(labels=[Text('Gold content (g)', 'en')], range=QuantityDatatype())
Google_Books_ID = Property(IRI('https://database.factgrid.de/entity/P525'), ExternalIdDatatype()).register(labels=[Text('Google Books ID', 'en')], range=ExternalIdDatatype())
Google_Knowledge_Graph_ID = Property(IRI('https://database.factgrid.de/entity/P672'), ExternalIdDatatype()).register(labels=[Text('Google Knowledge Graph ID', 'en')], range=ExternalIdDatatype())
Google_Scholar_author_ID = Property(IRI('https://database.factgrid.de/entity/P1354'), ExternalIdDatatype()).register(labels=[Text('Google Scholar author ID', 'en')], range=ExternalIdDatatype())
GOV_Group_of_Types = Property(IRI('https://database.factgrid.de/entity/P1075'), ItemDatatype()).register(labels=[Text('GOV - Group of Types', 'en')], range=ItemDatatype())
GOV_ID = Property(IRI('https://database.factgrid.de/entity/P1073'), ExternalIdDatatype()).register(labels=[Text('GOV-ID', 'en')], range=ExternalIdDatatype())
GOV_object_type = Property(IRI('https://database.factgrid.de/entity/P1077'), ItemDatatype()).register(labels=[Text('GOV object type', 'en')], range=ItemDatatype())
Grade_Level = Property(IRI('https://database.factgrid.de/entity/P1115'), ItemDatatype()).register(labels=[Text('Grade Level', 'en')], range=ItemDatatype())
Grammatical_Particle = Property(IRI('https://database.factgrid.de/entity/P1078'), ItemDatatype()).register(labels=[Text('Grammatical Particle', 'en')], range=ItemDatatype())
Grant = Property(IRI('https://database.factgrid.de/entity/P446'), ItemDatatype()).register(labels=[Text('Grant', 'en')], range=ItemDatatype())
Grave = Property(IRI('https://database.factgrid.de/entity/P79'), ItemDatatype()).register(labels=[Text('Grave', 'en')], range=ItemDatatype())
Grave_Row = Property(IRI('https://database.factgrid.de/entity/P1067'), QuantityDatatype()).register(labels=[Text('Grave Row', 'en')], range=QuantityDatatype())
Gregorian_calendar_start_date = Property(IRI('https://database.factgrid.de/entity/P289'), TimeDatatype()).register(labels=[Text('Gregorian calendar start date', 'en')], range=TimeDatatype())
Group_listings = Property(IRI('https://database.factgrid.de/entity/P930'), ItemDatatype()).register(labels=[Text('Group listings', 'en')], range=ItemDatatype())
GS_vocabulary_term = Property(IRI('https://database.factgrid.de/entity/P1301'), StringDatatype()).register(labels=[Text('GS vocabulary term', 'en')], range=StringDatatype())
Guardian = Property(IRI('https://database.factgrid.de/entity/P415'), ItemDatatype()).register(labels=[Text('Guardian', 'en')], range=ItemDatatype())
Hair = Property(IRI('https://database.factgrid.de/entity/P643'), ItemDatatype()).register(labels=[Text('Hair', 'en')], range=ItemDatatype())
HAIT_ID = Property(IRI('https://database.factgrid.de/entity/P1305'), ExternalIdDatatype()).register(labels=[Text('HAIT ID', 'en')], range=ExternalIdDatatype())
Handedness = Property(IRI('https://database.factgrid.de/entity/P640'), ItemDatatype()).register(labels=[Text('Handedness', 'en')], range=ItemDatatype())
Handwritten_by = Property(IRI('https://database.factgrid.de/entity/P25'), ItemDatatype()).register(labels=[Text('Handwritten by', 'en')], range=ItemDatatype())
Harmonia_Universalis_ID = Property(IRI('https://database.factgrid.de/entity/P424'), ExternalIdDatatype()).register(labels=[Text('Harmonia Universalis ID', 'en')], range=ExternalIdDatatype())
Has_subclasses = Property(IRI('https://database.factgrid.de/entity/P420'), ItemDatatype()).register(labels=[Text('Has subclasses', 'en')], range=ItemDatatype())
Has_works_in_the_collection = Property(IRI('https://database.factgrid.de/entity/P1275'), ItemDatatype()).register(labels=[Text('Has works in the collection', 'en')], range=ItemDatatype())
HDS_ID = Property(IRI('https://database.factgrid.de/entity/P1129'), ExternalIdDatatype()).register(labels=[Text('HDS ID', 'en')], range=ExternalIdDatatype())
Head_of = Property(IRI('https://database.factgrid.de/entity/P892'), ItemDatatype()).register(labels=[Text('Head of', 'en')], range=ItemDatatype())
Height = Property(IRI('https://database.factgrid.de/entity/P59'), QuantityDatatype()).register(labels=[Text('Height', 'en')], range=QuantityDatatype())
Heiress = Property(IRI('https://database.factgrid.de/entity/P417'), ItemDatatype()).register(labels=[Text('Heir(ess)', 'en')], range=ItemDatatype())
Hex_color = Property(IRI('https://database.factgrid.de/entity/P696'), StringDatatype()).register(labels=[Text('Hex color', 'en')], range=StringDatatype())
HISCO_ID = Property(IRI('https://database.factgrid.de/entity/P915'), ExternalIdDatatype()).register(labels=[Text('HISCO-ID', 'en')], range=ExternalIdDatatype())
Historic_county = Property(IRI('https://database.factgrid.de/entity/P538'), ItemDatatype()).register(labels=[Text('Historic county', 'en')], range=ItemDatatype())
Historical_context = Property(IRI('https://database.factgrid.de/entity/P443'), ItemDatatype()).register(labels=[Text('Historical context', 'en')], range=ItemDatatype())
Historical_continuum = Property(IRI('https://database.factgrid.de/entity/P742'), ItemDatatype()).register(labels=[Text('Historical continuum', 'en')], range=ItemDatatype())
Historical_description = Property(IRI('https://database.factgrid.de/entity/P187'), TextDatatype()).register(labels=[Text('Historical description', 'en')], range=TextDatatype())
Historical_Leiden_ID = Property(IRI('https://database.factgrid.de/entity/P1222'), ExternalIdDatatype()).register(labels=[Text('Historical Leiden ID', 'en')], range=ExternalIdDatatype())
Historical_political_regime = Property(IRI('https://database.factgrid.de/entity/P1274'), ItemDatatype()).register(labels=[Text('Historical-political regime', 'en')], range=ItemDatatype())
History = Property(IRI('https://database.factgrid.de/entity/P137'), ItemDatatype()).register(labels=[Text('History', 'en')], range=ItemDatatype())
History_of_History_Tree_ID = Property(IRI('https://database.factgrid.de/entity/P1392'), ExternalIdDatatype()).register(labels=[Text('History of History Tree ID', 'en')], range=ExternalIdDatatype())
Holding_this_position = Property(IRI('https://database.factgrid.de/entity/P299'), ItemDatatype()).register(labels=[Text('Holding this position', 'en')], range=ItemDatatype())
Holocaust_Geographies_ID = Property(IRI('https://database.factgrid.de/entity/P1386'), ExternalIdDatatype()).register(labels=[Text('Holocaust Geographies ID', 'en')], range=ExternalIdDatatype())
Holocaustcz_person_ID = Property(IRI('https://database.factgrid.de/entity/P1248'), ExternalIdDatatype()).register(labels=[Text('Holocaust.cz person ID', 'en')], range=ExternalIdDatatype())
Homosaurus_ID_version_3 = Property(IRI('https://database.factgrid.de/entity/P727'), ExternalIdDatatype()).register(labels=[Text('Homosaurus ID (version 3)', 'en')], range=ExternalIdDatatype())
Honorific_prefix = Property(IRI('https://database.factgrid.de/entity/P745'), ItemDatatype()).register(labels=[Text('Honorific prefix', 'en')], range=ItemDatatype())
Host = Property(IRI('https://database.factgrid.de/entity/P945'), ItemDatatype()).register(labels=[Text('Host', 'en')], range=ItemDatatype())
Hosted = Property(IRI('https://database.factgrid.de/entity/P210'), ItemDatatype()).register(labels=[Text('Hosted', 'en')], range=ItemDatatype())
House_number = Property(IRI('https://database.factgrid.de/entity/P152'), StringDatatype()).register(labels=[Text('House number', 'en')], range=StringDatatype())
House_numbering_system = Property(IRI('https://database.factgrid.de/entity/P646'), ItemDatatype()).register(labels=[Text('House numbering system', 'en')], range=ItemDatatype())
HOV_ID = Property(IRI('https://database.factgrid.de/entity/P1156'), ExternalIdDatatype()).register(labels=[Text('HOV ID', 'en')], range=ExternalIdDatatype())
How_sure_is_this = Property(IRI('https://database.factgrid.de/entity/P155'), ItemDatatype()).register(labels=[Text('How sure is this?', 'en')], range=ItemDatatype())
Husbandss_status = Property(IRI('https://database.factgrid.de/entity/P614'), ItemDatatype()).register(labels=[Text("Husbands's status", 'en')], range=ItemDatatype())
Hydromorphology = Property(IRI('https://database.factgrid.de/entity/P956'), ItemDatatype()).register(labels=[Text('Hydromorphology', 'en')], range=ItemDatatype())
I_campi_fascisti_ID = Property(IRI('https://database.factgrid.de/entity/P519'), ExternalIdDatatype()).register(labels=[Text('I campi fascisti ID', 'en')], range=ExternalIdDatatype())
ICD_10 = Property(IRI('https://database.factgrid.de/entity/P891'), ExternalIdDatatype()).register(labels=[Text('ICD-10', 'en')], range=ExternalIdDatatype())
Iconclass_ID = Property(IRI('https://database.factgrid.de/entity/P980'), ExternalIdDatatype()).register(labels=[Text('Iconclass ID', 'en')], range=ExternalIdDatatype())
Iconclass_identification_of_individual_motifs = Property(IRI('https://database.factgrid.de/entity/P991'), ExternalIdDatatype()).register(labels=[Text('Iconclass identification of individual motifs', 'en')], range=ExternalIdDatatype())
Iconography = Property(IRI('https://database.factgrid.de/entity/P1348'), ItemDatatype()).register(labels=[Text('Iconography', 'en')], range=ItemDatatype())
ID_19th_century_French_printers_lithographers = Property(IRI('https://database.factgrid.de/entity/P773'), ExternalIdDatatype()).register(labels=[Text('ID 19th-century French printers-lithographers', 'en')], range=ExternalIdDatatype())
ID_of_the_German_Federal_Office_of_Geodesy = Property(IRI('https://database.factgrid.de/entity/P1402'), ExternalIdDatatype()).register(labels=[Text('ID of the German Federal Office of Geodesy', 'en')], range=ExternalIdDatatype())
ID_of_the_Klassik_Stiftung_Weimar = Property(IRI('https://database.factgrid.de/entity/P1353'), ExternalIdDatatype()).register(labels=[Text('ID of the Klassik Stiftung Weimar', 'en')], range=ExternalIdDatatype())
Identification_by = Property(IRI('https://database.factgrid.de/entity/P1296'), ItemDatatype()).register(labels=[Text('Identification by', 'en')], range=ItemDatatype())
Identification_Document = Property(IRI('https://database.factgrid.de/entity/P1052'), ItemDatatype()).register(labels=[Text('Identification Document', 'en')], range=ItemDatatype())
Identification_number = Property(IRI('https://database.factgrid.de/entity/P57'), StringDatatype()).register(labels=[Text('Identification number', 'en')], range=StringDatatype())
Identified_work = Property(IRI('https://database.factgrid.de/entity/P590'), ItemDatatype()).register(labels=[Text('Identified work', 'en')], range=ItemDatatype())
Ideological_political_positioning = Property(IRI('https://database.factgrid.de/entity/P661'), ItemDatatype()).register(labels=[Text('Ideological / political positioning', 'en')], range=ItemDatatype())
IdRef_ID = Property(IRI('https://database.factgrid.de/entity/P366'), ExternalIdDatatype()).register(labels=[Text('IdRef ID', 'en')], range=ExternalIdDatatype())
ie = Property(IRI('https://database.factgrid.de/entity/P620'), ItemDatatype()).register(labels=[Text('i.e.', 'en')], range=ItemDatatype())
Illuminati_code_name = Property(IRI('https://database.factgrid.de/entity/P140'), ItemDatatype()).register(labels=[Text('Illuminati code name', 'en')], range=ItemDatatype())
Illuminati_code_name_of = Property(IRI('https://database.factgrid.de/entity/P139'), ItemDatatype()).register(labels=[Text('Illuminati code name of', 'en')], range=ItemDatatype())
Image_content = Property(IRI('https://database.factgrid.de/entity/P705'), ItemDatatype()).register(labels=[Text('Image content', 'en')], range=ItemDatatype())
Image_number = Property(IRI('https://database.factgrid.de/entity/P55'), StringDatatype()).register(labels=[Text('Image number', 'en')], range=StringDatatype())
Image_source = Property(IRI('https://database.factgrid.de/entity/P484'), ItemDatatype()).register(labels=[Text('Image source', 'en')], range=ItemDatatype())
Immediate_superiors = Property(IRI('https://database.factgrid.de/entity/P456'), ItemDatatype()).register(labels=[Text('Immediate superiors', 'en')], range=ItemDatatype())
Implemented_by = Property(IRI('https://database.factgrid.de/entity/P360'), ItemDatatype()).register(labels=[Text('Implemented by', 'en')], range=ItemDatatype())
IMSLP_ID = Property(IRI('https://database.factgrid.de/entity/P1391'), ExternalIdDatatype()).register(labels=[Text('IMSLP ID', 'en')], range=ExternalIdDatatype())
In_his_her_personal_service = Property(IRI('https://database.factgrid.de/entity/P220'), ItemDatatype()).register(labels=[Text('In his/her personal service', 'en')], range=ItemDatatype())
In_leading_position = Property(IRI('https://database.factgrid.de/entity/P14'), ItemDatatype()).register(labels=[Text('In leading position', 'en')], range=ItemDatatype())
In_the_the_reign_dynasty_time_frame = Property(IRI('https://database.factgrid.de/entity/P854'), ItemDatatype()).register(labels=[Text('In the the reign / dynasty / time frame', 'en')], range=ItemDatatype())
In_words = Property(IRI('https://database.factgrid.de/entity/P877'), TextDatatype()).register(labels=[Text('In words', 'en')], range=TextDatatype())
Incipit = Property(IRI('https://database.factgrid.de/entity/P70'), StringDatatype()).register(labels=[Text('Incipit', 'en')], range=StringDatatype())
Includes = Property(IRI('https://database.factgrid.de/entity/P9'), ItemDatatype()).register(labels=[Text('Includes', 'en')], range=ItemDatatype())
Income = Property(IRI('https://database.factgrid.de/entity/P673'), QuantityDatatype()).register(labels=[Text('Income', 'en')], range=QuantityDatatype())
Incunables_de_la_Biblioteca_Nacional_ID_1945 = Property(IRI('https://database.factgrid.de/entity/P1004'), StringDatatype()).register(labels=[Text('Incunables de la Biblioteca Nacional ID  (1945)', 'en')], range=StringDatatype())
Index_Theologicus_ID = Property(IRI('https://database.factgrid.de/entity/P1245'), ExternalIdDatatype()).register(labels=[Text('Index Theologicus ID', 'en')], range=ExternalIdDatatype())
Indication_the_object_existed = Property(IRI('https://database.factgrid.de/entity/P52'), ItemDatatype()).register(labels=[Text('Indication the object existed', 'en')], range=ItemDatatype())
INE_ID_Portugal = Property(IRI('https://database.factgrid.de/entity/P651'), ExternalIdDatatype()).register(labels=[Text('INE ID (Portugal)', 'en')], range=ExternalIdDatatype())
INE_ID_Spain = Property(IRI('https://database.factgrid.de/entity/P650'), ExternalIdDatatype()).register(labels=[Text('INE ID (Spain)', 'en')], range=ExternalIdDatatype())
Influenced_by = Property(IRI('https://database.factgrid.de/entity/P591'), ItemDatatype()).register(labels=[Text('Influenced by', 'en')], range=ItemDatatype())
Information_about_transport_connections = Property(IRI('https://database.factgrid.de/entity/P993'), ItemDatatype()).register(labels=[Text('Information about transport connections', 'en')], range=ItemDatatype())
Information_by = Property(IRI('https://database.factgrid.de/entity/P129'), ItemDatatype()).register(labels=[Text('Information by', 'en')], range=ItemDatatype())
Infrastructure = Property(IRI('https://database.factgrid.de/entity/P881'), ItemDatatype()).register(labels=[Text('Infrastructure', 'en')], range=ItemDatatype())
Initiated_by = Property(IRI('https://database.factgrid.de/entity/P268'), ItemDatatype()).register(labels=[Text('Initiated by', 'en')], range=ItemDatatype())
Inpatient_treatment_in = Property(IRI('https://database.factgrid.de/entity/P1153'), ItemDatatype()).register(labels=[Text('Inpatient treatment in', 'en')], range=ItemDatatype())
Input_form = Property(IRI('https://database.factgrid.de/entity/P1146'), IRI_Datatype()).register(labels=[Text('Input form', 'en')], range=IRI_Datatype())
Inscription = Property(IRI('https://database.factgrid.de/entity/P1219'), StringDatatype()).register(labels=[Text('Inscription', 'en')], range=StringDatatype())
INSEE_municipality_code = Property(IRI('https://database.factgrid.de/entity/P414'), ExternalIdDatatype()).register(labels=[Text('INSEE municipality code', 'en')], range=ExternalIdDatatype())
Installed_by = Property(IRI('https://database.factgrid.de/entity/P524'), ItemDatatype()).register(labels=[Text('Installed by', 'en')], range=ItemDatatype())
Instance_of = Property(IRI('https://database.factgrid.de/entity/P2'), ItemDatatype()).register(labels=[Text('Instance of', 'en')], range=ItemDatatype())
Institution_addressed = Property(IRI('https://database.factgrid.de/entity/P130'), ItemDatatype()).register(labels=[Text('Institution addressed', 'en')], range=ItemDatatype())
Institutions_mentioned = Property(IRI('https://database.factgrid.de/entity/P232'), ItemDatatype()).register(labels=[Text('Institution(s) mentioned', 'en')], range=ItemDatatype())
Instrument = Property(IRI('https://database.factgrid.de/entity/P832'), ItemDatatype()).register(labels=[Text('Instrument', 'en')], range=ItemDatatype())
Inter_national_responsibility = Property(IRI('https://database.factgrid.de/entity/P1179'), ItemDatatype()).register(labels=[Text('(Inter-)national responsibility', 'en')], range=ItemDatatype())
Inter_textual_allusions = Property(IRI('https://database.factgrid.de/entity/P574'), ItemDatatype()).register(labels=[Text('Inter-textual allusions', 'en')], range=ItemDatatype())
Interest_claim_per_annum = Property(IRI('https://database.factgrid.de/entity/P1012'), QuantityDatatype()).register(labels=[Text('Interest claim (per annum)', 'en')], range=QuantityDatatype())
Interlinear_commentary = Property(IRI('https://database.factgrid.de/entity/P1221'), StringDatatype()).register(labels=[Text('Interlinear commentary', 'en')], range=StringDatatype())
Internet_Archive_ID = Property(IRI('https://database.factgrid.de/entity/P1329'), ExternalIdDatatype()).register(labels=[Text('Internet Archive ID', 'en')], range=ExternalIdDatatype())
Internetportal_Westfälische_Geschichte_ID_Persons_entry = Property(IRI('https://database.factgrid.de/entity/P1056'), ExternalIdDatatype()).register(labels=[Text('Internetportal Westfälische Geschichte ID, Persons entry', 'en')], range=ExternalIdDatatype())
Interval = Property(IRI('https://database.factgrid.de/entity/P1231'), QuantityDatatype()).register(labels=[Text('Interval', 'en')], range=QuantityDatatype())
Intervened_on_behalf_of = Property(IRI('https://database.factgrid.de/entity/P557'), ItemDatatype()).register(labels=[Text('Intervened on behalf of', 'en')], range=ItemDatatype())
Intimate_relationships = Property(IRI('https://database.factgrid.de/entity/P230'), ItemDatatype()).register(labels=[Text('Intimate relationships', 'en')], range=ItemDatatype())
Inventoried_by = Property(IRI('https://database.factgrid.de/entity/P317'), ItemDatatype()).register(labels=[Text('Inventoried by', 'en')], range=ItemDatatype())
Inventory = Property(IRI('https://database.factgrid.de/entity/P345'), ItemDatatype()).register(labels=[Text('Inventory', 'en')], range=ItemDatatype())
Inventory_number = Property(IRI('https://database.factgrid.de/entity/P10'), StringDatatype()).register(labels=[Text('Inventory number', 'en')], range=StringDatatype())
Inverse_label_item = Property(IRI('https://database.factgrid.de/entity/P597'), ItemDatatype()).register(labels=[Text('Inverse label item', 'en')], range=ItemDatatype())
Inverse_property = Property(IRI('https://database.factgrid.de/entity/P86'), PropertyDatatype()).register(labels=[Text('Inverse property', 'en')], range=PropertyDatatype())
ISBN_10 = Property(IRI('https://database.factgrid.de/entity/P605'), ExternalIdDatatype()).register(labels=[Text('ISBN-10', 'en')], range=ExternalIdDatatype())
ISBN_13 = Property(IRI('https://database.factgrid.de/entity/P606'), ExternalIdDatatype()).register(labels=[Text('ISBN-13', 'en')], range=ExternalIdDatatype())
ISNI_ID = Property(IRI('https://database.factgrid.de/entity/P821'), ExternalIdDatatype()).register(labels=[Text('ISNI-ID', 'en')], range=ExternalIdDatatype())
ISO_3166_1_alpha_2_code = Property(IRI('https://database.factgrid.de/entity/P870'), ExternalIdDatatype()).register(labels=[Text('ISO 3166-1 alpha-2 code', 'en')], range=ExternalIdDatatype())
ISO_3166_1_alpha_3_code = Property(IRI('https://database.factgrid.de/entity/P871'), ExternalIdDatatype()).register(labels=[Text('ISO 3166-1 alpha-3 code', 'en')], range=ExternalIdDatatype())
ISO_3166_1_numeric_code = Property(IRI('https://database.factgrid.de/entity/P872'), ExternalIdDatatype()).register(labels=[Text('ISO 3166-1 numeric code', 'en')], range=ExternalIdDatatype())
ISO_3166_2 = Property(IRI('https://database.factgrid.de/entity/P873'), ExternalIdDatatype()).register(labels=[Text('ISO 3166-2', 'en')], range=ExternalIdDatatype())
ISO_3166_3 = Property(IRI('https://database.factgrid.de/entity/P874'), ExternalIdDatatype()).register(labels=[Text('ISO 3166-3', 'en')], range=ExternalIdDatatype())
ISO_639_1 = Property(IRI('https://database.factgrid.de/entity/P822'), ExternalIdDatatype()).register(labels=[Text('ISO 639-1', 'en')], range=ExternalIdDatatype())
ISO_639_2 = Property(IRI('https://database.factgrid.de/entity/P876'), ExternalIdDatatype()).register(labels=[Text('ISO 639-2', 'en')], range=ExternalIdDatatype())
ISO_639_3 = Property(IRI('https://database.factgrid.de/entity/P765'), ExternalIdDatatype()).register(labels=[Text('ISO 639-3', 'en')], range=ExternalIdDatatype())
ISO_639_5 = Property(IRI('https://database.factgrid.de/entity/P875'), ExternalIdDatatype()).register(labels=[Text('ISO 639-5', 'en')], range=ExternalIdDatatype())
ISSN = Property(IRI('https://database.factgrid.de/entity/P743'), ExternalIdDatatype()).register(labels=[Text('ISSN', 'en')], range=ExternalIdDatatype())
Issue = Property(IRI('https://database.factgrid.de/entity/P1117'), StringDatatype()).register(labels=[Text('* Issue', 'en')], range=StringDatatype())
Issuer = Property(IRI('https://database.factgrid.de/entity/P1252'), ItemDatatype()).register(labels=[Text('Issuer', 'en')], range=ItemDatatype())
ISTC_ID = Property(IRI('https://database.factgrid.de/entity/P645'), ExternalIdDatatype()).register(labels=[Text('ISTC-ID', 'en')], range=ExternalIdDatatype())
Item_count_to = Property(IRI('https://database.factgrid.de/entity/P884'), QuantityDatatype()).register(labels=[Text('Item count to', 'en')], range=QuantityDatatype())
Jacob_Grimm_Deutsches_Wörterbuch = Property(IRI('https://database.factgrid.de/entity/P893'), ExternalIdDatatype()).register(labels=[Text('Jacob Grimm, Deutsches Wörterbuch', 'en')], range=ExternalIdDatatype())
Jewish_Museum_Berlin_Person_ID = Property(IRI('https://database.factgrid.de/entity/P1225'), ExternalIdDatatype()).register(labels=[Text('Jewish Museum Berlin Person-ID', 'en')], range=ExternalIdDatatype())
Joint_partners = Property(IRI('https://database.factgrid.de/entity/P191'), ItemDatatype()).register(labels=[Text('Joint partners', 'en')], range=ItemDatatype())
Journey = Property(IRI('https://database.factgrid.de/entity/P316'), ItemDatatype()).register(labels=[Text('Journey', 'en')], range=ItemDatatype())
JudaicaLink_person_ID_GND = Property(IRI('https://database.factgrid.de/entity/P1249'), ExternalIdDatatype()).register(labels=[Text('JudaicaLink person ID (GND)', 'en')], range=ExternalIdDatatype())
Judge = Property(IRI('https://database.factgrid.de/entity/P1112'), ItemDatatype()).register(labels=[Text('Judge', 'en')], range=ItemDatatype())
Julian_calendar_last_date = Property(IRI('https://database.factgrid.de/entity/P288'), StringDatatype()).register(labels=[Text('Julian calendar last date', 'en')], range=StringDatatype())
Julian_calendar_stabiliser = Property(IRI('https://database.factgrid.de/entity/P88'), StringDatatype()).register(labels=[Text('Julian calendar stabiliser', 'en')], range=StringDatatype())
K10plus_PPN_ID = Property(IRI('https://database.factgrid.de/entity/P346'), ExternalIdDatatype()).register(labels=[Text('K10plus PPN ID', 'en')], range=ExternalIdDatatype())
Kalliope_ID = Property(IRI('https://database.factgrid.de/entity/P635'), ExternalIdDatatype()).register(labels=[Text('Kalliope ID', 'en')], range=ExternalIdDatatype())
KATOTTH_ID = Property(IRI('https://database.factgrid.de/entity/P1050'), ExternalIdDatatype()).register(labels=[Text('KATOTTH ID', 'en')], range=ExternalIdDatatype())
Key_data = Property(IRI('https://database.factgrid.de/entity/P1307'), QuantityDatatype()).register(labels=[Text('Key data', 'en')], range=QuantityDatatype())
KGI4NFDI_ID = Property(IRI('https://database.factgrid.de/entity/P1340'), ExternalIdDatatype()).register(labels=[Text('KGI4NFDI ID', 'en')], range=ExternalIdDatatype())
Kiel_Scholars_Directory_ID = Property(IRI('https://database.factgrid.de/entity/P1347'), ExternalIdDatatype()).register(labels=[Text("Kiel Scholars' Directory ID", 'en')], range=ExternalIdDatatype())
Killed_by = Property(IRI('https://database.factgrid.de/entity/P848'), ItemDatatype()).register(labels=[Text('Killed by', 'en')], range=ItemDatatype())
Klosterdatenbank_ID = Property(IRI('https://database.factgrid.de/entity/P471'), ExternalIdDatatype()).register(labels=[Text('Klosterdatenbank ID', 'en')], range=ExternalIdDatatype())
KOATUU_ID = Property(IRI('https://database.factgrid.de/entity/P1026'), ExternalIdDatatype()).register(labels=[Text('KOATUU-ID', 'en')], range=ExternalIdDatatype())
Lagis_Hessische_Biographie_ID = Property(IRI('https://database.factgrid.de/entity/P1250'), ExternalIdDatatype()).register(labels=[Text('Lagis Hessische Biographie ID', 'en')], range=ExternalIdDatatype())
Lanes_Masonic_Records_ID = Property(IRI('https://database.factgrid.de/entity/P1218'), ExternalIdDatatype()).register(labels=[Text("Lane's Masonic Records ID", 'en')], range=ExternalIdDatatype())
Language = Property(IRI('https://database.factgrid.de/entity/P18'), ItemDatatype()).register(labels=[Text('Language', 'en')], range=ItemDatatype())
Language_skills = Property(IRI('https://database.factgrid.de/entity/P460'), ItemDatatype()).register(labels=[Text('Language skills', 'en')], range=ItemDatatype())
Last_documented_date = Property(IRI('https://database.factgrid.de/entity/P291'), TimeDatatype()).register(labels=[Text('Last documented date', 'en')], range=TimeDatatype())
Last_holding_archive_of_the_lost_object = Property(IRI('https://database.factgrid.de/entity/P348'), ItemDatatype()).register(labels=[Text('Last holding archive of the lost object', 'en')], range=ItemDatatype())
Last_modified = Property(IRI('https://database.factgrid.de/entity/P612'), TimeDatatype()).register(labels=[Text('Last modified', 'en')], range=TimeDatatype())
Last_professional_status = Property(IRI('https://database.factgrid.de/entity/P211'), ItemDatatype()).register(labels=[Text('Last professional status', 'en')], range=ItemDatatype())
Latin_Place_Names_ID = Property(IRI('https://database.factgrid.de/entity/P931'), ExternalIdDatatype()).register(labels=[Text('Latin Place Names ID', 'en')], range=ExternalIdDatatype())
Latin_version = Property(IRI('https://database.factgrid.de/entity/P983'), ItemDatatype()).register(labels=[Text('Latin version', 'en')], range=ItemDatatype())
Leaseholder = Property(IRI('https://database.factgrid.de/entity/P1010'), ItemDatatype()).register(labels=[Text('Leaseholder', 'en')], range=ItemDatatype())
Leaser = Property(IRI('https://database.factgrid.de/entity/P1011'), ItemDatatype()).register(labels=[Text('Leaser', 'en')], range=ItemDatatype())
Legal_form = Property(IRI('https://database.factgrid.de/entity/P862'), ItemDatatype()).register(labels=[Text('Legal form', 'en')], range=ItemDatatype())
Legal_mandates = Property(IRI('https://database.factgrid.de/entity/P444'), ItemDatatype()).register(labels=[Text('Legal mandate(s)', 'en')], range=ItemDatatype())
Legal_response = Property(IRI('https://database.factgrid.de/entity/P1259'), ItemDatatype()).register(labels=[Text('Legal response', 'en')], range=ItemDatatype())
Legislative_term = Property(IRI('https://database.factgrid.de/entity/P795'), ItemDatatype()).register(labels=[Text('Legislative term', 'en')], range=ItemDatatype())
Length_distance = Property(IRI('https://database.factgrid.de/entity/P404'), QuantityDatatype()).register(labels=[Text('Length /distance', 'en')], range=QuantityDatatype())
Level_of_qualification = Property(IRI('https://database.factgrid.de/entity/P621'), ItemDatatype()).register(labels=[Text('Level of qualification', 'en')], range=ItemDatatype())
Library_of_Congress_authority_ID = Property(IRI('https://database.factgrid.de/entity/P1183'), ExternalIdDatatype()).register(labels=[Text('Library of Congress authority ID', 'en')], range=ExternalIdDatatype())
License = Property(IRI('https://database.factgrid.de/entity/P180'), ItemDatatype()).register(labels=[Text('License', 'en')], range=ItemDatatype())
Licensed_by = Property(IRI('https://database.factgrid.de/entity/P733'), ItemDatatype()).register(labels=[Text('Licensed by', 'en')], range=ItemDatatype())
Liegelord = Property(IRI('https://database.factgrid.de/entity/P1294'), ItemDatatype()).register(labels=[Text('Liegelord', 'en')], range=ItemDatatype())
Liegeman = Property(IRI('https://database.factgrid.de/entity/P1295'), ItemDatatype()).register(labels=[Text('Liegeman', 'en')], range=ItemDatatype())
Likelihood_percent = Property(IRI('https://database.factgrid.de/entity/P869'), QuantityDatatype()).register(labels=[Text('Likelihood (percent)', 'en')], range=QuantityDatatype())
Line = Property(IRI('https://database.factgrid.de/entity/P1030'), StringDatatype()).register(labels=[Text('Line', 'en')], range=StringDatatype())
LinkedIn_personal_profile_ID = Property(IRI('https://database.factgrid.de/entity/P709'), ExternalIdDatatype()).register(labels=[Text('LinkedIn personal profile ID', 'en')], range=ExternalIdDatatype())
Linking_back_to = Property(IRI('https://database.factgrid.de/entity/P233'), ItemDatatype()).register(labels=[Text('Linking back to', 'en')], range=ItemDatatype())
Listed_in = Property(IRI('https://database.factgrid.de/entity/P124'), ItemDatatype()).register(labels=[Text('Listed in', 'en')], range=ItemDatatype())
Literal_statement = Property(IRI('https://database.factgrid.de/entity/P35'), StringDatatype()).register(labels=[Text('Literal statement', 'en')], range=StringDatatype())
Literal_translation = Property(IRI('https://database.factgrid.de/entity/P1144'), TextDatatype()).register(labels=[Text('Literal translation', 'en')], range=TextDatatype())
Live_stock = Property(IRI('https://database.factgrid.de/entity/P1016'), QuantityDatatype()).register(labels=[Text('Live stock', 'en')], range=QuantityDatatype())
Living_conditions = Property(IRI('https://database.factgrid.de/entity/P1261'), ItemDatatype()).register(labels=[Text('Living conditions', 'en')], range=ItemDatatype())
Living_people_protection_class = Property(IRI('https://database.factgrid.de/entity/P723'), ItemDatatype()).register(labels=[Text('Living people protection class', 'en')], range=ItemDatatype())
Lizenznummer_of_books_printed_in_the_GDR = Property(IRI('https://database.factgrid.de/entity/P1093'), StringDatatype()).register(labels=[Text('Lizenznummer (of books printed in the GDR)', 'en')], range=StringDatatype())
Lobid_GND = Property(IRI('https://database.factgrid.de/entity/P855'), ExternalIdDatatype()).register(labels=[Text('Lobid-GND', 'en')], range=ExternalIdDatatype())
Local_units_of_measurement = Property(IRI('https://database.factgrid.de/entity/P386'), ItemDatatype()).register(labels=[Text('Local units of measurement', 'en')], range=ItemDatatype())
Localisation = Property(IRI('https://database.factgrid.de/entity/P47'), ItemDatatype()).register(labels=[Text('Localisation', 'en')], range=ItemDatatype())
Location_in_the_property = Property(IRI('https://database.factgrid.de/entity/P1342'), ItemDatatype()).register(labels=[Text('Location in the property', 'en')], range=ItemDatatype())
Lodge_Matriculation_number = Property(IRI('https://database.factgrid.de/entity/P669'), QuantityDatatype()).register(labels=[Text('Lodge Matriculation number', 'en')], range=QuantityDatatype())
Logo_image = Property(IRI('https://database.factgrid.de/entity/P181'), StringDatatype()).register(labels=[Text('Logo image', 'en')], range=StringDatatype())
Made_by = Property(IRI('https://database.factgrid.de/entity/P833'), ItemDatatype()).register(labels=[Text('Made by', 'en')], range=ItemDatatype())
Main_lodge = Property(IRI('https://database.factgrid.de/entity/P337'), ItemDatatype()).register(labels=[Text('Main lodge', 'en')], range=ItemDatatype())
Main_regulatory_text = Property(IRI('https://database.factgrid.de/entity/P1097'), ItemDatatype()).register(labels=[Text('Main regulatory text', 'en')], range=ItemDatatype())
Maintained_by = Property(IRI('https://database.factgrid.de/entity/P1162'), ItemDatatype()).register(labels=[Text('Maintained by', 'en')], range=ItemDatatype())
Mainzer_Ingrossaturbücher_ID = Property(IRI('https://database.factgrid.de/entity/P1057'), ExternalIdDatatype()).register(labels=[Text('Mainzer Ingrossaturbücher ID', 'en')], range=ExternalIdDatatype())
Maitron_ID = Property(IRI('https://database.factgrid.de/entity/P1065'), ExternalIdDatatype()).register(labels=[Text('Maitron ID', 'en')], range=ExternalIdDatatype())
Male_form_of_label = Property(IRI('https://database.factgrid.de/entity/P889'), TextDatatype()).register(labels=[Text('Male form of label', 'en')], range=TextDatatype())
Maps_and_plans = Property(IRI('https://database.factgrid.de/entity/P663'), ItemDatatype()).register(labels=[Text('Maps and plans', 'en')], range=ItemDatatype())
MARC_field = Property(IRI('https://database.factgrid.de/entity/P1246'), ExternalIdDatatype()).register(labels=[Text('MARC field', 'en')], range=ExternalIdDatatype())
Marriage_witness = Property(IRI('https://database.factgrid.de/entity/P340'), ItemDatatype()).register(labels=[Text('Marriage witness', 'en')], range=ItemDatatype())
Married_to = Property(IRI('https://database.factgrid.de/entity/P84'), ItemDatatype()).register(labels=[Text('Married to', 'en')], range=ItemDatatype())
Masonic_degree = Property(IRI('https://database.factgrid.de/entity/P447'), ItemDatatype()).register(labels=[Text('Masonic degree', 'en')], range=ItemDatatype())
Mass = Property(IRI('https://database.factgrid.de/entity/P397'), QuantityDatatype()).register(labels=[Text('Mass', 'en')], range=QuantityDatatype())
Mastodon_address = Property(IRI('https://database.factgrid.de/entity/P847'), ExternalIdDatatype()).register(labels=[Text('Mastodon address', 'en')], range=ExternalIdDatatype())
Matching = Property(IRI('https://database.factgrid.de/entity/P407'), QuantityDatatype()).register(labels=[Text('Matching', 'en')], range=QuantityDatatype())
Material_composition = Property(IRI('https://database.factgrid.de/entity/P401'), ItemDatatype()).register(labels=[Text('Material composition', 'en')], range=ItemDatatype())
Mathematics_Genealogy_Project_ID = Property(IRI('https://database.factgrid.de/entity/P1376'), ExternalIdDatatype()).register(labels=[Text('Mathematics Genealogy Project ID', 'en')], range=ExternalIdDatatype())
Matriculation_number_string = Property(IRI('https://database.factgrid.de/entity/P427'), StringDatatype()).register(labels=[Text('Matriculation number [string]', 'en')], range=StringDatatype())
Matrikelportal_Rostock_since_1419_ID = Property(IRI('https://database.factgrid.de/entity/P1058'), ExternalIdDatatype()).register(labels=[Text('Matrikelportal Rostock (since 1419) ID', 'en')], range=ExternalIdDatatype())
Maximum = Property(IRI('https://database.factgrid.de/entity/P767'), QuantityDatatype()).register(labels=[Text('Maximum', 'en')], range=QuantityDatatype())
Maximum_value = Property(IRI('https://database.factgrid.de/entity/P1116'), ItemDatatype()).register(labels=[Text('Maximum value', 'en')], range=ItemDatatype())
MDZ_digitisation_ID = Property(IRI('https://database.factgrid.de/entity/P526'), ExternalIdDatatype()).register(labels=[Text('MDZ digitisation ID', 'en')], range=ExternalIdDatatype())
means_of_authenticating = Property(IRI('https://database.factgrid.de/entity/P1378'), ItemDatatype()).register(labels=[Text('means of authenticating', 'en')], range=ItemDatatype())
Measures_taken = Property(IRI('https://database.factgrid.de/entity/P1200'), ItemDatatype()).register(labels=[Text('Measures taken', 'en')], range=ItemDatatype())
Media_type = Property(IRI('https://database.factgrid.de/entity/P15'), ItemDatatype()).register(labels=[Text('Media type', 'en')], range=ItemDatatype())
Medical_cause_of_death = Property(IRI('https://database.factgrid.de/entity/P162'), ItemDatatype()).register(labels=[Text('Medical cause of death', 'en')], range=ItemDatatype())
Medical_condition = Property(IRI('https://database.factgrid.de/entity/P186'), ItemDatatype()).register(labels=[Text('Medical condition', 'en')], range=ItemDatatype())
Medical_treatment = Property(IRI('https://database.factgrid.de/entity/P1135'), ItemDatatype()).register(labels=[Text('Medical treatment', 'en')], range=ItemDatatype())
Medically_tended_by = Property(IRI('https://database.factgrid.de/entity/P512'), ItemDatatype()).register(labels=[Text('Medically tended by', 'en')], range=ItemDatatype())
Meeting_point_of = Property(IRI('https://database.factgrid.de/entity/P726'), ItemDatatype()).register(labels=[Text('Meeting point of', 'en')], range=ItemDatatype())
MemArc_ID = Property(IRI('https://database.factgrid.de/entity/P1216'), ExternalIdDatatype()).register(labels=[Text('MemArc ID', 'en')], range=ExternalIdDatatype())
Member_of = Property(IRI('https://database.factgrid.de/entity/P91'), ItemDatatype()).register(labels=[Text('Member of', 'en')], range=ItemDatatype())
Members = Property(IRI('https://database.factgrid.de/entity/P293'), ItemDatatype()).register(labels=[Text('Members', 'en')], range=ItemDatatype())
Memorial_Book_Victims_of_the_Persecution_of_Jews_in_Germany_1933_1945_ID = Property(IRI('https://database.factgrid.de/entity/P1177'), ExternalIdDatatype()).register(labels=[Text('Memorial Book Victims of the Persecution of Jews in Germany 1933 – 1945 - ID', 'en')], range=ExternalIdDatatype())
Mentioned_in = Property(IRI('https://database.factgrid.de/entity/P143'), ItemDatatype()).register(labels=[Text('Mentioned in', 'en')], range=ItemDatatype())
Merchandise = Property(IRI('https://database.factgrid.de/entity/P1005'), ItemDatatype()).register(labels=[Text('Merchandise', 'en')], range=ItemDatatype())
Merger_with = Property(IRI('https://database.factgrid.de/entity/P436'), ItemDatatype()).register(labels=[Text('Merger with', 'en')], range=ItemDatatype())
Methodology = Property(IRI('https://database.factgrid.de/entity/P902'), ItemDatatype()).register(labels=[Text('Methodology', 'en')], range=ItemDatatype())
Metric_equivalent = Property(IRI('https://database.factgrid.de/entity/P834'), QuantityDatatype()).register(labels=[Text('Metric equivalent', 'en')], range=QuantityDatatype())
Minimum = Property(IRI('https://database.factgrid.de/entity/P766'), QuantityDatatype()).register(labels=[Text('Minimum', 'en')], range=QuantityDatatype())
MIRA_ID = Property(IRI('https://database.factgrid.de/entity/P1220'), ExternalIdDatatype()).register(labels=[Text('MIRA ID', 'en')], range=ExternalIdDatatype())
Misleading_attributions = Property(IRI('https://database.factgrid.de/entity/P235'), ItemDatatype()).register(labels=[Text('Misleading attributions', 'en')], range=ItemDatatype())
MMLO_ID = Property(IRI('https://database.factgrid.de/entity/P1242'), ExternalIdDatatype()).register(labels=[Text('MMLO ID', 'en')], range=ExternalIdDatatype())
Mode_of_presentation = Property(IRI('https://database.factgrid.de/entity/P698'), ItemDatatype()).register(labels=[Text('Mode of presentation', 'en')], range=ItemDatatype())
Mother = Property(IRI('https://database.factgrid.de/entity/P142'), ItemDatatype()).register(labels=[Text('Mother', 'en')], range=ItemDatatype())
Mother_lodge_Grand_lodge = Property(IRI('https://database.factgrid.de/entity/P336'), ItemDatatype()).register(labels=[Text('Mother lodge / Grand lodge', 'en')], range=ItemDatatype())
Motto = Property(IRI('https://database.factgrid.de/entity/P890'), ItemDatatype()).register(labels=[Text('Motto', 'en')], range=ItemDatatype())
Mouth = Property(IRI('https://database.factgrid.de/entity/P1397'), ItemDatatype()).register(labels=[Text('Mouth', 'en')], range=ItemDatatype())
Mouth_of_the_watercourse = Property(IRI('https://database.factgrid.de/entity/P953'), ItemDatatype()).register(labels=[Text('Mouth of the watercourse', 'en')], range=ItemDatatype())
Museum_Association_of_Saxony_Anhalt_ID = Property(IRI('https://database.factgrid.de/entity/P1227'), ExternalIdDatatype()).register(labels=[Text('Museum Association of Saxony-Anhalt ID', 'en')], range=ExternalIdDatatype())
Museum_Digital_Institutions_ID_Saxony_Anhalt = Property(IRI('https://database.factgrid.de/entity/P1228'), ExternalIdDatatype()).register(labels=[Text('Museum-Digital Institutions-ID (Saxony-Anhalt)', 'en')], range=ExternalIdDatatype())
Museum_Digital_Object_ID_Saxony_Anhalt = Property(IRI('https://database.factgrid.de/entity/P1362'), ExternalIdDatatype()).register(labels=[Text('Museum-Digital Object-ID (Saxony-Anhalt)', 'en')], range=ExternalIdDatatype())
museum_digitalhessen_people_ID = Property(IRI('https://database.factgrid.de/entity/P837'), ExternalIdDatatype()).register(labels=[Text('museum-digital:hessen people-ID', 'en')], range=ExternalIdDatatype())
Musical_notation = Property(IRI('https://database.factgrid.de/entity/P790'), ItemDatatype()).register(labels=[Text('Musical notation', 'en')], range=ItemDatatype())
Mythical_miraculous_supernatural_properties = Property(IRI('https://database.factgrid.de/entity/P1082'), ItemDatatype()).register(labels=[Text('Mythical, miraculous, supernatural properties', 'en')], range=ItemDatatype())
Name_with_the_Asiatic_Brethren = Property(IRI('https://database.factgrid.de/entity/P530'), ItemDatatype()).register(labels=[Text('Name with the Asiatic Brethren', 'en')], range=ItemDatatype())
Named_after = Property(IRI('https://database.factgrid.de/entity/P461'), ItemDatatype()).register(labels=[Text('Named after', 'en')], range=ItemDatatype())
Naming = Property(IRI('https://database.factgrid.de/entity/P34'), TextDatatype()).register(labels=[Text('Naming', 'en')], range=TextDatatype())
Naming_of_the_titles_central_protagonist = Property(IRI('https://database.factgrid.de/entity/P619'), ItemDatatype()).register(labels=[Text("Naming of the title's central protagonist", 'en')], range=ItemDatatype())
Naming_the_plural = Property(IRI('https://database.factgrid.de/entity/P1206'), ItemDatatype()).register(labels=[Text('Naming the plural', 'en')], range=ItemDatatype())
Naming_the_singular = Property(IRI('https://database.factgrid.de/entity/P1205'), ItemDatatype()).register(labels=[Text('Naming the singular', 'en')], range=ItemDatatype())
Natural_Law_Database_ID = Property(IRI('https://database.factgrid.de/entity/P844'), ExternalIdDatatype()).register(labels=[Text('Natural Law Database ID', 'en')], range=ExternalIdDatatype())
NDBA_ID = Property(IRI('https://database.factgrid.de/entity/P1133'), ExternalIdDatatype()).register(labels=[Text('NDBA ID', 'en')], range=ExternalIdDatatype())
Negative_search_result = Property(IRI('https://database.factgrid.de/entity/P468'), ItemDatatype()).register(labels=[Text('Negative search result', 'en')], range=ItemDatatype())
Net_profit = Property(IRI('https://database.factgrid.de/entity/P1238'), QuantityDatatype()).register(labels=[Text('Net profit', 'en')], range=QuantityDatatype())
Next_higher_archival_level = Property(IRI('https://database.factgrid.de/entity/P323'), ItemDatatype()).register(labels=[Text('Next higher archival level', 'en')], range=ItemDatatype())
Next_higher_organisational_level = Property(IRI('https://database.factgrid.de/entity/P428'), ItemDatatype()).register(labels=[Text('Next higher organisational level', 'en')], range=ItemDatatype())
Next_higher_rank_or_degree = Property(IRI('https://database.factgrid.de/entity/P356'), ItemDatatype()).register(labels=[Text('Next higher rank or degree', 'en')], range=ItemDatatype())
Next_version = Property(IRI('https://database.factgrid.de/entity/P219'), ItemDatatype()).register(labels=[Text('Next version', 'en')], range=ItemDatatype())
Niedersächsische_Personen_ID = Property(IRI('https://database.factgrid.de/entity/P830'), ExternalIdDatatype()).register(labels=[Text('Niedersächsische Personen ID', 'en')], range=ExternalIdDatatype())
NIOD_WW2_camp_ID = Property(IRI('https://database.factgrid.de/entity/P1184'), ExternalIdDatatype()).register(labels=[Text('NIOD WW2 camp ID', 'en')], range=ExternalIdDatatype())
NNDB_People_ID = Property(IRI('https://database.factgrid.de/entity/P1203'), ExternalIdDatatype()).register(labels=[Text('NNDB People-ID', 'en')], range=ExternalIdDatatype())
NordhausenWiki = Property(IRI('https://database.factgrid.de/entity/P1373'), ExternalIdDatatype()).register(labels=[Text('NordhausenWiki', 'en')], range=ExternalIdDatatype())
Normalization_variant = Property(IRI('https://database.factgrid.de/entity/P868'), ItemDatatype()).register(labels=[Text('Normalization variant', 'en')], range=ItemDatatype())
Nose = Property(IRI('https://database.factgrid.de/entity/P1395'), ItemDatatype()).register(labels=[Text('Nose', 'en')], range=ItemDatatype())
Not_noted_in = Property(IRI('https://database.factgrid.de/entity/P599'), ItemDatatype()).register(labels=[Text('Not noted in', 'en')], range=ItemDatatype())
Not_to_be_confused_with = Property(IRI('https://database.factgrid.de/entity/P514'), ItemDatatype()).register(labels=[Text('Not to be confused with', 'en')], range=ItemDatatype())
Note = Property(IRI('https://database.factgrid.de/entity/P73'), StringDatatype()).register(labels=[Text('Note', 'en')], range=StringDatatype())
Noted_in_these_historical_collections = Property(IRI('https://database.factgrid.de/entity/P136'), ItemDatatype()).register(labels=[Text('Noted in these historical collections', 'en')], range=ItemDatatype())
Notes = Property(IRI('https://database.factgrid.de/entity/P817'), IRI_Datatype()).register(labels=[Text('Notes', 'en')], range=IRI_Datatype())
NS_Medical_Victims_Institutions_ID = Property(IRI('https://database.factgrid.de/entity/P1380'), ExternalIdDatatype()).register(labels=[Text('NS Medical Victims Institutions ID', 'en')], range=ExternalIdDatatype())
NSDAP_membership_number_1925_1945_list = Property(IRI('https://database.factgrid.de/entity/P1190'), ExternalIdDatatype()).register(labels=[Text('NSDAP membership number  (1925–1945 list)', 'en')], range=ExternalIdDatatype())
Number = Property(IRI('https://database.factgrid.de/entity/P90'), StringDatatype()).register(labels=[Text('Number', 'en')], range=StringDatatype())
Number_making_a_unit = Property(IRI('https://database.factgrid.de/entity/P406'), QuantityDatatype()).register(labels=[Text('Number making a unit', 'en')], range=QuantityDatatype())
Number_of_abstentions = Property(IRI('https://database.factgrid.de/entity/P1309'), QuantityDatatype()).register(labels=[Text('Number of abstentions', 'en')], range=QuantityDatatype())
Number_of_blank_votes = Property(IRI('https://database.factgrid.de/entity/P1314'), QuantityDatatype()).register(labels=[Text('Number of blank votes', 'en')], range=QuantityDatatype())
Number_of_casualties = Property(IRI('https://database.factgrid.de/entity/P1164'), QuantityDatatype()).register(labels=[Text('Number of casualties', 'en')], range=QuantityDatatype())
Number_of_children = Property(IRI('https://database.factgrid.de/entity/P200'), QuantityDatatype()).register(labels=[Text('Number of children', 'en')], range=QuantityDatatype())
Number_of_copies_extant = Property(IRI('https://database.factgrid.de/entity/P654'), QuantityDatatype()).register(labels=[Text('Number of copies extant', 'en')], range=QuantityDatatype())
Number_of_copies_printed = Property(IRI('https://database.factgrid.de/entity/P653'), QuantityDatatype()).register(labels=[Text('Number of copies printed', 'en')], range=QuantityDatatype())
Number_of_employees = Property(IRI('https://database.factgrid.de/entity/P851'), QuantityDatatype()).register(labels=[Text('Number of employees', 'en')], range=QuantityDatatype())
Number_of_female_children = Property(IRI('https://database.factgrid.de/entity/P201'), QuantityDatatype()).register(labels=[Text('Number of female children', 'en')], range=QuantityDatatype())
Number_of_hierarchy_levels = Property(IRI('https://database.factgrid.de/entity/P942'), QuantityDatatype()).register(labels=[Text('Number of hierarchy levels', 'en')], range=QuantityDatatype())
Number_of_inhabitants_inmates = Property(IRI('https://database.factgrid.de/entity/P58'), QuantityDatatype()).register(labels=[Text('Number of inhabitants / inmates', 'en')], range=QuantityDatatype())
Number_of_integrated_items = Property(IRI('https://database.factgrid.de/entity/P613'), QuantityDatatype()).register(labels=[Text('Number of integrated items', 'en')], range=QuantityDatatype())
Number_of_male_children = Property(IRI('https://database.factgrid.de/entity/P202'), QuantityDatatype()).register(labels=[Text('Number of male children', 'en')], range=QuantityDatatype())
Number_of_objects_within_a_collection = Property(IRI('https://database.factgrid.de/entity/P1017'), QuantityDatatype()).register(labels=[Text('Number of objects within a collection', 'en')], range=QuantityDatatype())
Number_of_pages_leaves_sheets_columns_lines = Property(IRI('https://database.factgrid.de/entity/P107'), QuantityDatatype()).register(labels=[Text('Number of pages/ leaves/ sheets/ columns/ lines', 'en')], range=QuantityDatatype())
Number_of_participants_members = Property(IRI('https://database.factgrid.de/entity/P666'), QuantityDatatype()).register(labels=[Text('Number of participants /members', 'en')], range=QuantityDatatype())
Number_of_pieces = Property(IRI('https://database.factgrid.de/entity/P279'), QuantityDatatype()).register(labels=[Text('Number of pieces', 'en')], range=QuantityDatatype())
Number_of_registered_students = Property(IRI('https://database.factgrid.de/entity/P527'), QuantityDatatype()).register(labels=[Text('Number of registered students', 'en')], range=QuantityDatatype())
Number_of_sets_ordered = Property(IRI('https://database.factgrid.de/entity/P542'), QuantityDatatype()).register(labels=[Text('Number of sets ordered', 'en')], range=QuantityDatatype())
Number_of_social_media_followers = Property(IRI('https://database.factgrid.de/entity/P1268'), QuantityDatatype()).register(labels=[Text('Number of social media followers', 'en')], range=QuantityDatatype())
Number_of_spoilt_votes = Property(IRI('https://database.factgrid.de/entity/P1313'), QuantityDatatype()).register(labels=[Text('Number of spoilt votes', 'en')], range=QuantityDatatype())
Number_over_the_entire_period = Property(IRI('https://database.factgrid.de/entity/P1170'), QuantityDatatype()).register(labels=[Text('Number over the entire period', 'en')], range=QuantityDatatype())
NUTS_code = Property(IRI('https://database.factgrid.de/entity/P1332'), ExternalIdDatatype()).register(labels=[Text('NUTS code', 'en')], range=ExternalIdDatatype())
OARE_ID = Property(IRI('https://database.factgrid.de/entity/P1085'), ExternalIdDatatype()).register(labels=[Text('OARE ID', 'en')], range=ExternalIdDatatype())
OATP_ID = Property(IRI('https://database.factgrid.de/entity/P1087'), StringDatatype()).register(labels=[Text('OATP ID', 'en')], range=StringDatatype())
Object_has_role = Property(IRI('https://database.factgrid.de/entity/P820'), ItemDatatype()).register(labels=[Text('Object has role', 'en')], range=ItemDatatype())
Object_in_question = Property(IRI('https://database.factgrid.de/entity/P1106'), ItemDatatype()).register(labels=[Text('Object in question', 'en')], range=ItemDatatype())
Object_mentioned = Property(IRI('https://database.factgrid.de/entity/P1051'), ItemDatatype()).register(labels=[Text('Object mentioned', 'en')], range=ItemDatatype())
Object_of_payment = Property(IRI('https://database.factgrid.de/entity/P688'), ItemDatatype()).register(labels=[Text('Object of payment', 'en')], range=ItemDatatype())
Object_of_procedure = Property(IRI('https://database.factgrid.de/entity/P797'), ItemDatatype()).register(labels=[Text('Object of procedure', 'en')], range=ItemDatatype())
Object_paid = Property(IRI('https://database.factgrid.de/entity/P880'), QuantityDatatype()).register(labels=[Text('Object paid', 'en')], range=QuantityDatatype())
Object_properties_noted = Property(IRI('https://database.factgrid.de/entity/P984'), ItemDatatype()).register(labels=[Text('Object properties noted', 'en')], range=ItemDatatype())
Object_type_properties = Property(IRI('https://database.factgrid.de/entity/P899'), PropertyDatatype()).register(labels=[Text('Object type properties', 'en')], range=PropertyDatatype())
Object_types = Property(IRI('https://database.factgrid.de/entity/P936'), ItemDatatype()).register(labels=[Text('Object types', 'en')], range=ItemDatatype())
Objected_by = Property(IRI('https://database.factgrid.de/entity/P713'), ItemDatatype()).register(labels=[Text('Objected by', 'en')], range=ItemDatatype())
Objects_of_interest = Property(IRI('https://database.factgrid.de/entity/P497'), ItemDatatype()).register(labels=[Text('Objects of interest', 'en')], range=ItemDatatype())
Objects_of_knowledge = Property(IRI('https://database.factgrid.de/entity/P600'), ItemDatatype()).register(labels=[Text('Objects of knowledge', 'en')], range=ItemDatatype())
Objects_side = Property(IRI('https://database.factgrid.de/entity/P1029'), ItemDatatype()).register(labels=[Text("Object's side", 'en')], range=ItemDatatype())
OCLC_ID = Property(IRI('https://database.factgrid.de/entity/P595'), ExternalIdDatatype()).register(labels=[Text('OCLC ID', 'en')], range=ExternalIdDatatype())
OCLC_work_ID = Property(IRI('https://database.factgrid.de/entity/P375'), ExternalIdDatatype()).register(labels=[Text('OCLC work ID', 'en')], range=ExternalIdDatatype())
Of_importance_to = Property(IRI('https://database.factgrid.de/entity/P753'), ItemDatatype()).register(labels=[Text('Of importance to', 'en')], range=ItemDatatype())
Official_version = Property(IRI('https://database.factgrid.de/entity/P1076'), ItemDatatype()).register(labels=[Text('Official version', 'en')], range=ItemDatatype())
Official_website = Property(IRI('https://database.factgrid.de/entity/P156'), IRI_Datatype()).register(labels=[Text('Official website', 'en')], range=IRI_Datatype())
OhdAB_category = Property(IRI('https://database.factgrid.de/entity/P1007'), ItemDatatype()).register(labels=[Text('OhdAB category', 'en')], range=ItemDatatype())
OhdAB_ID = Property(IRI('https://database.factgrid.de/entity/P904'), ExternalIdDatatype()).register(labels=[Text('OhdAB ID', 'en')], range=ExternalIdDatatype())
OhdAB_Level_of_expertise = Property(IRI('https://database.factgrid.de/entity/P911'), ItemDatatype()).register(labels=[Text('OhdAB Level of expertise', 'en')], range=ItemDatatype())
OhdAB_standard_designation = Property(IRI('https://database.factgrid.de/entity/P914'), TextDatatype()).register(labels=[Text('OhdAB standard designation', 'en')], range=TextDatatype())
Old_inventory_number = Property(IRI('https://database.factgrid.de/entity/P30'), StringDatatype()).register(labels=[Text('Old inventory number', 'en')], range=StringDatatype())
Old_Israelite_Cemetery_Leipzig_Graves_ID = Property(IRI('https://database.factgrid.de/entity/P1223'), ExternalIdDatatype()).register(labels=[Text('Old Israelite Cemetery Leipzig Graves ID', 'en')], range=ExternalIdDatatype())
OME_ID = Property(IRI('https://database.factgrid.de/entity/P1169'), ExternalIdDatatype()).register(labels=[Text('OME ID', 'en')], range=ExternalIdDatatype())
On_the_side_of = Property(IRI('https://database.factgrid.de/entity/P739'), ItemDatatype()).register(labels=[Text('On the side of', 'en')], range=ItemDatatype())
Online_catalogue = Property(IRI('https://database.factgrid.de/entity/P438'), IRI_Datatype()).register(labels=[Text('Online catalogue', 'en')], range=IRI_Datatype())
Online_digitisation = Property(IRI('https://database.factgrid.de/entity/P138'), IRI_Datatype()).register(labels=[Text('Online digitisation', 'en')], range=IRI_Datatype())
Online_image = Property(IRI('https://database.factgrid.de/entity/P188'), IRI_Datatype()).register(labels=[Text('Online image', 'en')], range=IRI_Datatype())
Online_information = Property(IRI('https://database.factgrid.de/entity/P146'), IRI_Datatype()).register(labels=[Text('Online information', 'en')], range=IRI_Datatype())
Online_presentation = Property(IRI('https://database.factgrid.de/entity/P596'), IRI_Datatype()).register(labels=[Text('Online presentation', 'en')], range=IRI_Datatype())
Online_primary_documents = Property(IRI('https://database.factgrid.de/entity/P157'), IRI_Datatype()).register(labels=[Text('Online primary documents', 'en')], range=IRI_Datatype())
Online_transcript = Property(IRI('https://database.factgrid.de/entity/P69'), IRI_Datatype()).register(labels=[Text('Online transcript', 'en')], range=IRI_Datatype())
Online_translation = Property(IRI('https://database.factgrid.de/entity/P195'), IRI_Datatype()).register(labels=[Text('Online translation', 'en')], range=IRI_Datatype())
Ontology_data_model = Property(IRI('https://database.factgrid.de/entity/P948'), IRI_Datatype()).register(labels=[Text('Ontology / data model', 'en')], range=IRI_Datatype())
OpenHistoricalMap_ID = Property(IRI('https://database.factgrid.de/entity/P1119'), ExternalIdDatatype()).register(labels=[Text('OpenHistoricalMap ID', 'en')], range=ExternalIdDatatype())
OpenStreetMap_node_ID = Property(IRI('https://database.factgrid.de/entity/P1175'), ExternalIdDatatype()).register(labels=[Text('OpenStreetMap node ID', 'en')], range=ExternalIdDatatype())
OpenStreetMap_object = Property(IRI('https://database.factgrid.de/entity/P842'), ExternalIdDatatype()).register(labels=[Text('OpenStreetMap object', 'en')], range=ExternalIdDatatype())
OpenStreetMap_relation_ID = Property(IRI('https://database.factgrid.de/entity/P841'), ExternalIdDatatype()).register(labels=[Text('OpenStreetMap relation ID', 'en')], range=ExternalIdDatatype())
OpenStreetMap_way_ID = Property(IRI('https://database.factgrid.de/entity/P1174'), ExternalIdDatatype()).register(labels=[Text('OpenStreetMap way ID', 'en')], range=ExternalIdDatatype())
Operator = Property(IRI('https://database.factgrid.de/entity/P534'), ItemDatatype()).register(labels=[Text('Operator', 'en')], range=ItemDatatype())
Opponent_of_the_disputation = Property(IRI('https://database.factgrid.de/entity/P390'), ItemDatatype()).register(labels=[Text('Opponent of the disputation', 'en')], range=ItemDatatype())
Opposite_of = Property(IRI('https://database.factgrid.de/entity/P630'), ItemDatatype()).register(labels=[Text('Opposite of', 'en')], range=ItemDatatype())
Opposite_property = Property(IRI('https://database.factgrid.de/entity/P775'), PropertyDatatype()).register(labels=[Text('Opposite property', 'en')], range=PropertyDatatype())
Options = Property(IRI('https://database.factgrid.de/entity/P183'), ItemDatatype()).register(labels=[Text('Options', 'en')], range=ItemDatatype())
ORACC_ID = Property(IRI('https://database.factgrid.de/entity/P960'), ExternalIdDatatype()).register(labels=[Text('ORACC ID', 'en')], range=ExternalIdDatatype())
ORACC_id_word = Property(IRI('https://database.factgrid.de/entity/P1086'), StringDatatype()).register(labels=[Text('ORACC id_word', 'en')], range=StringDatatype())
ORCID_ID = Property(IRI('https://database.factgrid.de/entity/P408'), ExternalIdDatatype()).register(labels=[Text('ORCID ID', 'en')], range=ExternalIdDatatype())
Ordained_consecrated_by = Property(IRI('https://database.factgrid.de/entity/P1025'), ItemDatatype()).register(labels=[Text('Ordained / consecrated by', 'en')], range=ItemDatatype())
Organisation_open_from_here = Property(IRI('https://database.factgrid.de/entity/P358'), ItemDatatype()).register(labels=[Text('Organisation open from here', 'en')], range=ItemDatatype())
Organisation_signing_responsible = Property(IRI('https://database.factgrid.de/entity/P1150'), StringDatatype()).register(labels=[Text('* Organisation signing responsible', 'en')], range=StringDatatype())
Organisation_signing_responsible = Property(IRI('https://database.factgrid.de/entity/P66'), ItemDatatype()).register(labels=[Text('Organisation signing responsible', 'en')], range=ItemDatatype())
Organisational_aspects = Property(IRI('https://database.factgrid.de/entity/P1022'), ItemDatatype()).register(labels=[Text('Organisational aspects', 'en')], range=ItemDatatype())
Organisational_context = Property(IRI('https://database.factgrid.de/entity/P267'), ItemDatatype()).register(labels=[Text('Organisational context', 'en')], range=ItemDatatype())
Organisational_features = Property(IRI('https://database.factgrid.de/entity/P287'), ItemDatatype()).register(labels=[Text('Organisational features', 'en')], range=ItemDatatype())
Organisational_structure = Property(IRI('https://database.factgrid.de/entity/P1000'), ItemDatatype()).register(labels=[Text('Organisational structure', 'en')], range=ItemDatatype())
Organisational_ties = Property(IRI('https://database.factgrid.de/entity/P449'), ItemDatatype()).register(labels=[Text('Organisational ties', 'en')], range=ItemDatatype())
Organizational_functionality = Property(IRI('https://database.factgrid.de/entity/P1001'), ItemDatatype()).register(labels=[Text('Organizational functionality', 'en')], range=ItemDatatype())
Origin_attribute = Property(IRI('https://database.factgrid.de/entity/P970'), TextDatatype()).register(labels=[Text('Origin attribute', 'en')], range=TextDatatype())
Origin_of_the_watercourse = Property(IRI('https://database.factgrid.de/entity/P952'), ItemDatatype()).register(labels=[Text('Origin of the watercourse', 'en')], range=ItemDatatype())
Original_language = Property(IRI('https://database.factgrid.de/entity/P1157'), ItemDatatype()).register(labels=[Text('Original language', 'en')], range=ItemDatatype())
Original_note = Property(IRI('https://database.factgrid.de/entity/P520'), StringDatatype()).register(labels=[Text('Original note', 'en')], range=StringDatatype())
Original_of_this = Property(IRI('https://database.factgrid.de/entity/P114'), ItemDatatype()).register(labels=[Text('Original of this', 'en')], range=ItemDatatype())
Original_publication = Property(IRI('https://database.factgrid.de/entity/P578'), ItemDatatype()).register(labels=[Text('Original publication', 'en')], range=ItemDatatype())
Original_research_of = Property(IRI('https://database.factgrid.de/entity/P344'), ItemDatatype()).register(labels=[Text('Original research of', 'en')], range=ItemDatatype())
Originality_of_the_item = Property(IRI('https://database.factgrid.de/entity/P115'), ItemDatatype()).register(labels=[Text('Originality of the item', 'en')], range=ItemDatatype())
Osteological_Sex = Property(IRI('https://database.factgrid.de/entity/P1381'), ItemDatatype()).register(labels=[Text('Osteological Sex', 'en')], range=ItemDatatype())
Owned_by = Property(IRI('https://database.factgrid.de/entity/P126'), ItemDatatype()).register(labels=[Text('Owned by', 'en')], range=ItemDatatype())
Owner_of = Property(IRI('https://database.factgrid.de/entity/P175'), ItemDatatype()).register(labels=[Text('Owner of', 'en')], range=ItemDatatype())
P1356 = Property(IRI('https://database.factgrid.de/entity/P1356'), None)
P1389 = Property(IRI('https://database.factgrid.de/entity/P1389'), None)
Page_layout = Property(IRI('https://database.factgrid.de/entity/P481'), ItemDatatype()).register(labels=[Text('Page layout', 'en')], range=ItemDatatype())
Pages = Property(IRI('https://database.factgrid.de/entity/P54'), StringDatatype()).register(labels=[Text('Page(s)', 'en')], range=StringDatatype())
Parallel_tradition = Property(IRI('https://database.factgrid.de/entity/P253'), ItemDatatype()).register(labels=[Text('Parallel tradition', 'en')], range=ItemDatatype())
Parent_organisation = Property(IRI('https://database.factgrid.de/entity/P319'), ItemDatatype()).register(labels=[Text('Parent organisation', 'en')], range=ItemDatatype())
Parent_taxon = Property(IRI('https://database.factgrid.de/entity/P1187'), ItemDatatype()).register(labels=[Text('Parent taxon', 'en')], range=ItemDatatype())
Parish_affiliation = Property(IRI('https://database.factgrid.de/entity/P274'), ItemDatatype()).register(labels=[Text('Parish affiliation', 'en')], range=ItemDatatype())
Part_of = Property(IRI('https://database.factgrid.de/entity/P8'), ItemDatatype()).register(labels=[Text('Part of', 'en')], range=ItemDatatype())
Part_of_the_collection = Property(IRI('https://database.factgrid.de/entity/P123'), ItemDatatype()).register(labels=[Text('Part of the collection', 'en')], range=ItemDatatype())
Pastors_database_ID = Property(IRI('https://database.factgrid.de/entity/P946'), ExternalIdDatatype()).register(labels=[Text("Pastor's database ID", 'en')], range=ExternalIdDatatype())
Patients = Property(IRI('https://database.factgrid.de/entity/P513'), ItemDatatype()).register(labels=[Text('Patient(s)', 'en')], range=ItemDatatype())
Patronym_or_matronym_for_this_person = Property(IRI('https://database.factgrid.de/entity/P934'), ItemDatatype()).register(labels=[Text('Patronym or matronym for this person', 'en')], range=ItemDatatype())
Payment_interval = Property(IRI('https://database.factgrid.de/entity/P687'), ItemDatatype()).register(labels=[Text('Payment interval', 'en')], range=ItemDatatype())
Payment_recipient = Property(IRI('https://database.factgrid.de/entity/P659'), ItemDatatype()).register(labels=[Text('Payment recipient', 'en')], range=ItemDatatype())
Payment_sender = Property(IRI('https://database.factgrid.de/entity/P657'), ItemDatatype()).register(labels=[Text('Payment sender', 'en')], range=ItemDatatype())
Payment_transactor = Property(IRI('https://database.factgrid.de/entity/P658'), ItemDatatype()).register(labels=[Text('Payment transactor', 'en')], range=ItemDatatype())
Peerage_person_ID = Property(IRI('https://database.factgrid.de/entity/P1062'), ExternalIdDatatype()).register(labels=[Text('Peerage person ID', 'en')], range=ExternalIdDatatype())
People_who_were_involved_in_presence = Property(IRI('https://database.factgrid.de/entity/P133'), ItemDatatype()).register(labels=[Text('People who were involved in presence', 'en')], range=ItemDatatype())
Per = Property(IRI('https://database.factgrid.de/entity/P760'), ItemDatatype()).register(labels=[Text('Per', 'en')], range=ItemDatatype())
Percentage = Property(IRI('https://database.factgrid.de/entity/P402'), QuantityDatatype()).register(labels=[Text('Percentage', 'en')], range=QuantityDatatype())
Period_Style = Property(IRI('https://database.factgrid.de/entity/P853'), ItemDatatype()).register(labels=[Text('Period/Style', 'en')], range=ItemDatatype())
Periodicity = Property(IRI('https://database.factgrid.de/entity/P292'), ItemDatatype()).register(labels=[Text('Periodicity', 'en')], range=ItemDatatype())
Person_for_whom_the_document_was_written = Property(IRI('https://database.factgrid.de/entity/P607'), ItemDatatype()).register(labels=[Text('Person for whom the document was written', 'en')], range=ItemDatatype())
Person_signing_responsible = Property(IRI('https://database.factgrid.de/entity/P453'), ItemDatatype()).register(labels=[Text('Person signing responsible', 'en')], range=ItemDatatype())
Personal_connections = Property(IRI('https://database.factgrid.de/entity/P703'), ItemDatatype()).register(labels=[Text('Personal connections', 'en')], range=ItemDatatype())
Personal_inspection_by = Property(IRI('https://database.factgrid.de/entity/P411'), ItemDatatype()).register(labels=[Text('Personal inspection by', 'en')], range=ItemDatatype())
Personal_servant_of = Property(IRI('https://database.factgrid.de/entity/P486'), ItemDatatype()).register(labels=[Text('Personal servant of', 'en')], range=ItemDatatype())
Persons_mentioned = Property(IRI('https://database.factgrid.de/entity/P33'), ItemDatatype()).register(labels=[Text('Persons mentioned', 'en')], range=ItemDatatype())
Persons_of_Indian_Studies_ID = Property(IRI('https://database.factgrid.de/entity/P689'), ExternalIdDatatype()).register(labels=[Text('Persons of Indian Studies ID', 'en')], range=ExternalIdDatatype())
PhiloBiblon_ID = Property(IRI('https://database.factgrid.de/entity/P476'), ExternalIdDatatype()).register(labels=[Text('PhiloBiblon ID', 'en')], range=ExternalIdDatatype())
PhiloBiblon_Property_Emulator = Property(IRI('https://database.factgrid.de/entity/P1253'), PropertyDatatype()).register(labels=[Text('PhiloBiblon Property Emulator', 'en')], range=PropertyDatatype())
PhiloBiblon_vocabulary_term = Property(IRI('https://database.factgrid.de/entity/P994'), StringDatatype()).register(labels=[Text('PhiloBiblon vocabulary term', 'en')], range=StringDatatype())
Photo_Cardboard_Manufacturer = Property(IRI('https://database.factgrid.de/entity/P1360'), ItemDatatype()).register(labels=[Text('Photo Cardboard Manufacturer', 'en')], range=ItemDatatype())
Photographic_Studio = Property(IRI('https://database.factgrid.de/entity/P1204'), ItemDatatype()).register(labels=[Text('Photographic Studio', 'en')], range=ItemDatatype())
Physical_description = Property(IRI('https://database.factgrid.de/entity/P1243'), TextDatatype()).register(labels=[Text('Physical description', 'en')], range=TextDatatype())
Physical_feature = Property(IRI('https://database.factgrid.de/entity/P778'), ItemDatatype()).register(labels=[Text('Physical feature', 'en')], range=ItemDatatype())
Pilgrimage_to = Property(IRI('https://database.factgrid.de/entity/P1130'), ItemDatatype()).register(labels=[Text('Pilgrimage to', 'en')], range=ItemDatatype())
Place_of_action = Property(IRI('https://database.factgrid.de/entity/P566'), ItemDatatype()).register(labels=[Text('Place of action', 'en')], range=ItemDatatype())
Place_of_address = Property(IRI('https://database.factgrid.de/entity/P83'), ItemDatatype()).register(labels=[Text('Place of address', 'en')], range=ItemDatatype())
Place_of_baptism = Property(IRI('https://database.factgrid.de/entity/P169'), ItemDatatype()).register(labels=[Text('Place of baptism', 'en')], range=ItemDatatype())
Place_of_birth = Property(IRI('https://database.factgrid.de/entity/P82'), ItemDatatype()).register(labels=[Text('Place of birth', 'en')], range=ItemDatatype())
Place_of_death = Property(IRI('https://database.factgrid.de/entity/P168'), ItemDatatype()).register(labels=[Text('Place of death', 'en')], range=ItemDatatype())
Place_of_detention = Property(IRI('https://database.factgrid.de/entity/P216'), ItemDatatype()).register(labels=[Text('Place of detention', 'en')], range=ItemDatatype())
Place_of_education = Property(IRI('https://database.factgrid.de/entity/P501'), ItemDatatype()).register(labels=[Text('Place of education', 'en')], range=ItemDatatype())
Place_of_issue = Property(IRI('https://database.factgrid.de/entity/P926'), ItemDatatype()).register(labels=[Text('Place of issue', 'en')], range=ItemDatatype())
Place_of_marriage = Property(IRI('https://database.factgrid.de/entity/P132'), ItemDatatype()).register(labels=[Text('Place of marriage', 'en')], range=ItemDatatype())
Place_of_publication = Property(IRI('https://database.factgrid.de/entity/P1141'), StringDatatype()).register(labels=[Text('* Place of publication', 'en')], range=StringDatatype())
Place_of_publication_as_misleadingly_stated = Property(IRI('https://database.factgrid.de/entity/P240'), ItemDatatype()).register(labels=[Text('Place of publication as (misleadingly) stated', 'en')], range=ItemDatatype())
Place_of_publication_without_fictitious_information = Property(IRI('https://database.factgrid.de/entity/P241'), ItemDatatype()).register(labels=[Text('Place of publication (without fictitious information)', 'en')], range=ItemDatatype())
Plates = Property(IRI('https://database.factgrid.de/entity/P757'), StringDatatype()).register(labels=[Text('Plate(s)', 'en')], range=StringDatatype())
Pleiades_ID = Property(IRI('https://database.factgrid.de/entity/P671'), ExternalIdDatatype()).register(labels=[Text('Pleiades ID', 'en')], range=ExternalIdDatatype())
Plot_ingredient = Property(IRI('https://database.factgrid.de/entity/P568'), ItemDatatype()).register(labels=[Text('Plot ingredient', 'en')], range=ItemDatatype())
Plus = Property(IRI('https://database.factgrid.de/entity/P400'), QuantityDatatype()).register(labels=[Text('Plus', 'en')], range=QuantityDatatype())
PMB_person_ID = Property(IRI('https://database.factgrid.de/entity/P1064'), ExternalIdDatatype()).register(labels=[Text('PMB person ID', 'en')], range=ExternalIdDatatype())
Poetic_form = Property(IRI('https://database.factgrid.de/entity/P781'), StringDatatype()).register(labels=[Text('Poetic form', 'en')], range=StringDatatype())
Position_held = Property(IRI('https://database.factgrid.de/entity/P164'), ItemDatatype()).register(labels=[Text('Position held', 'en')], range=ItemDatatype())
Position_in_sequence = Property(IRI('https://database.factgrid.de/entity/P499'), QuantityDatatype()).register(labels=[Text('Position in sequence', 'en')], range=QuantityDatatype())
Position_towards_object = Property(IRI('https://database.factgrid.de/entity/P823'), ItemDatatype()).register(labels=[Text('Position towards object', 'en')], range=ItemDatatype())
Possible_further_item_connections = Property(IRI('https://database.factgrid.de/entity/P982'), ItemDatatype()).register(labels=[Text('Possible further item connections', 'en')], range=ItemDatatype())
Possible_identification_link_to_external_information = Property(IRI('https://database.factgrid.de/entity/P964'), IRI_Datatype()).register(labels=[Text('Possible identification, link to external information', 'en')], range=IRI_Datatype())
Possibly_identical_to = Property(IRI('https://database.factgrid.de/entity/P120'), ItemDatatype()).register(labels=[Text('Possibly identical to', 'en')], range=ItemDatatype())
Post_included = Property(IRI('https://database.factgrid.de/entity/P380'), ItemDatatype()).register(labels=[Text('Post included', 'en')], range=ItemDatatype())
Postal_address = Property(IRI('https://database.factgrid.de/entity/P153'), StringDatatype()).register(labels=[Text('Postal address', 'en')], range=StringDatatype())
Postal_code = Property(IRI('https://database.factgrid.de/entity/P986'), StringDatatype()).register(labels=[Text('Postal code', 'en')], range=StringDatatype())
Preceding_Lexemes_in_stemma = Property(IRI('https://database.factgrid.de/entity/P824'), LexemeDatatype()).register(labels=[Text('Preceding Lexemes in stemma', 'en')], range=LexemeDatatype())
Precision_of_begin_date = Property(IRI('https://database.factgrid.de/entity/P785'), ItemDatatype()).register(labels=[Text('Precision of begin date', 'en')], range=ItemDatatype())
Precision_of_begin_date_string = Property(IRI('https://database.factgrid.de/entity/P787'), StringDatatype()).register(labels=[Text('Precision of begin date [string]', 'en')], range=StringDatatype())
Precision_of_date = Property(IRI('https://database.factgrid.de/entity/P467'), ItemDatatype()).register(labels=[Text('Precision of date', 'en')], range=ItemDatatype())
Precision_of_end_date = Property(IRI('https://database.factgrid.de/entity/P786'), ItemDatatype()).register(labels=[Text('Precision of end date', 'en')], range=ItemDatatype())
Precision_of_end_date_string = Property(IRI('https://database.factgrid.de/entity/P788'), StringDatatype()).register(labels=[Text('Precision of end date [string]', 'en')], range=StringDatatype())
Precision_of_localisation = Property(IRI('https://database.factgrid.de/entity/P425'), ItemDatatype()).register(labels=[Text('Precision of localisation', 'en')], range=ItemDatatype())
Predominant_gender_usage = Property(IRI('https://database.factgrid.de/entity/P625'), ItemDatatype()).register(labels=[Text('Predominant gender usage', 'en')], range=ItemDatatype())
Preface_by = Property(IRI('https://database.factgrid.de/entity/P179'), ItemDatatype()).register(labels=[Text('Preface by', 'en')], range=ItemDatatype())
Preferred_designation = Property(IRI('https://database.factgrid.de/entity/P1331'), TextDatatype()).register(labels=[Text('Preferred designation', 'en')], range=TextDatatype())
PRELIB_archival_document_ID = Property(IRI('https://database.factgrid.de/entity/P811'), ExternalIdDatatype()).register(labels=[Text('PRELIB archival document ID', 'en')], range=ExternalIdDatatype())
PRELIB_edition_ID = Property(IRI('https://database.factgrid.de/entity/P810'), ExternalIdDatatype()).register(labels=[Text('PRELIB edition ID', 'en')], range=ExternalIdDatatype())
PRELIB_organization_ID = Property(IRI('https://database.factgrid.de/entity/P764'), ExternalIdDatatype()).register(labels=[Text('PRELIB organization ID', 'en')], range=ExternalIdDatatype())
PRELIB_periodical_ID = Property(IRI('https://database.factgrid.de/entity/P812'), ExternalIdDatatype()).register(labels=[Text('PRELIB periodical ID', 'en')], range=ExternalIdDatatype())
PRELIB_person_ID = Property(IRI('https://database.factgrid.de/entity/P763'), ExternalIdDatatype()).register(labels=[Text('PRELIB person ID', 'en')], range=ExternalIdDatatype())
PRELIB_place_ID = Property(IRI('https://database.factgrid.de/entity/P807'), ExternalIdDatatype()).register(labels=[Text('PRELIB place ID', 'en')], range=ExternalIdDatatype())
PRELIB_work_ID = Property(IRI('https://database.factgrid.de/entity/P809'), ExternalIdDatatype()).register(labels=[Text('PRELIB work ID', 'en')], range=ExternalIdDatatype())
Premiere = Property(IRI('https://database.factgrid.de/entity/P714'), ItemDatatype()).register(labels=[Text('Premiere', 'en')], range=ItemDatatype())
Present_holding = Property(IRI('https://database.factgrid.de/entity/P329'), ItemDatatype()).register(labels=[Text('Present holding', 'en')], range=ItemDatatype())
Presentation = Property(IRI('https://database.factgrid.de/entity/P238'), ItemDatatype()).register(labels=[Text('Presentation', 'en')], range=ItemDatatype())
Presented_at = Property(IRI('https://database.factgrid.de/entity/P237'), ItemDatatype()).register(labels=[Text('Presented at', 'en')], range=ItemDatatype())
Presented_by = Property(IRI('https://database.factgrid.de/entity/P264'), ItemDatatype()).register(labels=[Text('Presented by', 'en')], range=ItemDatatype())
Preservation = Property(IRI('https://database.factgrid.de/entity/P158'), ItemDatatype()).register(labels=[Text('Preservation', 'en')], range=ItemDatatype())
Presiding_the_disputation = Property(IRI('https://database.factgrid.de/entity/P388'), ItemDatatype()).register(labels=[Text('Presiding the disputation', 'en')], range=ItemDatatype())
Previous_version = Property(IRI('https://database.factgrid.de/entity/P218'), ItemDatatype()).register(labels=[Text('Previous version', 'en')], range=ItemDatatype())
Primary_source = Property(IRI('https://database.factgrid.de/entity/P51'), ItemDatatype()).register(labels=[Text('Primary source', 'en')], range=ItemDatatype())
Printed_by = Property(IRI('https://database.factgrid.de/entity/P207'), ItemDatatype()).register(labels=[Text('Printed by', 'en')], range=ItemDatatype())
Prisoner_of_war_of = Property(IRI('https://database.factgrid.de/entity/P752'), ItemDatatype()).register(labels=[Text('Prisoner of war of', 'en')], range=ItemDatatype())
Privilege_granted_by = Property(IRI('https://database.factgrid.de/entity/P322'), ItemDatatype()).register(labels=[Text('Privilege granted by', 'en')], range=ItemDatatype())
Proceedings_of_the_event = Property(IRI('https://database.factgrid.de/entity/P94'), ItemDatatype()).register(labels=[Text('Proceedings of the event', 'en')], range=ItemDatatype())
Process_File_number = Property(IRI('https://database.factgrid.de/entity/P1197'), ItemDatatype()).register(labels=[Text('Process / File number', 'en')], range=ItemDatatype())
Produced_by_brand = Property(IRI('https://database.factgrid.de/entity/P718'), ItemDatatype()).register(labels=[Text('Produced by (brand)', 'en')], range=ItemDatatype())
Produces_product_range = Property(IRI('https://database.factgrid.de/entity/P798'), ItemDatatype()).register(labels=[Text('Produces / product range', 'en')], range=ItemDatatype())
Professional_address = Property(IRI('https://database.factgrid.de/entity/P865'), ItemDatatype()).register(labels=[Text('Professional address', 'en')], range=ItemDatatype())
Programming_language = Property(IRI('https://database.factgrid.de/entity/P1319'), ItemDatatype()).register(labels=[Text('Programming language', 'en')], range=ItemDatatype())
Project = Property(IRI('https://database.factgrid.de/entity/P177'), ItemDatatype()).register(labels=[Text('Project', 'en')], range=ItemDatatype())
Pronunciation_IPA = Property(IRI('https://database.factgrid.de/entity/P1023'), TextDatatype()).register(labels=[Text('Pronunciation (IPA)', 'en')], range=TextDatatype())
Property_constraint = Property(IRI('https://database.factgrid.de/entity/P627'), ItemDatatype()).register(labels=[Text('Property constraint', 'en')], range=ItemDatatype())
Proposed_introduced_by = Property(IRI('https://database.factgrid.de/entity/P269'), ItemDatatype()).register(labels=[Text('Proposed / introduced by', 'en')], range=ItemDatatype())
Proposed_to_become_a_member_of = Property(IRI('https://database.factgrid.de/entity/P454'), ItemDatatype()).register(labels=[Text('Proposed to become a member of', 'en')], range=ItemDatatype())
Proprietor_in = Property(IRI('https://database.factgrid.de/entity/P149'), ItemDatatype()).register(labels=[Text('Proprietor in', 'en')], range=ItemDatatype())
Protagonists = Property(IRI('https://database.factgrid.de/entity/P567'), ItemDatatype()).register(labels=[Text('Protagonist(s)', 'en')], range=ItemDatatype())
Pseudonym = Property(IRI('https://database.factgrid.de/entity/P341'), ItemDatatype()).register(labels=[Text('Pseudonym', 'en')], range=ItemDatatype())
Pseudonym_literal = Property(IRI('https://database.factgrid.de/entity/P1230'), StringDatatype()).register(labels=[Text('Pseudonym [literal]', 'en')], range=StringDatatype())
Pseudonym_of = Property(IRI('https://database.factgrid.de/entity/P193'), ItemDatatype()).register(labels=[Text('Pseudonym of', 'en')], range=ItemDatatype())
Public_awards_and_titles = Property(IRI('https://database.factgrid.de/entity/P171'), ItemDatatype()).register(labels=[Text('Public awards and titles', 'en')], range=ItemDatatype())
Publications_stemming_from_this_research = Property(IRI('https://database.factgrid.de/entity/P151'), ItemDatatype()).register(labels=[Text('Publications stemming from this research', 'en')], range=ItemDatatype())
Published_in = Property(IRI('https://database.factgrid.de/entity/P1137'), StringDatatype()).register(labels=[Text('* Published in', 'en')], range=StringDatatype())
Published_in = Property(IRI('https://database.factgrid.de/entity/P64'), ItemDatatype()).register(labels=[Text('Published in', 'en')], range=ItemDatatype())
Published_in_this_publication = Property(IRI('https://database.factgrid.de/entity/P254'), ItemDatatype()).register(labels=[Text('Published in this publication', 'en')], range=ItemDatatype())
Publisher = Property(IRI('https://database.factgrid.de/entity/P1140'), StringDatatype()).register(labels=[Text('* Publisher', 'en')], range=StringDatatype())
Publisher = Property(IRI('https://database.factgrid.de/entity/P206'), ItemDatatype()).register(labels=[Text('Publisher', 'en')], range=ItemDatatype())
Publisher_as_misleadingly_stated = Property(IRI('https://database.factgrid.de/entity/P544'), ItemDatatype()).register(labels=[Text('Publisher as misleadingly stated', 'en')], range=ItemDatatype())
Purpose = Property(IRI('https://database.factgrid.de/entity/P515'), ItemDatatype()).register(labels=[Text('Purpose', 'en')], range=ItemDatatype())
Qualifier = Property(IRI('https://database.factgrid.de/entity/P4'), StringDatatype()).register(labels=[Text('* Qualifier', 'en')], range=StringDatatype())
Qualifying_sub_properties = Property(IRI('https://database.factgrid.de/entity/P333'), PropertyDatatype()).register(labels=[Text('Qualifying sub-properties', 'en')], range=PropertyDatatype())
Quantity = Property(IRI('https://database.factgrid.de/entity/P307'), QuantityDatatype()).register(labels=[Text('Quantity', 'en')], range=QuantityDatatype())
Quote = Property(IRI('https://database.factgrid.de/entity/P1272'), TextDatatype()).register(labels=[Text('Quote', 'en')], range=TextDatatype())
Quoting = Property(IRI('https://database.factgrid.de/entity/P306'), ItemDatatype()).register(labels=[Text('Quoting', 'en')], range=ItemDatatype())
RAG_ID = Property(IRI('https://database.factgrid.de/entity/P517'), ExternalIdDatatype()).register(labels=[Text('RAG ID', 'en')], range=ExternalIdDatatype())
Raised_by = Property(IRI('https://database.factgrid.de/entity/P258'), ItemDatatype()).register(labels=[Text('Raised by', 'en')], range=ItemDatatype())
RAM_size = Property(IRI('https://database.factgrid.de/entity/P1322'), QuantityDatatype()).register(labels=[Text('RAM size', 'en')], range=QuantityDatatype())
Rank = Property(IRI('https://database.factgrid.de/entity/P1145'), ItemDatatype()).register(labels=[Text('Rank', 'en')], range=ItemDatatype())
Rank_service_number = Property(IRI('https://database.factgrid.de/entity/P1080'), StringDatatype()).register(labels=[Text('Rank service number', 'en')], range=StringDatatype())
re3data_D = Property(IRI('https://database.factgrid.de/entity/P1159'), ExternalIdDatatype()).register(labels=[Text('re3data D', 'en')], range=ExternalIdDatatype())
Real_estate = Property(IRI('https://database.factgrid.de/entity/P208'), ItemDatatype()).register(labels=[Text('Real estate', 'en')], range=ItemDatatype())
Realization_Construction = Property(IRI('https://database.factgrid.de/entity/P518'), ItemDatatype()).register(labels=[Text('Realization / Construction', 'en')], range=ItemDatatype())
Reason_for_deprecated_rank = Property(IRI('https://database.factgrid.de/entity/P1343'), ItemDatatype()).register(labels=[Text('Reason for deprecated rank', 'en')], range=ItemDatatype())
Reason_for_persecution = Property(IRI('https://database.factgrid.de/entity/P558'), ItemDatatype()).register(labels=[Text('Reason for persecution', 'en')], range=ItemDatatype())
Reason_for_preferred_rank = Property(IRI('https://database.factgrid.de/entity/P1344'), ItemDatatype()).register(labels=[Text('Reason for preferred rank', 'en')], range=ItemDatatype())
Receives_area_from = Property(IRI('https://database.factgrid.de/entity/P1337'), ItemDatatype()).register(labels=[Text('Receives area from', 'en')], range=ItemDatatype())
Reception_promises_literal = Property(IRI('https://database.factgrid.de/entity/P570'), ItemDatatype()).register(labels=[Text('Reception promises (literal)', 'en')], range=ItemDatatype())
Recipient = Property(IRI('https://database.factgrid.de/entity/P28'), ItemDatatype()).register(labels=[Text('Recipient', 'en')], range=ItemDatatype())
Recognised_by = Property(IRI('https://database.factgrid.de/entity/P430'), ItemDatatype()).register(labels=[Text('Recognised by', 'en')], range=ItemDatatype())
Recording_online_information = Property(IRI('https://database.factgrid.de/entity/P541'), IRI_Datatype()).register(labels=[Text('Recording, online information', 'en')], range=IRI_Datatype())
Reference_code = Property(IRI('https://database.factgrid.de/entity/P806'), StringDatatype()).register(labels=[Text('Reference code', 'en')], range=StringDatatype())
Referencing_method = Property(IRI('https://database.factgrid.de/entity/P937'), ItemDatatype()).register(labels=[Text('Referencing method', 'en')], range=ItemDatatype())
Regional_localisation = Property(IRI('https://database.factgrid.de/entity/P861'), ItemDatatype()).register(labels=[Text('Regional localisation', 'en')], range=ItemDatatype())
Registered_accepted_by = Property(IRI('https://database.factgrid.de/entity/P503'), ItemDatatype()).register(labels=[Text('Registered / accepted by', 'en')], range=ItemDatatype())
Registrar = Property(IRI('https://database.factgrid.de/entity/P738'), ItemDatatype()).register(labels=[Text('Registrar', 'en')], range=ItemDatatype())
Registry_number = Property(IRI('https://database.factgrid.de/entity/P803'), StringDatatype()).register(labels=[Text('Registry number', 'en')], range=StringDatatype())
Registry_office_of = Property(IRI('https://database.factgrid.de/entity/P1088'), ItemDatatype()).register(labels=[Text('Registry office (of)', 'en')], range=ItemDatatype())
Regular_meeting_point = Property(IRI('https://database.factgrid.de/entity/P209'), ItemDatatype()).register(labels=[Text('Regular meeting point', 'en')], range=ItemDatatype())
Related_object = Property(IRI('https://database.factgrid.de/entity/P750'), ItemDatatype()).register(labels=[Text('Related object', 'en')], range=ItemDatatype())
Relation_constraint = Property(IRI('https://database.factgrid.de/entity/P628'), ItemDatatype()).register(labels=[Text('Relation constraint', 'en')], range=ItemDatatype())
Relationship_through = Property(IRI('https://database.factgrid.de/entity/P1066'), ItemDatatype()).register(labels=[Text('Relationship through', 'en')], range=ItemDatatype())
Religious_background = Property(IRI('https://database.factgrid.de/entity/P172'), ItemDatatype()).register(labels=[Text('Religious background', 'en')], range=ItemDatatype())
Religious_or_spiritual_practice_and_experiences = Property(IRI('https://database.factgrid.de/entity/P588'), ItemDatatype()).register(labels=[Text('Religious or spiritual practice and experiences', 'en')], range=ItemDatatype())
Religious_order = Property(IRI('https://database.factgrid.de/entity/P746'), ItemDatatype()).register(labels=[Text('Religious order', 'en')], range=ItemDatatype())
Religious_status = Property(IRI('https://database.factgrid.de/entity/P1118'), ItemDatatype()).register(labels=[Text('Religious status', 'en')], range=ItemDatatype())
Relocated_subject = Property(IRI('https://database.factgrid.de/entity/P1198'), ItemDatatype()).register(labels=[Text('Relocated subject', 'en')], range=ItemDatatype())
Renewal_date = Property(IRI('https://database.factgrid.de/entity/P818'), TimeDatatype()).register(labels=[Text('Renewal date', 'en')], range=TimeDatatype())
Rent_per_annum = Property(IRI('https://database.factgrid.de/entity/P943'), QuantityDatatype()).register(labels=[Text('Rent (per annum)', 'en')], range=QuantityDatatype())
Repertorium_Germanicum_ID = Property(IRI('https://database.factgrid.de/entity/P473'), ExternalIdDatatype()).register(labels=[Text('Repertorium Germanicum ID', 'en')], range=ExternalIdDatatype())
Repertorium_Poenitentiariae_Germanicum_ID = Property(IRI('https://database.factgrid.de/entity/P1128'), ExternalIdDatatype()).register(labels=[Text('Repertorium Poenitentiariae Germanicum ID', 'en')], range=ExternalIdDatatype())
Reported_event = Property(IRI('https://database.factgrid.de/entity/P19'), ItemDatatype()).register(labels=[Text('Reported event', 'en')], range=ItemDatatype())
Represented_by = Property(IRI('https://database.factgrid.de/entity/P328'), ItemDatatype()).register(labels=[Text('Represented by', 'en')], range=ItemDatatype())
Representing = Property(IRI('https://database.factgrid.de/entity/P448'), ItemDatatype()).register(labels=[Text('Representing', 'en')], range=ItemDatatype())
Request_FactGrid = Property(IRI('https://database.factgrid.de/entity/P592'), IRI_Datatype()).register(labels=[Text('Request FactGrid', 'en')], range=IRI_Datatype())
Request_name = Property(IRI('https://database.factgrid.de/entity/P593'), ItemDatatype()).register(labels=[Text('Request name', 'en')], range=ItemDatatype())
Research_projects_that_contributed_to_this_data_set = Property(IRI('https://database.factgrid.de/entity/P131'), ItemDatatype()).register(labels=[Text('Research projects that contributed to this data set', 'en')], range=ItemDatatype())
Research_stay_in = Property(IRI('https://database.factgrid.de/entity/P351'), ItemDatatype()).register(labels=[Text('Research stay in', 'en')], range=ItemDatatype())
ResearchGate_profile_ID = Property(IRI('https://database.factgrid.de/entity/P712'), ExternalIdDatatype()).register(labels=[Text('ResearchGate profile ID', 'en')], range=ExternalIdDatatype())
Resident = Property(IRI('https://database.factgrid.de/entity/P239'), ItemDatatype()).register(labels=[Text('Resident', 'en')], range=ItemDatatype())
Respondent_of_the_disputation = Property(IRI('https://database.factgrid.de/entity/P389'), ItemDatatype()).register(labels=[Text('Respondent of the disputation', 'en')], range=ItemDatatype())
Result = Property(IRI('https://database.factgrid.de/entity/P108'), QuantityDatatype()).register(labels=[Text('Result', 'en')], range=QuantityDatatype())
Result_of_investigation = Property(IRI('https://database.factgrid.de/entity/P1102'), ItemDatatype()).register(labels=[Text('Result of investigation', 'en')], range=ItemDatatype())
Reviewed_in = Property(IRI('https://database.factgrid.de/entity/P135'), ItemDatatype()).register(labels=[Text('Reviewed in', 'en')], range=ItemDatatype())
Reviewing = Property(IRI('https://database.factgrid.de/entity/P308'), ItemDatatype()).register(labels=[Text('Reviewing', 'en')], range=ItemDatatype())
Revised_by = Property(IRI('https://database.factgrid.de/entity/P22'), ItemDatatype()).register(labels=[Text('Revised by', 'en')], range=ItemDatatype())
Rhyme_scheme = Property(IRI('https://database.factgrid.de/entity/P783'), StringDatatype()).register(labels=[Text('Rhyme scheme', 'en')], range=StringDatatype())
RI_ID = Property(IRI('https://database.factgrid.de/entity/P791'), ExternalIdDatatype()).register(labels=[Text('RI ID', 'en')], range=ExternalIdDatatype())
RISM_ID = Property(IRI('https://database.factgrid.de/entity/P655'), ExternalIdDatatype()).register(labels=[Text('RISM ID', 'en')], range=ExternalIdDatatype())
Rite_rule_system = Property(IRI('https://database.factgrid.de/entity/P521'), ItemDatatype()).register(labels=[Text('Rite / rule / system', 'en')], range=ItemDatatype())
Role = Property(IRI('https://database.factgrid.de/entity/P445'), ItemDatatype()).register(labels=[Text('Role', 'en')], range=ItemDatatype())
Romanised_transcription = Property(IRI('https://database.factgrid.de/entity/P670'), StringDatatype()).register(labels=[Text('Romanised transcription', 'en')], range=StringDatatype())
Room_number = Property(IRI('https://database.factgrid.de/entity/P1032'), StringDatatype()).register(labels=[Text('Room number', 'en')], range=StringDatatype())
Rosicrucian_code_name = Property(IRI('https://database.factgrid.de/entity/P354'), ItemDatatype()).register(labels=[Text('Rosicrucian code name', 'en')], range=ItemDatatype())
Rosicrucian_code_name_of = Property(IRI('https://database.factgrid.de/entity/P353'), ItemDatatype()).register(labels=[Text('Rosicrucian code name of', 'en')], range=ItemDatatype())
Said_to_be_the_same_as = Property(IRI('https://database.factgrid.de/entity/P493'), ItemDatatype()).register(labels=[Text('Said to be the same as', 'en')], range=ItemDatatype())
Sandrartnet_person_ID = Property(IRI('https://database.factgrid.de/entity/P813'), ExternalIdDatatype()).register(labels=[Text('Sandrart.net person ID', 'en')], range=ExternalIdDatatype())
Scale_1n = Property(IRI('https://database.factgrid.de/entity/P859'), QuantityDatatype()).register(labels=[Text('Scale (1:n)', 'en')], range=QuantityDatatype())
Schoenberg_Database_of_Manuscripts_name_ID = Property(IRI('https://database.factgrid.de/entity/P1288'), ExternalIdDatatype()).register(labels=[Text('Schoenberg Database of Manuscripts name ID', 'en')], range=ExternalIdDatatype())
School_adherence = Property(IRI('https://database.factgrid.de/entity/P623'), ItemDatatype()).register(labels=[Text('School adherence', 'en')], range=ItemDatatype())
Script_style = Property(IRI('https://database.factgrid.de/entity/P747'), ItemDatatype()).register(labels=[Text('Script style', 'en')], range=ItemDatatype())
Seal = Property(IRI('https://database.factgrid.de/entity/P355'), ItemDatatype()).register(labels=[Text('Seal', 'en')], range=ItemDatatype())
Seal_ID = Property(IRI('https://database.factgrid.de/entity/P1084'), StringDatatype()).register(labels=[Text('Seal ID', 'en')], range=StringDatatype())
Second_family_name_in_Spanish_name = Property(IRI('https://database.factgrid.de/entity/P917'), ItemDatatype()).register(labels=[Text('Second family name in Spanish name', 'en')], range=ItemDatatype())
Secondary_literature_research = Property(IRI('https://database.factgrid.de/entity/P12'), ItemDatatype()).register(labels=[Text('Secondary literature / research', 'en')], range=ItemDatatype())
Secondary_literature_research_literal = Property(IRI('https://database.factgrid.de/entity/P1053'), StringDatatype()).register(labels=[Text('Secondary literature / research [literal]', 'en')], range=StringDatatype())
Section = Property(IRI('https://database.factgrid.de/entity/P103'), StringDatatype()).register(labels=[Text('Section', 'en')], range=StringDatatype())
See_also = Property(IRI('https://database.factgrid.de/entity/P301'), ItemDatatype()).register(labels=[Text('See also', 'en')], range=ItemDatatype())
See_also_property = Property(IRI('https://database.factgrid.de/entity/P85'), PropertyDatatype()).register(labels=[Text('See also property', 'en')], range=PropertyDatatype())
Segmentation = Property(IRI('https://database.factgrid.de/entity/P543'), ItemDatatype()).register(labels=[Text('Segmentation', 'en')], range=ItemDatatype())
Sejm_Wielkipl_profile_ID = Property(IRI('https://database.factgrid.de/entity/P1024'), ExternalIdDatatype()).register(labels=[Text('Sejm-Wielki.pl profile ID', 'en')], range=ExternalIdDatatype())
Self_classification_Lexeme = Property(IRI('https://database.factgrid.de/entity/P825'), LexemeDatatype()).register(labels=[Text('Self classification [Lexeme]', 'en')], range=LexemeDatatype())
Self_statement_on_historicity_fictionality = Property(IRI('https://database.factgrid.de/entity/P565'), ItemDatatype()).register(labels=[Text('Self-statement on historicity / fictionality', 'en')], range=ItemDatatype())
Semantic_Kompakkt_ID = Property(IRI('https://database.factgrid.de/entity/P1214'), ExternalIdDatatype()).register(labels=[Text('Semantic Kompakkt ID', 'en')], range=ExternalIdDatatype())
Series = Property(IRI('https://database.factgrid.de/entity/P1139'), StringDatatype()).register(labels=[Text('* Series', 'en')], range=StringDatatype())
Series_integration = Property(IRI('https://database.factgrid.de/entity/P441'), ItemDatatype()).register(labels=[Text('Series integration', 'en')], range=ItemDatatype())
Services_offered = Property(IRI('https://database.factgrid.de/entity/P995'), ItemDatatype()).register(labels=[Text('Services offered', 'en')], range=ItemDatatype())
Set_by = Property(IRI('https://database.factgrid.de/entity/P737'), ItemDatatype()).register(labels=[Text('Set by', 'en')], range=ItemDatatype())
Sexual_orientation = Property(IRI('https://database.factgrid.de/entity/P711'), ItemDatatype()).register(labels=[Text('Sexual orientation', 'en')], range=ItemDatatype())
Shareholder = Property(IRI('https://database.factgrid.de/entity/P1210'), ItemDatatype()).register(labels=[Text('Shareholder', 'en')], range=ItemDatatype())
Shares_border_with = Property(IRI('https://database.factgrid.de/entity/P1176'), ItemDatatype()).register(labels=[Text('Shares border with', 'en')], range=ItemDatatype())
short_digest = Property(IRI('https://database.factgrid.de/entity/P1148'), TextDatatype()).register(labels=[Text('short digest', 'en')], range=TextDatatype())
Short_reference = Property(IRI('https://database.factgrid.de/entity/P808'), TextDatatype()).register(labels=[Text('Short reference', 'en')], range=TextDatatype())
Siblings = Property(IRI('https://database.factgrid.de/entity/P203'), ItemDatatype()).register(labels=[Text('Sibling(s)', 'en')], range=ItemDatatype())
Signature = Property(IRI('https://database.factgrid.de/entity/P1267'), StringDatatype()).register(labels=[Text('Signature', 'en')], range=StringDatatype())
Signed_by = Property(IRI('https://database.factgrid.de/entity/P410'), ItemDatatype()).register(labels=[Text('Signed by', 'en')], range=ItemDatatype())
Silver_content = Property(IRI('https://database.factgrid.de/entity/P403'), QuantityDatatype()).register(labels=[Text('Silver content', 'en')], range=QuantityDatatype())
SIMC_ID = Property(IRI('https://database.factgrid.de/entity/P962'), ExternalIdDatatype()).register(labels=[Text('SIMC ID', 'en')], range=ExternalIdDatatype())
Skin_colour = Property(IRI('https://database.factgrid.de/entity/P642'), ItemDatatype()).register(labels=[Text('Skin colour', 'en')], range=ItemDatatype())
Social_status = Property(IRI('https://database.factgrid.de/entity/P581'), ItemDatatype()).register(labels=[Text('Social status', 'en')], range=ItemDatatype())
Software = Property(IRI('https://database.factgrid.de/entity/P819'), ItemDatatype()).register(labels=[Text('Software', 'en')], range=ItemDatatype())
Sort_by = Property(IRI('https://database.factgrid.de/entity/P249'), ItemDatatype()).register(labels=[Text('Sort by', 'en')], range=ItemDatatype())
Sort_string = Property(IRI('https://database.factgrid.de/entity/P101'), StringDatatype()).register(labels=[Text('Sort string', 'en')], range=StringDatatype())
Source_based_classification = Property(IRI('https://database.factgrid.de/entity/P582'), ItemDatatype()).register(labels=[Text('Source-based classification', 'en')], range=ItemDatatype())
Source_literal = Property(IRI('https://database.factgrid.de/entity/P721'), StringDatatype()).register(labels=[Text('Source [literal]', 'en')], range=StringDatatype())
Spanish_Biographical_Dictionary_ID = Property(IRI('https://database.factgrid.de/entity/P707'), ExternalIdDatatype()).register(labels=[Text('Spanish Biographical Dictionary ID', 'en')], range=ExternalIdDatatype())
SPARQL_endpoint_URL = Property(IRI('https://database.factgrid.de/entity/P941'), IRI_Datatype()).register(labels=[Text('SPARQL endpoint URL', 'en')], range=IRI_Datatype())
Specific_data_set = Property(IRI('https://database.factgrid.de/entity/P276'), ItemDatatype()).register(labels=[Text('Specific data set', 'en')], range=ItemDatatype())
Specific_statement = Property(IRI('https://database.factgrid.de/entity/P166'), ItemDatatype()).register(labels=[Text('Specific statement', 'en')], range=ItemDatatype())
Specification = Property(IRI('https://database.factgrid.de/entity/P382'), ItemDatatype()).register(labels=[Text('Specification', 'en')], range=ItemDatatype())
Speech_act_qualities = Property(IRI('https://database.factgrid.de/entity/P912'), ItemDatatype()).register(labels=[Text('Speech act qualities', 'en')], range=ItemDatatype())
Sphere_in_life = Property(IRI('https://database.factgrid.de/entity/P569'), ItemDatatype()).register(labels=[Text('Sphere in life', 'en')], range=ItemDatatype())
Split_off = Property(IRI('https://database.factgrid.de/entity/P457'), ItemDatatype()).register(labels=[Text('Split-off', 'en')], range=ItemDatatype())
Split_off_from = Property(IRI('https://database.factgrid.de/entity/P458'), ItemDatatype()).register(labels=[Text('Split-off from', 'en')], range=ItemDatatype())
Sponsor_supporter = Property(IRI('https://database.factgrid.de/entity/P735'), ItemDatatype()).register(labels=[Text('Sponsor / supporter', 'en')], range=ItemDatatype())
SS_KL_Auschwitz_Garrison_ID = Property(IRI('https://database.factgrid.de/entity/P1195'), ExternalIdDatatype()).register(labels=[Text('SS KL Auschwitz Garrison ID', 'en')], range=ExternalIdDatatype())
SS_membership_number = Property(IRI('https://database.factgrid.de/entity/P1191'), ExternalIdDatatype()).register(labels=[Text('SS membership number', 'en')], range=ExternalIdDatatype())
SS_Resettlement_ID = Property(IRI('https://database.factgrid.de/entity/P1196'), ExternalIdDatatype()).register(labels=[Text('SS Resettlement ID', 'en')], range=ExternalIdDatatype())
SSNE_person_ID = Property(IRI('https://database.factgrid.de/entity/P816'), ExternalIdDatatype()).register(labels=[Text('SSNE person ID', 'en')], range=ExternalIdDatatype())
Standardised_evaluation = Property(IRI('https://database.factgrid.de/entity/P990'), ItemDatatype()).register(labels=[Text('Standardised evaluation', 'en')], range=ItemDatatype())
Start_time_of_reported_events = Property(IRI('https://database.factgrid.de/entity/P45'), TimeDatatype()).register(labels=[Text('Start time of reported events', 'en')], range=TimeDatatype())
State_bibliographical = Property(IRI('https://database.factgrid.de/entity/P770'), StringDatatype()).register(labels=[Text('* State (bibliographical)', 'en')], range=StringDatatype())
State_of_conservation_literal = Property(IRI('https://database.factgrid.de/entity/P769'), StringDatatype()).register(labels=[Text('State of conservation [literal]', 'en')], range=StringDatatype())
State_of_work = Property(IRI('https://database.factgrid.de/entity/P263'), ItemDatatype()).register(labels=[Text('State of work', 'en')], range=ItemDatatype())
Statement_denied_by = Property(IRI('https://database.factgrid.de/entity/P1160'), ItemDatatype()).register(labels=[Text('Statement denied by', 'en')], range=ItemDatatype())
Statement_refers_to = Property(IRI('https://database.factgrid.de/entity/P1142'), StringDatatype()).register(labels=[Text('* Statement refers to', 'en')], range=StringDatatype())
Statement_refers_to = Property(IRI('https://database.factgrid.de/entity/P700'), ItemDatatype()).register(labels=[Text('Statement refers to', 'en')], range=ItemDatatype())
Statements_to_be_verified_in_this_data_set = Property(IRI('https://database.factgrid.de/entity/P857'), PropertyDatatype()).register(labels=[Text('Statements to be verified in this data set', 'en')], range=PropertyDatatype())
Stature = Property(IRI('https://database.factgrid.de/entity/P639'), ItemDatatype()).register(labels=[Text('Stature', 'en')], range=ItemDatatype())
Status = Property(IRI('https://database.factgrid.de/entity/P560'), ItemDatatype()).register(labels=[Text('Status', 'en')], range=ItemDatatype())
Status_of_possesion = Property(IRI('https://database.factgrid.de/entity/P127'), ItemDatatype()).register(labels=[Text('Status of possesion', 'en')], range=ItemDatatype())
Stay_in = Property(IRI('https://database.factgrid.de/entity/P296'), ItemDatatype()).register(labels=[Text('Stay in', 'en')], range=ItemDatatype())
Stored_in = Property(IRI('https://database.factgrid.de/entity/P226'), ItemDatatype()).register(labels=[Text('Stored in', 'en')], range=ItemDatatype())
Street_square = Property(IRI('https://database.factgrid.de/entity/P522'), ItemDatatype()).register(labels=[Text('Street/square', 'en')], range=ItemDatatype())
Strict_Observance_order_name = Property(IRI('https://database.factgrid.de/entity/P363'), ItemDatatype()).register(labels=[Text('Strict Observance order name', 'en')], range=ItemDatatype())
Strict_Observance_order_name_of = Property(IRI('https://database.factgrid.de/entity/P148'), ItemDatatype()).register(labels=[Text('Strict Observance order name of', 'en')], range=ItemDatatype())
Structural_hierarchies_implemented = Property(IRI('https://database.factgrid.de/entity/P359'), ItemDatatype()).register(labels=[Text('Structural hierarchies implemented', 'en')], range=ItemDatatype())
Student = Property(IRI('https://database.factgrid.de/entity/P190'), ItemDatatype()).register(labels=[Text('Student', 'en')], range=ItemDatatype())
Student_of = Property(IRI('https://database.factgrid.de/entity/P161'), ItemDatatype()).register(labels=[Text('Student of', 'en')], range=ItemDatatype())
Styrian_State_Library_ID = Property(IRI('https://database.factgrid.de/entity/P1224'), ExternalIdDatatype()).register(labels=[Text('Styrian State Library ID', 'en')], range=ExternalIdDatatype())
Subclass_of = Property(IRI('https://database.factgrid.de/entity/P3'), ItemDatatype()).register(labels=[Text('Subclass of', 'en')], range=ItemDatatype())
Subject_evicted = Property(IRI('https://database.factgrid.de/entity/P1199'), ItemDatatype()).register(labels=[Text('Subject evicted', 'en')], range=ItemDatatype())
Subject_has_role = Property(IRI('https://database.factgrid.de/entity/P277'), ItemDatatype()).register(labels=[Text('Subject has role', 'en')], range=ItemDatatype())
Subject_heading = Property(IRI('https://database.factgrid.de/entity/P422'), ItemDatatype()).register(labels=[Text('Subject heading', 'en')], range=ItemDatatype())
Subject_matter = Property(IRI('https://database.factgrid.de/entity/P576'), ItemDatatype()).register(labels=[Text('Subject matter', 'en')], range=ItemDatatype())
Subject_matter_that_raised_objections = Property(IRI('https://database.factgrid.de/entity/P676'), ItemDatatype()).register(labels=[Text('Subject matter that raised objections', 'en')], range=ItemDatatype())
Subject_of_negotiation = Property(IRI('https://database.factgrid.de/entity/P674'), ItemDatatype()).register(labels=[Text('Subject of negotiation', 'en')], range=ItemDatatype())
Subject_paid = Property(IRI('https://database.factgrid.de/entity/P879'), QuantityDatatype()).register(labels=[Text('Subject paid', 'en')], range=QuantityDatatype())
Subject_studied_at_university = Property(IRI('https://database.factgrid.de/entity/P304'), ItemDatatype()).register(labels=[Text('Subject studied at university', 'en')], range=ItemDatatype())
Subject_topic_heading = Property(IRI('https://database.factgrid.de/entity/P1094'), TextDatatype()).register(labels=[Text('Subject / topic / heading', 'en')], range=TextDatatype())
Subjected = Property(IRI('https://database.factgrid.de/entity/P751'), ItemDatatype()).register(labels=[Text('Subjected', 'en')], range=ItemDatatype())
Subjected_to = Property(IRI('https://database.factgrid.de/entity/P550'), ItemDatatype()).register(labels=[Text('Subjected to', 'en')], range=ItemDatatype())
Subproperties = Property(IRI('https://database.factgrid.de/entity/P451'), PropertyDatatype()).register(labels=[Text('Subproperties', 'en')], range=PropertyDatatype())
Subproperty_of = Property(IRI('https://database.factgrid.de/entity/P450'), PropertyDatatype()).register(labels=[Text('Subproperty of', 'en')], range=PropertyDatatype())
Subscribers = Property(IRI('https://database.factgrid.de/entity/P275'), ItemDatatype()).register(labels=[Text('Subscribers', 'en')], range=ItemDatatype())
Subscription_text = Property(IRI('https://database.factgrid.de/entity/P282'), StringDatatype()).register(labels=[Text('Subscription text', 'en')], range=StringDatatype())
Subscriptions_signed = Property(IRI('https://database.factgrid.de/entity/P278'), ItemDatatype()).register(labels=[Text('Subscriptions signed', 'en')], range=ItemDatatype())
Subsidiary = Property(IRI('https://database.factgrid.de/entity/P419'), ItemDatatype()).register(labels=[Text('Subsidiary', 'en')], range=ItemDatatype())
Subunit_of = Property(IRI('https://database.factgrid.de/entity/P13'), ItemDatatype()).register(labels=[Text('Subunit of', 'en')], range=ItemDatatype())
Subunits = Property(IRI('https://database.factgrid.de/entity/P399'), ItemDatatype()).register(labels=[Text('Subunits', 'en')], range=ItemDatatype())
Supplied_by = Property(IRI('https://database.factgrid.de/entity/P1212'), ItemDatatype()).register(labels=[Text('Supplied by', 'en')], range=ItemDatatype())
Supplied_forced_laborers_for = Property(IRI('https://database.factgrid.de/entity/P1172'), ItemDatatype()).register(labels=[Text('Supplied forced laborers for', 'en')], range=ItemDatatype())
Surviving_copies = Property(IRI('https://database.factgrid.de/entity/P840'), ItemDatatype()).register(labels=[Text('Surviving copies', 'en')], range=ItemDatatype())
Sustainability = Property(IRI('https://database.factgrid.de/entity/P999'), ItemDatatype()).register(labels=[Text('Sustainability', 'en')], range=ItemDatatype())
Swedish_portrait_archive_ID = Property(IRI('https://database.factgrid.de/entity/P379'), ExternalIdDatatype()).register(labels=[Text('Swedish portrait archive ID', 'en')], range=ExternalIdDatatype())
Swedish_small_places_ID = Property(IRI('https://database.factgrid.de/entity/P529'), ExternalIdDatatype()).register(labels=[Text('Swedish small places ID', 'en')], range=ExternalIdDatatype())
Swedish_urban_area_code = Property(IRI('https://database.factgrid.de/entity/P528'), ExternalIdDatatype()).register(labels=[Text('Swedish urban area code', 'en')], range=ExternalIdDatatype())
Swiss_municipality_code = Property(IRI('https://database.factgrid.de/entity/P1081'), ExternalIdDatatype()).register(labels=[Text('Swiss municipality code', 'en')], range=ExternalIdDatatype())
Symbolises = Property(IRI('https://database.factgrid.de/entity/P1349'), ItemDatatype()).register(labels=[Text('Symbolises', 'en')], range=ItemDatatype())
Synonym = Property(IRI('https://database.factgrid.de/entity/P815'), ItemDatatype()).register(labels=[Text('Synonym', 'en')], range=ItemDatatype())
System_component_of = Property(IRI('https://database.factgrid.de/entity/P372'), ItemDatatype()).register(labels=[Text('System component of', 'en')], range=ItemDatatype())
Sächsische_Biografie_ID = Property(IRI('https://database.factgrid.de/entity/P1328'), ExternalIdDatatype()).register(labels=[Text('Sächsische Biografie ID', 'en')], range=ExternalIdDatatype())
Süddeutsche_Patrizier_Datenbank_ID = Property(IRI('https://database.factgrid.de/entity/P1244'), ExternalIdDatatype()).register(labels=[Text('Süddeutsche Patrizier Datenbank-ID', 'en')], range=ExternalIdDatatype())
Target_group_person = Property(IRI('https://database.factgrid.de/entity/P573'), ItemDatatype()).register(labels=[Text('Target group / person', 'en')], range=ItemDatatype())
Target_language = Property(IRI('https://database.factgrid.de/entity/P213'), ItemDatatype()).register(labels=[Text('Target language', 'en')], range=ItemDatatype())
Tax_per_annum = Property(IRI('https://database.factgrid.de/entity/P944'), QuantityDatatype()).register(labels=[Text('Tax (per annum)', 'en')], range=QuantityDatatype())
Taxable_assets = Property(IRI('https://database.factgrid.de/entity/P1324'), QuantityDatatype()).register(labels=[Text('Taxable assets', 'en')], range=QuantityDatatype())
Taxon_range = Property(IRI('https://database.factgrid.de/entity/P1158'), ItemDatatype()).register(labels=[Text('Taxon range', 'en')], range=ItemDatatype())
Taxonomic_name = Property(IRI('https://database.factgrid.de/entity/P632'), StringDatatype()).register(labels=[Text('Taxonomic name', 'en')], range=StringDatatype())
Taxonomic_rank = Property(IRI('https://database.factgrid.de/entity/P294'), ItemDatatype()).register(labels=[Text('Taxonomic rank', 'en')], range=ItemDatatype())
Team = Property(IRI('https://database.factgrid.de/entity/P178'), ItemDatatype()).register(labels=[Text('Team', 'en')], range=ItemDatatype())
Technology = Property(IRI('https://database.factgrid.de/entity/P940'), ItemDatatype()).register(labels=[Text('Technology', 'en')], range=ItemDatatype())
Teeth = Property(IRI('https://database.factgrid.de/entity/P1394'), ItemDatatype()).register(labels=[Text('Teeth', 'en')], range=ItemDatatype())
TEI_ID = Property(IRI('https://database.factgrid.de/entity/P535'), ExternalIdDatatype()).register(labels=[Text('TEI ID', 'en')], range=ExternalIdDatatype())
Telephone_number = Property(IRI('https://database.factgrid.de/entity/P846'), StringDatatype()).register(labels=[Text('Telephone number', 'en')], range=StringDatatype())
Term_attributed_by = Property(IRI('https://database.factgrid.de/entity/P421'), ItemDatatype()).register(labels=[Text('Term attributed by', 'en')], range=ItemDatatype())
Term_for_practitioner = Property(IRI('https://database.factgrid.de/entity/P1276'), ItemDatatype()).register(labels=[Text('Term for practitioner', 'en')], range=ItemDatatype())
Term_for_the_academic_expert = Property(IRI('https://database.factgrid.de/entity/P1279'), ItemDatatype()).register(labels=[Text('Term for the academic expert', 'en')], range=ItemDatatype())
Term_for_the_field_of_study = Property(IRI('https://database.factgrid.de/entity/P1278'), ItemDatatype()).register(labels=[Text('Term for the field of study', 'en')], range=ItemDatatype())
Term_for_the_group_practicing = Property(IRI('https://database.factgrid.de/entity/P1277'), ItemDatatype()).register(labels=[Text('Term for the group practicing', 'en')], range=ItemDatatype())
Term_for_the_ideology = Property(IRI('https://database.factgrid.de/entity/P1282'), ItemDatatype()).register(labels=[Text('Term for the ideology', 'en')], range=ItemDatatype())
Term_for_the_institution = Property(IRI('https://database.factgrid.de/entity/P1283'), ItemDatatype()).register(labels=[Text('Term for the institution', 'en')], range=ItemDatatype())
Term_for_the_object_of_knowledge = Property(IRI('https://database.factgrid.de/entity/P1281'), ItemDatatype()).register(labels=[Text('Term for the object of knowledge', 'en')], range=ItemDatatype())
Territorial_localisation = Property(IRI('https://database.factgrid.de/entity/P297'), ItemDatatype()).register(labels=[Text('Territorial localisation', 'en')], range=ItemDatatype())
Territory_granting_the_indigenate = Property(IRI('https://database.factgrid.de/entity/P523'), ItemDatatype()).register(labels=[Text('Territory granting the indigenate', 'en')], range=ItemDatatype())
Test_property_url = Property(IRI('https://database.factgrid.de/entity/P1379'), IRI_Datatype()).register(labels=[Text('Test property url', 'en')], range=IRI_Datatype())
Text_justification_legal_basis_constitution = Property(IRI('https://database.factgrid.de/entity/P555'), ItemDatatype()).register(labels=[Text('Text justification / legal basis / constitution', 'en')], range=ItemDatatype())
Text_source = Property(IRI('https://database.factgrid.de/entity/P311'), ItemDatatype()).register(labels=[Text('Text source', 'en')], range=ItemDatatype())
Texts_depicting_staging_the_subject = Property(IRI('https://database.factgrid.de/entity/P762'), ItemDatatype()).register(labels=[Text('Texts depicting/staging the subject', 'en')], range=ItemDatatype())
Texts_mentioned = Property(IRI('https://database.factgrid.de/entity/P116'), ItemDatatype()).register(labels=[Text('Texts mentioned', 'en')], range=ItemDatatype())
Thesis = Property(IRI('https://database.factgrid.de/entity/P99'), StringDatatype()).register(labels=[Text('Thesis', 'en')], range=StringDatatype())
Things_and_places_mentioned = Property(IRI('https://database.factgrid.de/entity/P256'), ItemDatatype()).register(labels=[Text('Things and places mentioned', 'en')], range=ItemDatatype())
Time_of_day = Property(IRI('https://database.factgrid.de/entity/P509'), StringDatatype()).register(labels=[Text('Time of day', 'en')], range=StringDatatype())
Timestamp = Property(IRI('https://database.factgrid.de/entity/P1241'), QuantityDatatype()).register(labels=[Text('Timestamp', 'en')], range=QuantityDatatype())
Title = Property(IRI('https://database.factgrid.de/entity/P11'), StringDatatype()).register(labels=[Text('Title', 'en')], range=StringDatatype())
Title_aspects = Property(IRI('https://database.factgrid.de/entity/P572'), ItemDatatype()).register(labels=[Text('Title aspects', 'en')], range=ItemDatatype())
Title_page_transcript = Property(IRI('https://database.factgrid.de/entity/P5'), StringDatatype()).register(labels=[Text('Title page transcript', 'en')], range=StringDatatype())
to = Property(IRI('https://database.factgrid.de/entity/P1346'), ItemDatatype()).register(labels=[Text('to', 'en')], range=ItemDatatype())
Topic = Property(IRI('https://database.factgrid.de/entity/P243'), ItemDatatype()).register(labels=[Text('Topic', 'en')], range=ItemDatatype())
Total_assets = Property(IRI('https://database.factgrid.de/entity/P1234'), QuantityDatatype()).register(labels=[Text('Total assets', 'en')], range=QuantityDatatype())
Total_revenue = Property(IRI('https://database.factgrid.de/entity/P1235'), QuantityDatatype()).register(labels=[Text('Total revenue', 'en')], range=QuantityDatatype())
Total_valid_votes = Property(IRI('https://database.factgrid.de/entity/P1312'), QuantityDatatype()).register(labels=[Text('Total valid votes', 'en')], range=QuantityDatatype())
Transacted_object = Property(IRI('https://database.factgrid.de/entity/P1201'), ItemDatatype()).register(labels=[Text('Transacted object', 'en')], range=ItemDatatype())
Transcribed_by = Property(IRI('https://database.factgrid.de/entity/P68'), ItemDatatype()).register(labels=[Text('Transcribed by', 'en')], range=ItemDatatype())
Translation = Property(IRI('https://database.factgrid.de/entity/P71'), ItemDatatype()).register(labels=[Text('Translation', 'en')], range=ItemDatatype())
Translation_literal = Property(IRI('https://database.factgrid.de/entity/P298'), TextDatatype()).register(labels=[Text('Translation [literal]', 'en')], range=TextDatatype())
Translation_of = Property(IRI('https://database.factgrid.de/entity/P63'), ItemDatatype()).register(labels=[Text('Translation of', 'en')], range=ItemDatatype())
Translator = Property(IRI('https://database.factgrid.de/entity/P24'), ItemDatatype()).register(labels=[Text('Translator', 'en')], range=ItemDatatype())
Translator_as_misleadingly_stated = Property(IRI('https://database.factgrid.de/entity/P583'), ItemDatatype()).register(labels=[Text('Translator as misleadingly stated', 'en')], range=ItemDatatype())
Transliteration = Property(IRI('https://database.factgrid.de/entity/P1155'), TextDatatype()).register(labels=[Text('Transliteration', 'en')], range=TextDatatype())
Transmitted_by = Property(IRI('https://database.factgrid.de/entity/P134'), ItemDatatype()).register(labels=[Text('Transmitted by', 'en')], range=ItemDatatype())
Transparency = Property(IRI('https://database.factgrid.de/entity/P829'), ItemDatatype()).register(labels=[Text('Transparency', 'en')], range=ItemDatatype())
Transparency_of_the_information_provided = Property(IRI('https://database.factgrid.de/entity/P828'), ItemDatatype()).register(labels=[Text('Transparency of the information provided', 'en')], range=ItemDatatype())
Transport_connection = Property(IRI('https://database.factgrid.de/entity/P571'), ItemDatatype()).register(labels=[Text('Transport connection', 'en')], range=ItemDatatype())
Transport_connection_from = Property(IRI('https://database.factgrid.de/entity/P971'), ItemDatatype()).register(labels=[Text('Transport connection from', 'en')], range=ItemDatatype())
Transport_connection_to = Property(IRI('https://database.factgrid.de/entity/P972'), ItemDatatype()).register(labels=[Text('Transport connection to', 'en')], range=ItemDatatype())
Tribe = Property(IRI('https://database.factgrid.de/entity/P494'), ItemDatatype()).register(labels=[Text('Tribe', 'en')], range=ItemDatatype())
Troop_contributors = Property(IRI('https://database.factgrid.de/entity/P981'), ItemDatatype()).register(labels=[Text('Troop contributors', 'en')], range=ItemDatatype())
Troop_strength = Property(IRI('https://database.factgrid.de/entity/P957'), QuantityDatatype()).register(labels=[Text('Troop strength', 'en')], range=QuantityDatatype())
Truth_context = Property(IRI('https://database.factgrid.de/entity/P225'), ItemDatatype()).register(labels=[Text('Truth context', 'en')], range=ItemDatatype())
Twitter_X_handle = Property(IRI('https://database.factgrid.de/entity/P433'), ExternalIdDatatype()).register(labels=[Text('Twitter / X handle', 'en')], range=ExternalIdDatatype())
Type_of_event = Property(IRI('https://database.factgrid.de/entity/P442'), ItemDatatype()).register(labels=[Text('Type of event', 'en')], range=ItemDatatype())
Type_of_legal_act = Property(IRI('https://database.factgrid.de/entity/P1254'), ItemDatatype()).register(labels=[Text('Type of legal act', 'en')], range=ItemDatatype())
Type_of_publication = Property(IRI('https://database.factgrid.de/entity/P144'), ItemDatatype()).register(labels=[Text('Type of publication', 'en')], range=ItemDatatype())
Type_of_term = Property(IRI('https://database.factgrid.de/entity/P147'), ItemDatatype()).register(labels=[Text('Type of term', 'en')], range=ItemDatatype())
Type_of_treatment = Property(IRI('https://database.factgrid.de/entity/P792'), ItemDatatype()).register(labels=[Text('Type of treatment', 'en')], range=ItemDatatype())
Type_of_work = Property(IRI('https://database.factgrid.de/entity/P121'), ItemDatatype()).register(labels=[Text('Type of work', 'en')], range=ItemDatatype())
Typeface = Property(IRI('https://database.factgrid.de/entity/P748'), ItemDatatype()).register(labels=[Text('Typeface', 'en')], range=ItemDatatype())
Typology = Property(IRI('https://database.factgrid.de/entity/P754'), ItemDatatype()).register(labels=[Text('Typology', 'en')], range=ItemDatatype())
Under_the_rule_of = Property(IRI('https://database.factgrid.de/entity/P925'), ItemDatatype()).register(labels=[Text('Under the rule of', 'en')], range=ItemDatatype())
Underlying_problem = Property(IRI('https://database.factgrid.de/entity/P677'), ItemDatatype()).register(labels=[Text('Underlying problem', 'en')], range=ItemDatatype())
Union_List_of_Artist_Names_ID = Property(IRI('https://database.factgrid.de/entity/P1289'), ExternalIdDatatype()).register(labels=[Text('Union List of Artist Names ID', 'en')], range=ExternalIdDatatype())
University_Collections_in_Germany_ID = Property(IRI('https://database.factgrid.de/entity/P1290'), ExternalIdDatatype()).register(labels=[Text('University Collections in Germany ID', 'en')], range=ExternalIdDatatype())
URL = Property(IRI('https://database.factgrid.de/entity/P887'), IRI_Datatype()).register(labels=[Text('URL', 'en')], range=IRI_Datatype())
URL_links_to = Property(IRI('https://database.factgrid.de/entity/P850'), ItemDatatype()).register(labels=[Text('URL links to', 'en')], range=ItemDatatype())
URN_formatter = Property(IRI('https://database.factgrid.de/entity/P744'), StringDatatype()).register(labels=[Text('URN formatter', 'en')], range=StringDatatype())
Use_functionality = Property(IRI('https://database.factgrid.de/entity/P280'), ItemDatatype()).register(labels=[Text('Use / functionality', 'en')], range=ItemDatatype())
Used_forced_labor_from = Property(IRI('https://database.factgrid.de/entity/P1171'), ItemDatatype()).register(labels=[Text('Used forced labor from', 'en')], range=ItemDatatype())
Users = Property(IRI('https://database.factgrid.de/entity/P1095'), ItemDatatype()).register(labels=[Text('Users', 'en')], range=ItemDatatype())
USTC_editions_ID = Property(IRI('https://database.factgrid.de/entity/P647'), ExternalIdDatatype()).register(labels=[Text('USTC editions ID', 'en')], range=ExternalIdDatatype())
Value_price = Property(IRI('https://database.factgrid.de/entity/P545'), QuantityDatatype()).register(labels=[Text('Value / price', 'en')], range=QuantityDatatype())
Variant = Property(IRI('https://database.factgrid.de/entity/P901'), ItemDatatype()).register(labels=[Text('Variant', 'en')], range=ItemDatatype())
Vasserot_ID_streets_of_Paris = Property(IRI('https://database.factgrid.de/entity/P1193'), ExternalIdDatatype()).register(labels=[Text('Vasserot ID (streets of Paris)', 'en')], range=ExternalIdDatatype())
VD16_ID = Property(IRI('https://database.factgrid.de/entity/P368'), ExternalIdDatatype()).register(labels=[Text('VD16 ID', 'en')], range=ExternalIdDatatype())
VD17_ID = Property(IRI('https://database.factgrid.de/entity/P369'), ExternalIdDatatype()).register(labels=[Text('VD17 ID', 'en')], range=ExternalIdDatatype())
VD18_ID = Property(IRI('https://database.factgrid.de/entity/P370'), ExternalIdDatatype()).register(labels=[Text('VD18 ID', 'en')], range=ExternalIdDatatype())
Verdict = Property(IRI('https://database.factgrid.de/entity/P483'), ItemDatatype()).register(labels=[Text('Verdict', 'en')], range=ItemDatatype())
Vergue_ID = Property(IRI('https://database.factgrid.de/entity/P660'), ExternalIdDatatype()).register(labels=[Text('Vergue ID', 'en')], range=ExternalIdDatatype())
Verkaufspreis = Property(IRI('https://database.factgrid.de/entity/P1168'), QuantityDatatype()).register(labels=[Text('Verkaufspreis', 'en')], range=QuantityDatatype())
Versioning = Property(IRI('https://database.factgrid.de/entity/P939'), ItemDatatype()).register(labels=[Text('Versioning', 'en')], range=ItemDatatype())
Versions_of_this_work = Property(IRI('https://database.factgrid.de/entity/P838'), ItemDatatype()).register(labels=[Text('Versions of this work', 'en')], range=ItemDatatype())
VIAF_ID = Property(IRI('https://database.factgrid.de/entity/P378'), ExternalIdDatatype()).register(labels=[Text('VIAF ID', 'en')], range=ExternalIdDatatype())
Victims_of_NS_Medical_Research_ID = Property(IRI('https://database.factgrid.de/entity/P1273'), ExternalIdDatatype()).register(labels=[Text('Victims of NS Medical Research ID', 'en')], range=ExternalIdDatatype())
Visual_work_component = Property(IRI('https://database.factgrid.de/entity/P801'), ItemDatatype()).register(labels=[Text('Visual work component', 'en')], range=ItemDatatype())
Visual_work_components_by = Property(IRI('https://database.factgrid.de/entity/P611'), ItemDatatype()).register(labels=[Text('Visual work components by', 'en')], range=ItemDatatype())
Voice_type = Property(IRI('https://database.factgrid.de/entity/P638'), ItemDatatype()).register(labels=[Text('Voice type', 'en')], range=ItemDatatype())
Volksbund_Gräbersuche_Online_ID = Property(IRI('https://database.factgrid.de/entity/P1369'), ExternalIdDatatype()).register(labels=[Text('Volksbund Gräbersuche Online ID', 'en')], range=ExternalIdDatatype())
Volume = Property(IRI('https://database.factgrid.de/entity/P105'), StringDatatype()).register(labels=[Text('Volume', 'en')], range=StringDatatype())
Volume_as_a_quantity = Property(IRI('https://database.factgrid.de/entity/P1091'), QuantityDatatype()).register(labels=[Text('Volume as a quantity', 'en')], range=QuantityDatatype())
War_deployment = Property(IRI('https://database.factgrid.de/entity/P426'), ItemDatatype()).register(labels=[Text('War deployment', 'en')], range=ItemDatatype())
Watermark = Property(IRI('https://database.factgrid.de/entity/P749'), ItemDatatype()).register(labels=[Text('Watermark', 'en')], range=ItemDatatype())
Weapons_category = Property(IRI('https://database.factgrid.de/entity/P967'), ItemDatatype()).register(labels=[Text('Weapons category', 'en')], range=ItemDatatype())
Webhosting = Property(IRI('https://database.factgrid.de/entity/P947'), ItemDatatype()).register(labels=[Text('Webhosting', 'en')], range=ItemDatatype())
Weekday = Property(IRI('https://database.factgrid.de/entity/P973'), ItemDatatype()).register(labels=[Text('Weekday', 'en')], range=ItemDatatype())
Well_Known_Text_Geometry = Property(IRI('https://database.factgrid.de/entity/P1035'), StringDatatype()).register(labels=[Text('Well-Known Text Geometry', 'en')], range=StringDatatype())
What_supports_this_identification = Property(IRI('https://database.factgrid.de/entity/P118'), ItemDatatype()).register(labels=[Text('What supports this identification', 'en')], range=ItemDatatype())
Where_started_or_produced = Property(IRI('https://database.factgrid.de/entity/P95'), ItemDatatype()).register(labels=[Text('Where started or produced?', 'en')], range=ItemDatatype())
WIAG_ID = Property(IRI('https://database.factgrid.de/entity/P601'), ExternalIdDatatype()).register(labels=[Text('WIAG ID', 'en')], range=ExternalIdDatatype())
WIAG_Office_in_Sequence_ID = Property(IRI('https://database.factgrid.de/entity/P1100'), ExternalIdDatatype()).register(labels=[Text('WIAG Office in Sequence ID', 'en')], range=ExternalIdDatatype())
Wider_field_of_genres = Property(IRI('https://database.factgrid.de/entity/P122'), ItemDatatype()).register(labels=[Text('Wider field of genres', 'en')], range=ItemDatatype())
Width = Property(IRI('https://database.factgrid.de/entity/P60'), QuantityDatatype()).register(labels=[Text('Width', 'en')], range=QuantityDatatype())
Wikibase_Browser = Property(IRI('https://database.factgrid.de/entity/P992'), IRI_Datatype()).register(labels=[Text('Wikibase Browser', 'en')], range=IRI_Datatype())
Wikibase_World_Item_ID = Property(IRI('https://database.factgrid.de/entity/P977'), ExternalIdDatatype()).register(labels=[Text('Wikibase World Item ID', 'en')], range=ExternalIdDatatype())
Wikidata_Item = Property(IRI('https://database.factgrid.de/entity/P771'), ExternalIdDatatype()).register(labels=[Text('Wikidata Item', 'en')], range=ExternalIdDatatype())
Wikidata_lexeme = Property(IRI('https://database.factgrid.de/entity/P826'), ExternalIdDatatype()).register(labels=[Text('Wikidata lexeme', 'en')], range=ExternalIdDatatype())
Wikidata_property = Property(IRI('https://database.factgrid.de/entity/P343'), ExternalIdDatatype()).register(labels=[Text('Wikidata property', 'en')], range=ExternalIdDatatype())
Wikimedia_Commons_archival_document_reproductions = Property(IRI('https://database.factgrid.de/entity/P1089'), StringDatatype()).register(labels=[Text('Wikimedia Commons archival document reproductions', 'en')], range=StringDatatype())
Wikimedia_commons_exemplary_work = Property(IRI('https://database.factgrid.de/entity/P636'), StringDatatype()).register(labels=[Text('Wikimedia commons exemplary work', 'en')], range=StringDatatype())
Wikimedia_Commons_image_of_grave_or_memorial = Property(IRI('https://database.factgrid.de/entity/P556'), StringDatatype()).register(labels=[Text('Wikimedia Commons image of grave or memorial', 'en')], range=StringDatatype())
Wikimedia_Commons_Item_image = Property(IRI('https://database.factgrid.de/entity/P189'), StringDatatype()).register(labels=[Text('Wikimedia Commons Item image', 'en')], range=StringDatatype())
Wikimedia_language_code = Property(IRI('https://database.factgrid.de/entity/P53'), StringDatatype()).register(labels=[Text('Wikimedia language code', 'en')], range=StringDatatype())
Wikimedia_map_location = Property(IRI('https://database.factgrid.de/entity/P979'), StringDatatype()).register(labels=[Text('Wikimedia map location', 'en')], range=StringDatatype())
With_manuscript_notes_by = Property(IRI('https://database.factgrid.de/entity/P352'), ItemDatatype()).register(labels=[Text('With manuscript notes by', 'en')], range=ItemDatatype())
Without = Property(IRI('https://database.factgrid.de/entity/P706'), ItemDatatype()).register(labels=[Text('Without', 'en')], range=ItemDatatype())
Work_literal = Property(IRI('https://database.factgrid.de/entity/P1292'), TextDatatype()).register(labels=[Text('Work [literal]', 'en')], range=TextDatatype())
Work_location = Property(IRI('https://database.factgrid.de/entity/P1372'), ItemDatatype()).register(labels=[Text('Work location', 'en')], range=ItemDatatype())
Work_task_description = Property(IRI('https://database.factgrid.de/entity/P1256'), ItemDatatype()).register(labels=[Text('Work / task description', 'en')], range=ItemDatatype())
Work_to_be_subscribed = Property(IRI('https://database.factgrid.de/entity/P540'), ItemDatatype()).register(labels=[Text('Work to be subscribed', 'en')], range=ItemDatatype())
Works_published_or_unpublished = Property(IRI('https://database.factgrid.de/entity/P174'), ItemDatatype()).register(labels=[Text('Works, published or unpublished', 'en')], range=ItemDatatype())
WorldCat_Identities_ID = Property(IRI('https://database.factgrid.de/entity/P594'), ExternalIdDatatype()).register(labels=[Text('WorldCat Identities ID', 'en')], range=ExternalIdDatatype())
WorldCat_Registry_ID = Property(IRI('https://database.factgrid.de/entity/P376'), ExternalIdDatatype()).register(labels=[Text('WorldCat Registry ID', 'en')], range=ExternalIdDatatype())
WorldCat_Title_ID = Property(IRI('https://database.factgrid.de/entity/P827'), ExternalIdDatatype()).register(labels=[Text('WorldCat Title ID', 'en')], range=ExternalIdDatatype())
Worshipful_Master = Property(IRI('https://database.factgrid.de/entity/P342'), ItemDatatype()).register(labels=[Text('Worshipful Master', 'en')], range=ItemDatatype())
Writing_surface = Property(IRI('https://database.factgrid.de/entity/P480'), ItemDatatype()).register(labels=[Text('Writing surface', 'en')], range=ItemDatatype())
Württembergische_Kirchengeschichte_person_ID = Property(IRI('https://database.factgrid.de/entity/P1247'), ExternalIdDatatype()).register(labels=[Text('Württembergische Kirchengeschichte person ID', 'en')], range=ExternalIdDatatype())
X_numeric_user_ID = Property(IRI('https://database.factgrid.de/entity/P1269'), ExternalIdDatatype()).register(labels=[Text('X numeric user ID', 'en')], range=ExternalIdDatatype())
X_post_ID = Property(IRI('https://database.factgrid.de/entity/P1334'), ExternalIdDatatype()).register(labels=[Text('X post ID', 'en')], range=ExternalIdDatatype())
Yad_Vashem_Ghetto_ID = Property(IRI('https://database.factgrid.de/entity/P1181'), ExternalIdDatatype()).register(labels=[Text('Yad Vashem Ghetto ID', 'en')], range=ExternalIdDatatype())
Yad_Vashem_name_genealogy_ID = Property(IRI('https://database.factgrid.de/entity/P549'), ExternalIdDatatype()).register(labels=[Text('Yad Vashem name genealogy ID', 'en')], range=ExternalIdDatatype())
Year_of_the_time_frame = Property(IRI('https://database.factgrid.de/entity/P933'), QuantityDatatype()).register(labels=[Text('Year of the time frame', 'en')], range=QuantityDatatype())
YouTube_video_ID = Property(IRI('https://database.factgrid.de/entity/P1240'), ExternalIdDatatype()).register(labels=[Text('YouTube video ID', 'en')], range=ExternalIdDatatype())
Yu_Gi_Oh_Wiki_ID = Property(IRI('https://database.factgrid.de/entity/P1251'), ExternalIdDatatype()).register(labels=[Text('Yu-Gi-Oh! Wiki ID', 'en')], range=ExternalIdDatatype())
Zeitschriften_database_ID = Property(IRI('https://database.factgrid.de/entity/P1061'), ExternalIdDatatype()).register(labels=[Text('Zeitschriften database ID', 'en')], range=ExternalIdDatatype())
Zenodo_ID = Property(IRI('https://database.factgrid.de/entity/P1368'), ExternalIdDatatype()).register(labels=[Text('Zenodo ID', 'en')], range=ExternalIdDatatype())
ZOBODAT_People_ID = Property(IRI('https://database.factgrid.de/entity/P1357'), ExternalIdDatatype()).register(labels=[Text('ZOBODAT-People-ID', 'en')], range=ExternalIdDatatype())
ZOBODAT_Publication_Article_ID = Property(IRI('https://database.factgrid.de/entity/P1359'), ExternalIdDatatype()).register(labels=[Text('ZOBODAT-Publication-Article-ID', 'en')], range=ExternalIdDatatype())
ZOBODAT_Publication_Series_ID = Property(IRI('https://database.factgrid.de/entity/P1358'), ExternalIdDatatype()).register(labels=[Text('ZOBODAT-Publication Series-ID', 'en')], range=ExternalIdDatatype())
ZWAR_ID = Property(IRI('https://database.factgrid.de/entity/P1178'), ExternalIdDatatype()).register(labels=[Text('ZWAR ID', 'en')], range=ExternalIdDatatype())
ZWAR_Interview_ID = Property(IRI('https://database.factgrid.de/entity/P1186'), ExternalIdDatatype()).register(labels=[Text('ZWAR Interview-ID', 'en')], range=ExternalIdDatatype())
ÖSTAT_number = Property(IRI('https://database.factgrid.de/entity/P961'), ExternalIdDatatype()).register(labels=[Text('ÖSTAT number', 'en')], range=ExternalIdDatatype())

__all__ = (
"_1st_carry",
"_2nd_carry",
"_2nd_Qualifier",
"_3D_model_external",
"_3D_model_Wikimadia_Commons",
"Abbot",
"Abbreviation",
"Ability",
"Absent",
"Accessibility",
"Accession_number",
"Accounts_held_in",
"Accusation_of",
"Accuser",
"Acquired_name",
"Active_ingredient",
"Actual_statement",
"Actually_addressed_to",
"ADB_Wikisource",
"Additional_name_attributes",
"Addressees_of_deliveries",
"Adjectivisation",
"Administrative_localisation",
"Admission_requirement_required_membership",
"Adversary",
"Age_from",
"Age_statement",
"Age_up_to",
"Agency_or_person_that_gave_the_records",
"Agents_Agencies_involved",
"Akademie_der_Künste_Berlin_Member_ID",
"Album_Academicum_Altorphinum_ID",
"Alleged_member_of",
"Alternate_shelfmark",
"Alternatively",
"Amburger_database_ID",
"Amount_in_dispute",
"Amount_of_punishment",
"Amount_of_the_penalty_payment",
"Annex",
"Answer_on",
"Answered_with",
"Apartment",
"API_endpoint_URL",
"Applied_means",
"Apprenticeship_at",
"Appropriate_clothing",
"Approved_by",
"Archaeological_Project",
"Archival_collection",
"Archived_at_the_URL",
"Archives_at",
"Area",
"Area_changes_to",
"Area_ID",
"Aristocratic_tenures",
"Aristocratic_title",
"Arolsen_Archives_Document_ID",
"Arolsen_Archives_Persons_ID",
"Arrival",
"Art_and_Architecture_Thesaurus_ID",
"Article",
"Article_literal",
"Asiatic_Brethren_code_name_of",
"Associated_person",
"Associated_place",
"Authenticated_by",
"Authenticity_of_the_document_confirmed_by",
"Author",
"Author_as_strangely_stated",
"Autobiography_diaries",
"Average",
"BAG_code_for_Dutch_places_of_residence",
"Ballots_cast",
"Banns_of_marriage_date",
"Barcode",
"BARTOC_Vocabularies_ID",
"Based_on",
"Bavarikon_ID",
"Bayrisches_Musiker_Lexikon_Online_ID",
"BDTNS_ID",
"Bearer",
"Bearer_of_the_Coat_of_Arms",
"Begin_date",
"Begin_date_terminus_ante_quem",
"Begin_date_terminus_post_quem",
"Begin_text_span",
"Beginning_of_composition",
"Best_practice_notice",
"Bestellnummer_of_books_printed_in_the_GDR",
"Binding",
"Biographical_notes",
"Biographisches_Portal_der_Rabbiner_ID",
"Blood_type",
"Blueness_of_the_sky",
"BNE_ID",
"BnF_ID",
"Body_form",
"Bookbinding",
"Bookbinding_by",
"Bossu_ID",
"Buchenwald_satellite_camp_ID",
"Building_history",
"Business_partner_of",
"Can_mean",
"Canonization_status",
"Capacity",
"Capital",
"Capital_burden",
"Capital_of",
"Capital_return_of_the_property",
"Career_aspiration",
"Career_statement",
"CARLA_ID",
"Catalogus_Professorum_Dresdensis_ID",
"Catalogus_Professorum_Halensis_ID",
"Catalogus_Professorum_Hamburgensis_ID",
"Catholic_Hierarchy_ID",
"Catholic_religious_name",
"Catholic_religious_name_of",
"Cause_of_end",
"Cause_of_loss",
"CDLI_ID",
"CDLI_ID2",
"Celebrating",
"CERL_Thesaurus_ID",
"Check",
"Chemical_formula",
"Child",
"Child_raised",
"Choice_of_title_in_Prozent",
"Chronology",
"CIDOC_CRM_class",
"CIDOC_CRM_property",
"Circumcision_Date_religious",
"Circumstances_of_death",
"Cite_as",
"Citizen_of",
"City_Wiki_Dresden_ID",
"Claimbase_ID",
"Classification_by",
"classification_of_the_data_provider",
"Coat_of_arms",
"Coat_of_arms_family",
"Coding_key",
"Coin_equivalents",
"Collation",
"Collected_by",
"Collects_information_about",
"Colour",
"Columns",
"Commemorative_date",
"Commentator",
"Commissioned_by",
"Competent_Jurisdiction",
"Complementary_term_for_the_theoretical_collective",
"Complete_Bible_Genealogy_ID",
"Completeness",
"Complex_Evaluation",
"Composer",
"Composite_ID",
"Compulsory_obligation_towards",
"Conceptual_ramification",
"Conference_participations",
"Confirmed_by",
"Conflict_parties",
"Connection_to_preceding",
"Constituted_by",
"constraint_scope",
"Contact_person",
"Contains_documents_of",
"Contains_documents_of",
"Contemporary_witness_document",
"contemporary_witnesses_in_the_audience",
"Context",
"Continuation_of",
"Continued_by",
"Contributor",
"Contributor_to",
"Conversion_rates",
"Coordinate_location",
"Copy_of",
"Copy_of_this",
"Copyright_holder",
"Correlation",
"Cosignatory_in",
"Country_of_citizenship",
"Court_Tribunal",
"Cousin",
"Creator",
"Creator",
"Credit_receiver_of",
"CTHS_ID_person",
"CTHS_ID_society",
"Currency",
"Curriculum_Vitae",
"Customer",
"Customer_of",
"Czech_municipality_ID",
"Dachau_Memorial_Database",
"Dansk_Biografisk_Leksikon_ID",
"Data_BnF_ID",
"Data_download_link",
"Data_format",
"Data_set_wanting_a_statement_on",
"Data_size",
"database_of_Austrian_deportees_in_Auschwitz_ID",
"Database_of_Salon_Artists_person_ID",
"Dataset",
"Dataset_complaint",
"Dataset_editing",
"Dataset_status",
"Datatype",
"Date",
"Date_after",
"Date_as_stated",
"Date_as_stated",
"Date_before",
"Date_of_artifact",
"Date_of_baptism",
"Date_of_birth",
"Date_of_Blessing",
"Date_of_burial",
"Date_of_confirmation",
"Date_of_consecration_ordination",
"Date_of_creation",
"Date_of_death",
"Date_of_discovery_or_invention",
"Date_of_disputation",
"Date_of_ennoblement",
"Date_of_finding",
"Date_of_first_publication",
"Date_of_last_will",
"Date_of_premiere",
"Date_of_publication",
"Date_of_receipt",
"Date_of_retirement",
"Date_of_verdict",
"Daughter_lodges",
"Dedicated_day",
"Dedicatee",
"Dedicatee",
"Defender",
"Defined_equivalent",
"Definition",
"Degree_system",
"Degree_to_which_this_is_the_case",
"Degrees_worked",
"Den_Store_Danske_ID",
"Departure",
"Deportation_extradition_to",
"Depth_thickness",
"Design_features",
"Design_planning",
"Designed_to_state",
"Destination",
"Deutsche_Biographie_GND_ID",
"Deutsche_Digitale_Bibliothek_Item_ID",
"Deutsche_Digitale_Bibliothek_Person_ID",
"Deutsche_Fotothek_object_ID",
"Deutsche_Inschriften_Online_ID",
"Deutsches_Literaturarchiv_Marbach_ID",
"Deutsches_Rechtswörterbuch",
"Dewey_Decimal_Classification",
"DFG_subject_classification",
"Diameter",
"Diccionari_de_la_Literatura_Catalana_ID",
"Dictionary_of_Swedish_National_Biography_ID",
"Dictionnaire_des_journalistes_1600_1789_ID",
"Digest",
"Diocese",
"Discovered_invented_developed_by",
"Dissertation",
"Distance_between_addresses",
"Distant_participants",
"DNB_Info_ID",
"Docker_Hub_repository",
"Doctoral_supervisor",
"Document_attested_by",
"Documented_list_of_members",
"Documented_object",
"Documented_use_case",
"DOI",
"Donations_received",
"Download_link",
"Duration",
"Duration_of_the_prison_sentence",
"Earnings_before_interest_and_taxes",
"Ears",
"eBL_ID",
"Ecclesiastical_province",
"Eckard_Rolf_class_of_functional_text_types",
"Economic_sector_of_the_career_statement",
"Editions_series_productions",
"Editor_of",
"Editorial_responsibility",
"Educating_institution",
"Education_level_academic_degree",
"Edvard_Munchs_correspondance_person_ID",
"Effect_of",
"EHAK_ID",
"EHRI_camps_ID",
"EHRI_ghetto_ID",
"Einkaufspreis",
"Election_results_by_candidate",
"Elevation_above_sea_level",
"Eligible_voters",
"Email_contact_page",
"Employed_at",
"Employers_status",
"Encounter",
"End_date",
"End_date_terminus_ante_quem",
"End_date_terminus_post_quem",
"End_of_events_reported",
"End_text_span",
"Enzyklopädie_der_Russlanddeutschen_ID",
"epidat_ID",
"EPN",
"Equivalent_class",
"Equivalent_in_grams_of_copper",
"Equivalent_in_grams_of_gold",
"Equivalent_in_grams_of_silver",
"Equivalent_in_other_organizations",
"Equivalent_multilingual_item",
"Equivalent_property_elsewhere",
"Escape_emigration_to",
"Espacenet_ID_for_patents",
"ESTC_ID",
"Ethnic_background",
"Etymological_components",
"Etymological_explanation",
"EU_Knowledge_Graph_item_ID",
"EU_Transparency_Register_ID",
"Europeana_Entity",
"Events_attended",
"Events_in_the_sequence",
"Events_mentioned",
"Events_witnessed",
"EVZ_ID",
"Example",
"Excipit",
"Exclusion_criterion_incompatible_with_Membership_in",
"Executor",
"Exemplary_FactGrid_item",
"Exlibris_of",
"External_matching",
"External_tutorial",
"Extra_stemmatic_relationship",
"Extract",
"Extramarital_relationship_to_procure_a_child",
"Eye_colour",
"Fabrication_method",
"Face_shape",
"Facebook_username",
"Facial_hair",
"FactGrid_Collection_of_Information",
"FactGrid_Dokumentseite",
"FactGrid_keyword",
"FactGrid_List",
"FactGrid_list_of_Items_designed_for_this_property",
"FactGrid_list_of_members",
"FactGrid_locality_type",
"FactGrid_map_House_numbers",
"FactGrid_merger_candidate",
"FactGrid_project_space",
"FactGrid_properties_in_which_this_item_can_serve_as_an_answer",
"FactGrid_properties_under_which_this_property_can_serve_as_a_qualifier",
"FactGrid_property",
"FactGrid_property_complaint",
"FactGrid_Property_to_use_instead",
"FactGrid_table_of_contents",
"FactGrid_user_page",
"FactGrid_visualisation",
"Falk_Regiment_ID",
"Family",
"family_database_Juden_im_Deutschen_Reich_ID",
"Family_name",
"Family_various",
"Father",
"Fathers_status",
"Feldpost_number",
"Fellow_student",
"Female_form_of_label",
"Feudal_obligation",
"Fictionalises_stages",
"Fief_leasehold_property",
"Field_of_engagement_expertise",
"Field_of_knowledge",
"Field_of_offices_in_the_Roman_Catholic_Church",
"Field_of_research",
"Final_destination",
"Financed_by",
"Find_a_Grave_memorial_ID",
"Finding_spot",
"Fineness_1000",
"First_documented_date",
"First_documented_in",
"Fiscal_revenue",
"Flag",
"Fly_leaf_Fly_leaves",
"Folios",
"Follower_of",
"Font_size",
"Footnote",
"Form_of_address",
"Form_of_government",
"Form_of_punishment",
"Format",
"format_as_a_regular_expression",
"Formatter_URL",
"Formed_a_set_with",
"Forum_München_ID",
"Founding_members",
"Francke_Foundations_Archives_Orphanage_Registry",
"Francke_Foundations_Bio_ID",
"Franckes_Schulen_Database_ID",
"Frankfurter_Personenlexikon",
"Frauen_in_Bewegung_1848_1938_ID",
"FRBR_entity_class",
"Friends_with",
"From_place_as_mentioned",
"Fruitbearing_Society_Member_ID",
"Fundamental_sentiment",
"Funeral_speech_by",
"fuzzy_sl_ID",
"Gallica_ID",
"GEDBAS_genealogy_person_ID",
"Gender",
"Genealogycom_ID",
"Genicom_profile_ID",
"Geographic_compatriot_of",
"Geographical_outreach",
"Geographical_treated",
"Geomorphology",
"Geonames_Feature_Code",
"GeoNames_ID",
"Geoshape",
"GEPRIS_Historical_ID_Person",
"German_Lobbyregister_ID",
"German_municipality_key",
"Germania_Sacra_database_of_persons_ID",
"Getty_Thesaurus_of_Geographic_Names_ID",
"GitHub_username",
"Given_names",
"GKW_ID",
"Glottolog_ID",
"GND_ID",
"GND_input_field",
"GND_network_graph",
"Godfather_of_the_confirmand",
"Gold_content_g",
"Google_Books_ID",
"Google_Knowledge_Graph_ID",
"Google_Scholar_author_ID",
"GOV_Group_of_Types",
"GOV_ID",
"GOV_object_type",
"Grade_Level",
"Grammatical_Particle",
"Grant",
"Grave",
"Grave_Row",
"Gregorian_calendar_start_date",
"Group_listings",
"GS_vocabulary_term",
"Guardian",
"Hair",
"HAIT_ID",
"Handedness",
"Handwritten_by",
"Harmonia_Universalis_ID",
"Has_subclasses",
"Has_works_in_the_collection",
"HDS_ID",
"Head_of",
"Height",
"Heiress",
"Hex_color",
"HISCO_ID",
"Historic_county",
"Historical_context",
"Historical_continuum",
"Historical_description",
"Historical_Leiden_ID",
"Historical_political_regime",
"History",
"History_of_History_Tree_ID",
"Holding_this_position",
"Holocaust_Geographies_ID",
"Holocaustcz_person_ID",
"Homosaurus_ID_version_3",
"Honorific_prefix",
"Host",
"Hosted",
"House_number",
"House_numbering_system",
"HOV_ID",
"How_sure_is_this",
"Husbandss_status",
"Hydromorphology",
"I_campi_fascisti_ID",
"ICD_10",
"Iconclass_ID",
"Iconclass_identification_of_individual_motifs",
"Iconography",
"ID_19th_century_French_printers_lithographers",
"ID_of_the_German_Federal_Office_of_Geodesy",
"ID_of_the_Klassik_Stiftung_Weimar",
"Identification_by",
"Identification_Document",
"Identification_number",
"Identified_work",
"Ideological_political_positioning",
"IdRef_ID",
"ie",
"Illuminati_code_name",
"Illuminati_code_name_of",
"Image_content",
"Image_number",
"Image_source",
"Immediate_superiors",
"Implemented_by",
"IMSLP_ID",
"In_his_her_personal_service",
"In_leading_position",
"In_the_the_reign_dynasty_time_frame",
"In_words",
"Incipit",
"Includes",
"Income",
"Incunables_de_la_Biblioteca_Nacional_ID_1945",
"Index_Theologicus_ID",
"Indication_the_object_existed",
"INE_ID_Portugal",
"INE_ID_Spain",
"Influenced_by",
"Information_about_transport_connections",
"Information_by",
"Infrastructure",
"Initiated_by",
"Inpatient_treatment_in",
"Input_form",
"Inscription",
"INSEE_municipality_code",
"Installed_by",
"Instance_of",
"Institution_addressed",
"Institutions_mentioned",
"Instrument",
"Inter_national_responsibility",
"Inter_textual_allusions",
"Interest_claim_per_annum",
"Interlinear_commentary",
"Internet_Archive_ID",
"Internetportal_Westfälische_Geschichte_ID_Persons_entry",
"Interval",
"Intervened_on_behalf_of",
"Intimate_relationships",
"Inventoried_by",
"Inventory",
"Inventory_number",
"Inverse_label_item",
"Inverse_property",
"ISBN_10",
"ISBN_13",
"ISNI_ID",
"ISO_3166_1_alpha_2_code",
"ISO_3166_1_alpha_3_code",
"ISO_3166_1_numeric_code",
"ISO_3166_2",
"ISO_3166_3",
"ISO_639_1",
"ISO_639_2",
"ISO_639_3",
"ISO_639_5",
"ISSN",
"Issue",
"Issuer",
"ISTC_ID",
"Item_count_to",
"Jacob_Grimm_Deutsches_Wörterbuch",
"Jewish_Museum_Berlin_Person_ID",
"Joint_partners",
"Journey",
"JudaicaLink_person_ID_GND",
"Judge",
"Julian_calendar_last_date",
"Julian_calendar_stabiliser",
"K10plus_PPN_ID",
"Kalliope_ID",
"KATOTTH_ID",
"Key_data",
"KGI4NFDI_ID",
"Kiel_Scholars_Directory_ID",
"Killed_by",
"Klosterdatenbank_ID",
"KOATUU_ID",
"Lagis_Hessische_Biographie_ID",
"Lanes_Masonic_Records_ID",
"Language",
"Language_skills",
"Last_documented_date",
"Last_holding_archive_of_the_lost_object",
"Last_modified",
"Last_professional_status",
"Latin_Place_Names_ID",
"Latin_version",
"Leaseholder",
"Leaser",
"Legal_form",
"Legal_mandates",
"Legal_response",
"Legislative_term",
"Length_distance",
"Level_of_qualification",
"Library_of_Congress_authority_ID",
"License",
"Licensed_by",
"Liegelord",
"Liegeman",
"Likelihood_percent",
"Line",
"LinkedIn_personal_profile_ID",
"Linking_back_to",
"Listed_in",
"Literal_statement",
"Literal_translation",
"Live_stock",
"Living_conditions",
"Living_people_protection_class",
"Lizenznummer_of_books_printed_in_the_GDR",
"Lobid_GND",
"Local_units_of_measurement",
"Localisation",
"Location_in_the_property",
"Lodge_Matriculation_number",
"Logo_image",
"Made_by",
"Main_lodge",
"Main_regulatory_text",
"Maintained_by",
"Mainzer_Ingrossaturbücher_ID",
"Maitron_ID",
"Male_form_of_label",
"Maps_and_plans",
"MARC_field",
"Marriage_witness",
"Married_to",
"Masonic_degree",
"Mass",
"Mastodon_address",
"Matching",
"Material_composition",
"Mathematics_Genealogy_Project_ID",
"Matriculation_number_string",
"Matrikelportal_Rostock_since_1419_ID",
"Maximum",
"Maximum_value",
"MDZ_digitisation_ID",
"means_of_authenticating",
"Measures_taken",
"Media_type",
"Medical_cause_of_death",
"Medical_condition",
"Medical_treatment",
"Medically_tended_by",
"Meeting_point_of",
"MemArc_ID",
"Member_of",
"Members",
"Memorial_Book_Victims_of_the_Persecution_of_Jews_in_Germany_1933_1945_ID",
"Mentioned_in",
"Merchandise",
"Merger_with",
"Methodology",
"Metric_equivalent",
"Minimum",
"MIRA_ID",
"Misleading_attributions",
"MMLO_ID",
"Mode_of_presentation",
"Mother",
"Mother_lodge_Grand_lodge",
"Motto",
"Mouth",
"Mouth_of_the_watercourse",
"Museum_Association_of_Saxony_Anhalt_ID",
"Museum_Digital_Institutions_ID_Saxony_Anhalt",
"Museum_Digital_Object_ID_Saxony_Anhalt",
"museum_digitalhessen_people_ID",
"Musical_notation",
"Mythical_miraculous_supernatural_properties",
"Name_with_the_Asiatic_Brethren",
"Named_after",
"Naming",
"Naming_of_the_titles_central_protagonist",
"Naming_the_plural",
"Naming_the_singular",
"Natural_Law_Database_ID",
"NDBA_ID",
"Negative_search_result",
"Net_profit",
"Next_higher_archival_level",
"Next_higher_organisational_level",
"Next_higher_rank_or_degree",
"Next_version",
"Niedersächsische_Personen_ID",
"NIOD_WW2_camp_ID",
"NNDB_People_ID",
"NordhausenWiki",
"Normalization_variant",
"Nose",
"Not_noted_in",
"Not_to_be_confused_with",
"Note",
"Noted_in_these_historical_collections",
"Notes",
"NS_Medical_Victims_Institutions_ID",
"NSDAP_membership_number_1925_1945_list",
"Number",
"Number_making_a_unit",
"Number_of_abstentions",
"Number_of_blank_votes",
"Number_of_casualties",
"Number_of_children",
"Number_of_copies_extant",
"Number_of_copies_printed",
"Number_of_employees",
"Number_of_female_children",
"Number_of_hierarchy_levels",
"Number_of_inhabitants_inmates",
"Number_of_integrated_items",
"Number_of_male_children",
"Number_of_objects_within_a_collection",
"Number_of_pages_leaves_sheets_columns_lines",
"Number_of_participants_members",
"Number_of_pieces",
"Number_of_registered_students",
"Number_of_sets_ordered",
"Number_of_social_media_followers",
"Number_of_spoilt_votes",
"Number_over_the_entire_period",
"NUTS_code",
"OARE_ID",
"OATP_ID",
"Object_has_role",
"Object_in_question",
"Object_mentioned",
"Object_of_payment",
"Object_of_procedure",
"Object_paid",
"Object_properties_noted",
"Object_type_properties",
"Object_types",
"Objected_by",
"Objects_of_interest",
"Objects_of_knowledge",
"Objects_side",
"OCLC_ID",
"OCLC_work_ID",
"Of_importance_to",
"Official_version",
"Official_website",
"OhdAB_category",
"OhdAB_ID",
"OhdAB_Level_of_expertise",
"OhdAB_standard_designation",
"Old_inventory_number",
"Old_Israelite_Cemetery_Leipzig_Graves_ID",
"OME_ID",
"On_the_side_of",
"Online_catalogue",
"Online_digitisation",
"Online_image",
"Online_information",
"Online_presentation",
"Online_primary_documents",
"Online_transcript",
"Online_translation",
"Ontology_data_model",
"OpenHistoricalMap_ID",
"OpenStreetMap_node_ID",
"OpenStreetMap_object",
"OpenStreetMap_relation_ID",
"OpenStreetMap_way_ID",
"Operator",
"Opponent_of_the_disputation",
"Opposite_of",
"Opposite_property",
"Options",
"ORACC_ID",
"ORACC_id_word",
"ORCID_ID",
"Ordained_consecrated_by",
"Organisation_open_from_here",
"Organisation_signing_responsible",
"Organisation_signing_responsible",
"Organisational_aspects",
"Organisational_context",
"Organisational_features",
"Organisational_structure",
"Organisational_ties",
"Organizational_functionality",
"Origin_attribute",
"Origin_of_the_watercourse",
"Original_language",
"Original_note",
"Original_of_this",
"Original_publication",
"Original_research_of",
"Originality_of_the_item",
"Osteological_Sex",
"Owned_by",
"Owner_of",
"P1356",
"P1389",
"Page_layout",
"Pages",
"Parallel_tradition",
"Parent_organisation",
"Parent_taxon",
"Parish_affiliation",
"Part_of",
"Part_of_the_collection",
"Pastors_database_ID",
"Patients",
"Patronym_or_matronym_for_this_person",
"Payment_interval",
"Payment_recipient",
"Payment_sender",
"Payment_transactor",
"Peerage_person_ID",
"People_who_were_involved_in_presence",
"Per",
"Percentage",
"Period_Style",
"Periodicity",
"Person_for_whom_the_document_was_written",
"Person_signing_responsible",
"Personal_connections",
"Personal_inspection_by",
"Personal_servant_of",
"Persons_mentioned",
"Persons_of_Indian_Studies_ID",
"PhiloBiblon_ID",
"PhiloBiblon_Property_Emulator",
"PhiloBiblon_vocabulary_term",
"Photo_Cardboard_Manufacturer",
"Photographic_Studio",
"Physical_description",
"Physical_feature",
"Pilgrimage_to",
"Place_of_action",
"Place_of_address",
"Place_of_baptism",
"Place_of_birth",
"Place_of_death",
"Place_of_detention",
"Place_of_education",
"Place_of_issue",
"Place_of_marriage",
"Place_of_publication",
"Place_of_publication_as_misleadingly_stated",
"Place_of_publication_without_fictitious_information",
"Plates",
"Pleiades_ID",
"Plot_ingredient",
"Plus",
"PMB_person_ID",
"Poetic_form",
"Position_held",
"Position_in_sequence",
"Position_towards_object",
"Possible_further_item_connections",
"Possible_identification_link_to_external_information",
"Possibly_identical_to",
"Post_included",
"Postal_address",
"Postal_code",
"Preceding_Lexemes_in_stemma",
"Precision_of_begin_date",
"Precision_of_begin_date_string",
"Precision_of_date",
"Precision_of_end_date",
"Precision_of_end_date_string",
"Precision_of_localisation",
"Predominant_gender_usage",
"Preface_by",
"Preferred_designation",
"PRELIB_archival_document_ID",
"PRELIB_edition_ID",
"PRELIB_organization_ID",
"PRELIB_periodical_ID",
"PRELIB_person_ID",
"PRELIB_place_ID",
"PRELIB_work_ID",
"Premiere",
"Present_holding",
"Presentation",
"Presented_at",
"Presented_by",
"Preservation",
"Presiding_the_disputation",
"Previous_version",
"Primary_source",
"Printed_by",
"Prisoner_of_war_of",
"Privilege_granted_by",
"Proceedings_of_the_event",
"Process_File_number",
"Produced_by_brand",
"Produces_product_range",
"Professional_address",
"Programming_language",
"Project",
"Pronunciation_IPA",
"Property_constraint",
"Proposed_introduced_by",
"Proposed_to_become_a_member_of",
"Proprietor_in",
"Protagonists",
"Pseudonym",
"Pseudonym_literal",
"Pseudonym_of",
"Public_awards_and_titles",
"Publications_stemming_from_this_research",
"Published_in",
"Published_in",
"Published_in_this_publication",
"Publisher",
"Publisher",
"Publisher_as_misleadingly_stated",
"Purpose",
"Qualifier",
"Qualifying_sub_properties",
"Quantity",
"Quote",
"Quoting",
"RAG_ID",
"Raised_by",
"RAM_size",
"Rank",
"Rank_service_number",
"re3data_D",
"Real_estate",
"Realization_Construction",
"Reason_for_deprecated_rank",
"Reason_for_persecution",
"Reason_for_preferred_rank",
"Receives_area_from",
"Reception_promises_literal",
"Recipient",
"Recognised_by",
"Recording_online_information",
"Reference_code",
"Referencing_method",
"Regional_localisation",
"Registered_accepted_by",
"Registrar",
"Registry_number",
"Registry_office_of",
"Regular_meeting_point",
"Related_object",
"Relation_constraint",
"Relationship_through",
"Religious_background",
"Religious_or_spiritual_practice_and_experiences",
"Religious_order",
"Religious_status",
"Relocated_subject",
"Renewal_date",
"Rent_per_annum",
"Repertorium_Germanicum_ID",
"Repertorium_Poenitentiariae_Germanicum_ID",
"Reported_event",
"Represented_by",
"Representing",
"Request_FactGrid",
"Request_name",
"Research_projects_that_contributed_to_this_data_set",
"Research_stay_in",
"ResearchGate_profile_ID",
"Resident",
"Respondent_of_the_disputation",
"Result",
"Result_of_investigation",
"Reviewed_in",
"Reviewing",
"Revised_by",
"Rhyme_scheme",
"RI_ID",
"RISM_ID",
"Rite_rule_system",
"Role",
"Romanised_transcription",
"Room_number",
"Rosicrucian_code_name",
"Rosicrucian_code_name_of",
"Said_to_be_the_same_as",
"Sandrartnet_person_ID",
"Scale_1n",
"Schoenberg_Database_of_Manuscripts_name_ID",
"School_adherence",
"Script_style",
"Seal",
"Seal_ID",
"Second_family_name_in_Spanish_name",
"Secondary_literature_research",
"Secondary_literature_research_literal",
"Section",
"See_also",
"See_also_property",
"Segmentation",
"Sejm_Wielkipl_profile_ID",
"Self_classification_Lexeme",
"Self_statement_on_historicity_fictionality",
"Semantic_Kompakkt_ID",
"Series",
"Series_integration",
"Services_offered",
"Set_by",
"Sexual_orientation",
"Shareholder",
"Shares_border_with",
"short_digest",
"Short_reference",
"Siblings",
"Signature",
"Signed_by",
"Silver_content",
"SIMC_ID",
"Skin_colour",
"Social_status",
"Software",
"Sort_by",
"Sort_string",
"Source_based_classification",
"Source_literal",
"Spanish_Biographical_Dictionary_ID",
"SPARQL_endpoint_URL",
"Specific_data_set",
"Specific_statement",
"Specification",
"Speech_act_qualities",
"Sphere_in_life",
"Split_off",
"Split_off_from",
"Sponsor_supporter",
"SS_KL_Auschwitz_Garrison_ID",
"SS_membership_number",
"SS_Resettlement_ID",
"SSNE_person_ID",
"Standardised_evaluation",
"Start_time_of_reported_events",
"State_bibliographical",
"State_of_conservation_literal",
"State_of_work",
"Statement_denied_by",
"Statement_refers_to",
"Statement_refers_to",
"Statements_to_be_verified_in_this_data_set",
"Stature",
"Status",
"Status_of_possesion",
"Stay_in",
"Stored_in",
"Street_square",
"Strict_Observance_order_name",
"Strict_Observance_order_name_of",
"Structural_hierarchies_implemented",
"Student",
"Student_of",
"Styrian_State_Library_ID",
"Subclass_of",
"Subject_evicted",
"Subject_has_role",
"Subject_heading",
"Subject_matter",
"Subject_matter_that_raised_objections",
"Subject_of_negotiation",
"Subject_paid",
"Subject_studied_at_university",
"Subject_topic_heading",
"Subjected",
"Subjected_to",
"Subproperties",
"Subproperty_of",
"Subscribers",
"Subscription_text",
"Subscriptions_signed",
"Subsidiary",
"Subunit_of",
"Subunits",
"Supplied_by",
"Supplied_forced_laborers_for",
"Surviving_copies",
"Sustainability",
"Swedish_portrait_archive_ID",
"Swedish_small_places_ID",
"Swedish_urban_area_code",
"Swiss_municipality_code",
"Symbolises",
"Synonym",
"System_component_of",
"Sächsische_Biografie_ID",
"Süddeutsche_Patrizier_Datenbank_ID",
"Target_group_person",
"Target_language",
"Tax_per_annum",
"Taxable_assets",
"Taxon_range",
"Taxonomic_name",
"Taxonomic_rank",
"Team",
"Technology",
"Teeth",
"TEI_ID",
"Telephone_number",
"Term_attributed_by",
"Term_for_practitioner",
"Term_for_the_academic_expert",
"Term_for_the_field_of_study",
"Term_for_the_group_practicing",
"Term_for_the_ideology",
"Term_for_the_institution",
"Term_for_the_object_of_knowledge",
"Territorial_localisation",
"Territory_granting_the_indigenate",
"Test_property_url",
"Text_justification_legal_basis_constitution",
"Text_source",
"Texts_depicting_staging_the_subject",
"Texts_mentioned",
"Thesis",
"Things_and_places_mentioned",
"Time_of_day",
"Timestamp",
"Title",
"Title_aspects",
"Title_page_transcript",
"to",
"Topic",
"Total_assets",
"Total_revenue",
"Total_valid_votes",
"Transacted_object",
"Transcribed_by",
"Translation",
"Translation_literal",
"Translation_of",
"Translator",
"Translator_as_misleadingly_stated",
"Transliteration",
"Transmitted_by",
"Transparency",
"Transparency_of_the_information_provided",
"Transport_connection",
"Transport_connection_from",
"Transport_connection_to",
"Tribe",
"Troop_contributors",
"Troop_strength",
"Truth_context",
"Twitter_X_handle",
"Type_of_event",
"Type_of_legal_act",
"Type_of_publication",
"Type_of_term",
"Type_of_treatment",
"Type_of_work",
"Typeface",
"Typology",
"Under_the_rule_of",
"Underlying_problem",
"Union_List_of_Artist_Names_ID",
"University_Collections_in_Germany_ID",
"URL",
"URL_links_to",
"URN_formatter",
"Use_functionality",
"Used_forced_labor_from",
"Users",
"USTC_editions_ID",
"Value_price",
"Variant",
"Vasserot_ID_streets_of_Paris",
"VD16_ID",
"VD17_ID",
"VD18_ID",
"Verdict",
"Vergue_ID",
"Verkaufspreis",
"Versioning",
"Versions_of_this_work",
"VIAF_ID",
"Victims_of_NS_Medical_Research_ID",
"Visual_work_component",
"Visual_work_components_by",
"Voice_type",
"Volksbund_Gräbersuche_Online_ID",
"Volume",
"Volume_as_a_quantity",
"War_deployment",
"Watermark",
"Weapons_category",
"Webhosting",
"Weekday",
"Well_Known_Text_Geometry",
"What_supports_this_identification",
"Where_started_or_produced",
"WIAG_ID",
"WIAG_Office_in_Sequence_ID",
"Wider_field_of_genres",
"Width",
"Wikibase_Browser",
"Wikibase_World_Item_ID",
"Wikidata_Item",
"Wikidata_lexeme",
"Wikidata_property",
"Wikimedia_Commons_archival_document_reproductions",
"Wikimedia_commons_exemplary_work",
"Wikimedia_Commons_image_of_grave_or_memorial",
"Wikimedia_Commons_Item_image",
"Wikimedia_language_code",
"Wikimedia_map_location",
"With_manuscript_notes_by",
"Without",
"Work_literal",
"Work_location",
"Work_task_description",
"Work_to_be_subscribed",
"Works_published_or_unpublished",
"WorldCat_Identities_ID",
"WorldCat_Registry_ID",
"WorldCat_Title_ID",
"Worshipful_Master",
"Writing_surface",
"Württembergische_Kirchengeschichte_person_ID",
"X_numeric_user_ID",
"X_post_ID",
"Yad_Vashem_Ghetto_ID",
"Yad_Vashem_name_genealogy_ID",
"Year_of_the_time_frame",
"YouTube_video_ID",
"Yu_Gi_Oh_Wiki_ID",
"Zeitschriften_database_ID",
"Zenodo_ID",
"ZOBODAT_People_ID",
"ZOBODAT_Publication_Article_ID",
"ZOBODAT_Publication_Series_ID",
"ZWAR_ID",
"ZWAR_Interview_ID",
"ÖSTAT_number"
)

# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...model import (
    ExternalId,
    IRI,
    Item,
    Property,
    Quantity,
    String,
    Text,
    Time,
)
from .prelude import P

# autopep8: off
# flake8: noqa

_1st_carry = P(546, range=Quantity, label='1st carry', description='for the first fraction esp. in an early modern price statement')
_2nd_carry = P(547, range=Quantity, label='2nd carry', description='for the third component of an early modern price tag')
_3D_model_external = P(1034, range=IRI, label='3D model (external)')
Abbot = P(474, range=Item, label='Abbot', description='Leader of a monastery')
Accessibility = P(125, range=Item, label='Accessibility', description='to state access restrictions of archival resources')
According_to = P(129, range=Item, label='According to', description='state who made a certain claim without identifying with it')
Accounts_held_in = P(686, range=Item, label='Accounts held in', description='to state how monetary values were stated in a given context, refer to basic unit and add P684 and P685 for the subsequent fractions')
Accusation_of = P(507, range=Item, label='Accusation of', description='to state a accusation, use P1102 to state the result of the trial')
Actually_addressed_to = P(27, range=Item, label='Actually addressed to', description='property to use if a sender did not have clearer knowledge about the actual receiver. State with "was addressed" and clarify with P28 the actual receiver(s)')
ADB_Wikisource = P(741, range=ExternalId, label='ADB (Wikisource)', description='Link to the respective Wikisource ADB-article')
Additional_name_attributes = P(784, range=Text, label='Additional name attributes')
Address_item = P(208, range=Item, label='Address [item]', description='street address where subject or organization is located, preferably full. Include building number, city/locality, post code, but not country')
Addressees_of_deliveries = P(1211, range=Item, label='Addressees of deliveries', description='not necessarily the customers who make a payment')
Admission_requirement_required_membership = P(863, range=Item, label='Admission requirement / required membership', description='to name obligatory criteria which a member has to fulfil')
Adversary = P(664, range=Item, label='Adversary', description='to name ideological, political or religious views opposed by the person or organisation')
Age_from = P(866, range=Quantity, label='Age from', description='after reaching a certain age')
Age_up_to = P(867, range=Quantity, label='Age up to', description='before reaching a certain age')
Akademie_der_Künste_Berlin_Member_ID = P(1151, range=ExternalId, label='Akademie der Künste Berlin Member ID')
Alleged_member_of = P(455, range=Item, label='Alleged member of', description='to note allegations of membership')
Alternatively = P(516, range=Item, label='Alternatively', description='FactGrid Qualifier to offer an alternative Statement')
Amount_in_dispute = P(1107, range=Quantity, label='Amount in dispute')
Amount_of_the_penalty_payment = P(1109, range=Quantity, label='Amount of the penalty payment')
Annex = P(104, range=String, label='Annex', description='qualifier to refer to a specific annex in a work stated in the main statement.')
Answered_with = P(205, range=Item, label='Answered with', description='the reply that answers the present item')
Apartment = P(886, range=Item, label='Apartment', description='property to identify an apartment number in a house')
Approved_by = P(729, range=Item, label='Approved by', description='person or authority that is granting permission to proceed with a proposal or to print a text')
Archived_at_the_URL = P(1361, range=IRI, label='Archived at the URL', description='URL to the archived web page')
Archives_at = P(185, range=Item, label='Archives at', description='to state where documents of a person or organisation are now to be found')
Area = P(1020, range=Quantity, label='Area')
Area_changes_to = P(1338, range=Item, label='Area changes to', description='to record losses of land, for example after wars or reorganization of territories')
Area_ID = P(1033, range=String, label='Area ID')
Aristocratic_tenures = P(215, range=Item, label='Aristocratic tenures', description='tenure of a territory / object held by a person because of their noble ancestry')
Aristocratic_title = P(26, range=Item, label='Aristocratic title', description='titles held by the person, mostly because of noble ancestry')
Arolsen_Archives_Persons_ID = P(1207, range=ExternalId, label='Arolsen Archives Persons ID')
Arrival = P(996, range=Item, label='Arrival')
Art_and_Architecture_Thesaurus_ID = P(710, range=ExternalId, label='Art & Architecture Thesaurus ID', description='identifier in the Art & Architecture Thesaurus by the Getty Research Institute')
Article = P(98, range=Item, label='Article', description='qualifier to reference a specific article, e.g. in an encyclopedia, book, or journal named in the preceding statement.')
Associated_person = P(1136, range=String, label='* Associated person', description='string version of P703: general property to link people in various personal or professional relationships that are not covered by the more common properties, as recorded')
Authenticated_by = P(734, range=Item, label='Authenticated by', description='to state a person or authority that legally certified a document')
Author = P(21, range=Item, label='Author', description='who wrote the object in question?')
Author_as_strangely_stated = P(20, range=Item, label='Author as strangely stated', description='the author as stated in a text or on a book cover. Use P21 as the default')
BAG_code_for_Dutch_places_of_residence = P(1352, range=ExternalId, label='BAG code for Dutch places of residence', description='BAG (Basic Registration of Addresses and Buildings) code for places in the Netherlands')
Ballots_cast = P(1310, range=Quantity, label='Ballots cast', description='total number of ballot(s) cast, including invalid or blank ballots')
Banns_of_marriage_date = P(1079, range=Time, label='Banns of marriage, date')
Based_on = P(702, range=Item, label='Based on', description='work(s) or document(s) used as the basis for subject item')
Bayrisches_Musiker_Lexikon_Online_ID = P(1333, range=ExternalId, label='Bayrisches Musiker-Lexikon Online-ID', description='Digital lexicon for people, works and places of Bavarian music history')
Bearer = P(732, range=Item, label='Bearer', description='the person who transmitted a document')
Bearer_of_the_Coat_of_Arms = P(1316, range=Item, label='Bearer of the Coat of Arms')
Begin_date = P(49, range=Time, label='Begin date', description='start in time (including the date: [→), e.g. of a longer event; also as a qualifier e.g. for the beginning of a marriage. Counterpart: P50 End date.')
Begin_text_span = P(1208, range=String, label='Begin text span', description='place in a manuscript or printed volume where a text or text segment (e.g., prologue) begins')
Beginning_of_composition = P(39, range=Time, label='Beginning of composition', description='use this property if a document has been written over a longer period of time')
Best_practice_notice = P(598, range=Text, label='Best practice notice', description='to note how a certain item or property is designed to work on the database')
Bestellnummer_of_books_printed_in_the_GDR = P(1092, range=String, label='Bestellnummer (of books printed in the GDR)')
Binding = P(800, range=String, label='* Binding')
Biographical_notes = P(173, range=String, label='Biographical notes', description='text field for biographical notes')
Blood_type = P(641, range=Item, label='Blood type', description='a classification of blood, based on the presence and absence of antibodies and inherited antigenic substances on the surface of red blood cells (RBCs)')
BNE_ID = P(652, range=ExternalId, label='BNE-ID', description='identifier from the authority file of the Biblioteca Nacional de España. Format for persons: "XX" followed by 4 to 7 digits')
BnF_ID = P(367, range=ExternalId, label='BnF ID')
Bossu_ID = P(610, range=ExternalId, label='Bossu ID', description='identifier in the Fichier Bossu (French freemasons database, ~1750-1850)')
Buchenwald_satellite_camp_ID = P(1325, range=ExternalId, label='Buchenwald satellite camp ID', description='ID of the internet project aussenlager-buchenwald.de')
Canonization_status = P(1147, range=Item, label='Canonization status')
Capacity = P(717, range=Quantity, label='Capacity', description='the maximum amount that something can contain')
Capital = P(465, range=Item, label='Capital', description='to state the capital city of a country or region')
Capital_burden = P(1014, range=Quantity, label='Capital burden')
Capital_of = P(466, range=Item, label='Capital of', description='to name the country or region ruled from the city')
Capital_return_of_the_property = P(1019, range=Quantity, label='Capital return of the property')
Career_statement = P(165, range=Item, label='Career statement')
Catalogus_Professorum_Halensis_ID = P(1055, range=ExternalId, label='Catalogus Professorum Halensis ID')
Catholic_Hierarchy_ID = P(462, range=ExternalId, label='Catholic Hierarchy ID', description='Identifier from the online database of bishops and dioceses of the Roman Catholic Church')
Catholic_religious_name_of = P(373, range=Item, label='Catholic religious name of')
Cause_of_end = P(506, range=Item, label='Cause of end', description='qualifier to define the end of a time span with more precision')
Cause_of_loss = P(347, range=Item, label='Cause of loss', description='state how an object got lost')
CDLI_ID = P(692, range=ExternalId, label='CDLI ID', description='Identifier of an artifact in the Cuneiform Digital Library Initiative')
CDLI_ID2 = P(694, range=ExternalId, label='CDLI ID2', description='cdli database URI for external resources')
CERL_Thesaurus_ID = P(537, range=ExternalId, label='CERL Thesaurus ID', description='book history database')
Choice_of_title_in_Prozent = P(1311, range=Quantity, label='Choice of title (in Prozent)', description='Calculating what percentage of eligible voters participated in an election')
Chronology = P(1350, range=Time, label='Chronology')
CIDOC_CRM_class = P(1317, range=Item, label='CIDOC CRM class', description='Property for mapping the CDO CRM ontology structure in FactGrid')
CIDOC_CRM_property = P(1318, range=ExternalId, label='CIDOC CRM property', description='states the equivalent CIDOC CRM property')
Circumcision_Date_religious = P(1060, range=Time, label='Circumcision Date (religious)')
Circumstances_of_death = P(885, range=Item, label='Circumstances of death', description='P162 indicates the effective (medical) cause of death, the present property notes circumstances such as execution, suicide or accident')
Citizen_of = P(617, range=Item, label='Citizen of')
City_Wiki_Dresden_ID = P(1327, range=ExternalId, label='City Wiki Dresden ID', description='Reference in the wiki-based city encyclopedia for the state capital Dresden, as well as Saxony, provided there under license: CC BY-NC-SA 2.0 DE')
Claimbase_ID = P(1341, range=ExternalId, label='Claimbase ID', description='ID of the FactGrid Claimbase')
classification_of_the_data_provider = P(1300, range=Item, label='classification of the data provider', description='To keep the P2 equivalent of a data source for mass entries, use P129 to name the source and P34 to fix the literal if necessary')
Collation = P(704, range=String, label='Collation', description='the arrangement of sheets in a codex or book')
Collected_by = P(159, range=Item, label='Collected by')
Collegiate_church = P(469, range=Item, label='Collegiate church')
Colour = P(697, range=Item, label='Colour', description='to state a colour in words like red, dark blue etc.')
Columns = P(755, range=String, label='Column(s)', description='to refer to a particular column or columns of a quoted document')
Commentator = P(730, range=Item, label='Commentator', description='person who writes a commentary on a text')
Competent_Jurisdiction = P(1009, range=Item, label='Competent Jurisdiction')
Complete_Bible_Genealogy_ID = P(502, range=ExternalId, label='Complete Bible Genealogy-ID', description='link to personal data sets of http://www.complete-bible-genealogy.com/')
Complex_Evaluation = P(1143, range=String, label='Complex Evaluation', description='to quote a longer complex evaluation')
Composer = P(539, range=Item, label='Composer', description='author of a piece of music')
Composite_ID = P(1083, range=String, label='Composite ID')
Compulsory_obligation_towards = P(1015, range=Item, label='Compulsory obligation towards')
Conference_participations = P(349, range=Item, label='Conference participations', description='to state conferences the person participated in')
Confirmed_by = P(731, range=Item, label='Confirmed by', description='a person who gives his/her personal back up to a statement')
Conflict_parties = P(715, range=Item, label='Conflict parties', description='to state the factions that were involved in a conflict')
Constituted_by = P(362, range=Item, label='Constituted by', description='to state the lodges that constituted a lodge')
constraint_scope = P(1046, range=Item, label='constraint scope')
Contains_documents_of = P(1054, range=String, label='* Contains documents of')
Contemporary_witness_document = P(32, range=Item, label='Contemporary witness document', description='to identify individuals in the public')
Continuation_of = P(6, range=Item, label='Continuation of', description='State e.g. the last number of a journal you are registering.')
Continued_by = P(7, range=Item, label='Continued by', description='to state for instance the next volume of a book, an event, an organisation, addresses, etc.')
Contributor = P(511, range=Item, label='Contributor', description='use for a subordinate role in the production of the resource, qualify the specific contribution (e.g. preface to a book) with P553')
Contributor_to = P(649, range=Item, label='Contributor to', description='to name works, such as a magazine, in the creation of which the person was involved')
Copy_of = P(16, range=Item, label='Copy of', description='to name the source of the text/object in question.')
Copyright_holder = P(1303, range=Item, label='Copyright holder')
Correlation = P(736, range=Item, label='Correlation', description='state that sort of statistics and qualify with the quantity property P307')
Cosignatory_in = P(167, range=Item, label='Cosignatory in')
Country_of_citizenship = P(616, range=Item, label='Country of citizenship')
Cousin = P(505, range=Item, label='Cousin', description='the son of an aunt or uncle')
Creator = P(1134, range=String, label='* Creator', description='string version of P845: General category statement above the more specific statements like author, as recorded')
Credit_receiver_of = P(609, range=Item, label='Credit receiver of', description='Organisation or person commissioning a person or organisation to provide a service')
CTHS_ID_person = P(656, range=ExternalId, label='CTHS ID person', description='identifier in "Annuaire prosopographique : la France savante" by CTHS')
CTHS_ID_society = P(678, range=ExternalId, label='CTHS ID society', description='identifier in "Annuaire des sociétés savantes" by CTHS')
Curriculum_Vitae = P(1131, range=Time, label='Curriculum Vitae')
Dansk_Biografisk_Leksikon_ID = P(1298, range=ExternalId, label='Dansk-Biografisk-Leksikon ID')
Data_BnF_ID = P(500, range=ExternalId, label='Data BnF ID', description='identifier in Data BnF')
Data_set_wanting_a_statement_on = P(496, range=Property, label='Data set wanting a statement on', description='link Properties you want to have connected with a statement')
Data_size = P(1321, range=Quantity, label='Data size', description='size of a software, dataset, neural network, or individual file')
Dataset = P(648, range=Item, label='Dataset', description='to state the dataset from which the data come')
Dataset_complaint = P(17, range=Item, label='Dataset complaint', description='Use this property to state deficiencies in the data set (which future research should handle)')
Dataset_editing = P(1302, range=Item, label='Dataset editing')
Dataset_status = P(799, range=Item, label='Dataset status', description='Use this property to give status of a dataset or a record in a dataset, database, or catalogue, e.g. date created or updated')
Datatype = P(1217, range=Item, label='Datatype', description='datatype of the FactGrid property')
Date_after = P(41, range=Time, label='Date after', description='the earliest possible date for something')
Date_as_stated = P(96, range=Time, label='Date as stated', description='Qualifier (e.g. if you could previously specify a day where only a year was mentioned. Alternatively, P35 is available for text input.')
Date_before = P(43, range=Time, label='Date before', description='the latest possible date for something')
Date_of_baptism = P(37, range=Time, label='Date of baptism', description='Date on which a person was baptized')
Date_of_birth = P(77, range=Time, label='Date of birth', description='date on which a person was born')
Date_of_burial = P(40, range=Time, label='Date of burial', description='See also P38 date of death')
Date_of_confirmation = P(182, range=Time, label='Date of confirmation', description='Date on which a person was confirmed')
Date_of_creation = P(412, range=Time, label='Date of creation', description='use if a text for instance was composed far earlier than the copy extant')
Date_of_death = P(38, range=Time, label='Date of death', description='date on which a person died')
Date_of_first_publication = P(1152, range=Time, label='Date of first publication')
Date_of_last_will = P(214, range=Time, label='Date of last will', description='Date on which the last will of a person was set up')
Date_of_premiere = P(551, range=Time, label='Date of premiere', description='to state the date when a play was first staged')
Date_of_publication = P(222, range=Time, label='Date of publication', description='The standard date as taken from a title page. Use P96 if you know the exact day, week, or month of the publication')
Date_of_receipt = P(44, range=Time, label='Date of receipt', description='date when a letter arrived')
Date_of_retirement = P(459, range=Time, label='Date of retirement', description='property to be used with qualifiers the time of retirement etc.')
Dedicatee = P(391, range=Item, label='Dedicatee')
Degree_system = P(357, range=Item, label='Degree system', description='to state the degrees offered by an organisation')
Degrees_worked = P(361, range=Item, label='Degrees worked', description='Masonic property: state for instance "St John\'s Masonry" or "St Andrews Masonry"')
Den_Store_Danske_ID = P(1297, range=ExternalId, label='Den-Store-Danske ID')
Departure = P(997, range=Item, label='Departure')
Design_planning = P(552, range=Item, label='Design / planning', description='to name the designer of a building')
Destimation_Arrival_point = P(29, range=Item, label='Destimation / Arrival point', description='the starting place for any event (journey, transport, dispatch of an object, sending of a letter, flight, etc.)')
Deutsche_Biographie_GND_ID = P(622, range=ExternalId, label='Deutsche Biographie (GND) ID')
Deutsche_Fotothek_object_ID = P(1202, range=ExternalId, label='Deutsche Fotothek object-ID')
Deutsche_Inschriften_Online_ID = P(1059, range=ExternalId, label='Deutsche Inschriften Online ID')
Deutsches_Literaturarchiv_Marbach_ID = P(1149, range=ExternalId, label='Deutsches Literaturarchiv Marbach ID')
Deutsches_Rechtswörterbuch = P(882, range=ExternalId, label='Deutsches Rechtswörterbuch', description='link into the database version')
Dewey_Decimal_Classification = P(1306, range=ExternalId, label='Dewey Decimal Classification')
DFG_subject_classification = P(1027, range=Item, label='DFG subject classification')
Diameter = P(690, range=Quantity, label='Diameter', description='(largest) distance between two points of a circle or sphere')
Diccionari_de_la_Literatura_Catalana_ID = P(1330, range=ExternalId, label='Diccionari de la Literatura Catalana ID', description='identifier for an item in the Diccionari de la Literatura Catalana')
Dictionary_of_Swedish_National_Biography_ID = P(377, range=ExternalId, label='Dictionary of Swedish National Biography ID')
Digest = P(724, range=Text, label='Digest', description='to give a brief summary')
Discovered_invented_developed_by = P(618, range=Item, label='Discovered / invented / developed by')
Distance_between_addresses = P(793, range=Quantity, label='Distance between addresses')
DNB_Info_ID = P(668, range=ExternalId, label='DNB-Info ID', description='Special GND ID for information')
Docker_Hub_repository = P(1320, range=ExternalId, label='Docker Hub repository', description='Docker repository hosted on Docker Hub')
Documented_object = P(371, range=Item, label='Documented object')
DOI = P(634, range=ExternalId, label='DOI')
Download_link = P(1161, range=IRI, label='Download link', description='to provide a link to download a file or data set')
Duration = P(398, range=Quantity, label='Duration')
Duration_of_the_prison_sentence = P(1108, range=Quantity, label='Duration of the prison sentence')
Ecclesiastical_province = P(463, range=Property, label='Ecclesiastical province')
Economic_sector_of_the_career_statement = P(626, range=Item, label='Economic sector of the career statement')
Editorial_responsibility = P(176, range=Item, label='Editorial responsibility', description='to state those responsible for the presentation of a text or texts in a book, a collective volume or journal, usually neither authors of object nor the publishing business that organises the distribution')
Educating_institution = P(160, range=Item, label='Educating institution')
Education_level_academic_degree = P(170, range=Item, label='Education level / academic degree')
Edvard_Munchs_correspondance_person_ID = P(699, range=ExternalId, label='Edvard Munch\'s correspondance person ID', description='identity identifier for a person in correspondance with Edvard Munch')
EHAK_ID = P(1213, range=ExternalId, label='EHAK-ID', description='ID of the Estonian statistical office')
EHRI_ghetto_ID = P(1194, range=ExternalId, label='EHRI ghetto ID')
Election_results_by_candidate = P(1304, range=Item, label='Election results by candidate', description='Person or party as an applicant or candidate for a position')
Eligible_voters = P(1308, range=Quantity, label='Eligible voters', description='number of eligible voters for a particular election')
Email_contact_page = P(722, range=IRI, label='Email / contact page', description='to be used on organisations, and by users where they handle their personal Items, prefix with "mailto:"')
Employers_status = P(675, range=Item, label='Employer\'s status', description='to note the status differences among servants or slaves with a perspective on their masters or mistresses')
End_date = P(50, range=Time, label='End date', description='the final point of a period (excluding that date: →])')
End_of_events_reported = P(46, range=Time, label='End of events reported', description='e.g. last date of a diary')
End_text_span = P(1209, range=String, label='End text span', description='place in a manuscript or printed volume where a text or text segment ends')
Enzyklopädie_der_Russlanddeutschen_ID = P(1154, range=ExternalId, label='Enzyklopädie der Russlanddeutschen ID')
epidat_Database_ID = P(1063, range=ExternalId, label='epidat-Database ID')
Equivalent_in_grams_of_copper = P(682, range=Quantity, label='Equivalent in grams of copper', description='to give a value independent of monetary fixings')
Equivalent_in_grams_of_gold = P(681, range=Quantity, label='Equivalent in grams of gold', description='to give a value independent of monetary fixings')
Equivalent_in_grams_of_silver = P(680, range=Quantity, label='Equivalent in grams of silver', description='to give a value independent of monetary fixings')
Equivalent_multilingual_item = P(796, range=Item, label='Equivalent multilingual item')
Espacenet_ID_for_patents = P(384, range=ExternalId, label='Espacenet ID for patents')
Ethnic_background = P(212, range=Item, label='Ethnic background', description='to state particular physical characteristic that betray ethnic origin')
Europeana_Entity = P(385, range=ExternalId, label='Europeana Entity')
Events_attended = P(119, range=Item, label='Events attended', description='to state events or initiatives the person participated in, use alternatively P242 to state events witnessed')
Events_in_the_sequence = P(224, range=Item, label='Events in the sequence', description='name the contributions (e.g. to a meeting, conference or celebration)')
Excipit = P(602, range=String, label='Excipit', description='to quote the last words of a text or part of a text, e.g., prologue')
Exclusion_criterion_incompatible_with_Membership_in = P(864, range=Item, label='Exclusion criterion / incompatible with Membership in')
Executor = P(416, range=Item, label='Executor', description='An executor is someone who is responsible for executing, or following through on, an assigned task or duty. The feminine form, executrix, may sometimes be used.')
Exemplary_FactGrid_item = P(364, range=Item, label='Exemplary FactGrid item', description='to name an item that uses this property as intended')
Exlibris_of = P(413, range=Item, label='Exlibris of', description='state whose Exlibris is found in a book')
Extra_stemmatic_relationship = P(740, range=Item, label='Extra-stemmatic relationship', description='to use as an alternative to P233, use again with P234 as qualifier')
Extract = P(204, range=Item, label='Extract', description='use this property especially on lost documents where you still have an extract')
Extramarital_relationship_to_procure_a_child = P(495, range=Item, label='Extramarital relationship to procure a child', description='one of the partners is surrogate mother, the other receives the child')
Eye_colour = P(637, range=Item, label='Eye colour', description='color of the irises of a person\'s eyes')
Facial_hair = P(644, range=Item, label='Facial hair', description='e.g. for of beard')
FactGrid_keyword = P(1132, range=Item, label='FactGrid keyword')
FactGrid_List = P(720, range=IRI, label='FactGrid List', description='URL for FactGrid queries')
FactGrid_locality_type = P(1335, range=Item, label='FactGrid locality type', description='classification of the FactGrid localities project')
FactGrid_map_House_numbers = P(679, range=IRI, label='FactGrid map: House numbers', description='addresses on the street')
FactGrid_properties_in_which_this_item_can_serve_as_an_answer = P(184, range=Property, label='FactGrid properties in which this item can serve as an answer', description='FactGrid properties this item has been designed to suit')
FactGrid_property = P(548, range=Property, label='FactGrid property', description='the FactGrid property that captures objects of the item type')
FactGrid_property_complaint = P(381, range=Item, label='FactGrid property complaint')
FactGrid_user_page = P(163, range=IRI, label='FactGrid user page')
FactGrid_visualisation = P(693, range=IRI, label='FactGrid visualisation', description='Link pointing to a map generated with the QueryService')
family_database_Juden_im_Deutschen_Reich_ID = P(1068, range=ExternalId, label='family database "Juden im Deutschen Reich" ID')
Family_various = P(629, range=Item, label='Family various')
Fathers_status = P(615, range=Item, label='Father\'s status')
Fellow_student = P(485, range=Item, label='Fellow student', description='designation of students for their fellow students')
Feudal_obligation = P(1013, range=Quantity, label='Feudal obligation')
Field_of_engagement_expertise = P(452, range=Item, label='Field of engagement / expertise', description='to mention fields for which an organisation is responsible')
Field_of_knowledge = P(608, range=Item, label='Field of knowledge', description='to mention fields of knowledge in which a work has been published or to which it is designed to contribute')
Field_of_offices_in_the_Roman_Catholic_Church = P(1018, range=Item, label='Field of offices in the Roman Catholic Church')
Field_of_research = P(97, range=Item, label='Field of research', description='use this property to create a context that will define searches of your project\'s research interest.')
Finding_spot = P(695, range=Item, label='Finding spot', description='place where an object has been found, e.g. in an archaeological excavation')
Fineness_1000 = P(405, range=Quantity, label='Fineness (/1000)', description='content of precious metal')
First_documented_in = P(631, range=Item, label='First documented in')
Folios = P(100, range=String, label='Folio(s)', description='qualifier to refer to a specific sheet number or range (like:  5v-7r) in the work referenced in the preceding main statement')
Font_size = P(1299, range=Quantity, label='Font size', description='give value in px, pt, millimeters or centimetres')
Footnote = P(102, range=String, label='Footnote', description='qualifier to refer to a specific footnote in the work that is referenced with the main statement.')
Format = P(93, range=Item, label='Format', description='file format, physical medium, or dimensions of the resource. Refers to items like folio or A4')
format_as_a_regular_expression = P(1044, range=String, label='format as a regular expression')
Formed_a_set_with = P(409, range=Item, label='Formed a set with', description='to name objects that originally belonged together')
Forum_München_ID = P(728, range=ExternalId, label='Forum München ID', description='Identifier of the database of the Forum Queeres Archiv München e.V.')
Francke_Foundations_Bio_ID = P(998, range=ExternalId, label='Francke Foundations Bio ID')
Frankfurter_Personenlexikon = P(716, range=ExternalId, label='Frankfurter Personenlexikon', description='Scientific online encyclopedia with Frankfurt biographies from over 1,200 years of city history')
Frauen_in_Bewegung_1848_1938_ID = P(667, range=ExternalId, label='Frauen in Bewegung 1848–1938 ID', description='identifier for entries in the ARIADNE “Frauen in Bewegung 1848–1938” database, published by the Austrian National Library')
Friends_with = P(192, range=Item, label='Friends with', description='name the person with whom the subject is a friend')
Fruitbearing_Society_Member_ID = P(794, range=ExternalId, label='Fruitbearing Society Member ID')
Funeral_speech_by = P(470, range=Item, label='Funeral speech by', description='um die Autoren von Leichenreden zu nennen')
fuzzy_sl_ID = P(1215, range=ExternalId, label='fuzzy-sl ID', description='ID in the fuzzy-sl Wikibase instance')
Genealogycom_ID = P(1090, range=ExternalId, label='Genealogy.com-ID')
Genicom_profile_ID = P(374, range=ExternalId, label='Geni.com profile ID')
GeoNames_ID = P(418, range=ExternalId, label='GeoNames ID', description='identifier in the GeoNames geographical database')
German_municipality_key = P(1072, range=ExternalId, label='German municipality key')
Germania_Sacra_database_of_persons_ID = P(472, range=ExternalId, label='Germania Sacra database of persons ID', description='Entry in Germania Sacra database of persons')
Getty_Thesaurus_of_Geographic_Names_ID = P(624, range=ExternalId, label='Getty Thesaurus of Geographic Names ID')
GitHub_username = P(719, range=ExternalId, label='GitHub username', description='username of this project, person or organization on GitHub')
Glottolog_ID = P(1326, range=ExternalId, label='Glottolog ID', description='identifier for a languoid in the Glottolog database')
GND_input_field = P(701, range=ExternalId, label='GND input field')
GND_network_graph = P(878, range=ExternalId, label='GND network graph', description='beta version of the new view and search tool for the Common Authority File')
Godfather_of_the_confirmand = P(504, range=Item, label='Godfather of the confirmand', description='godfather of a confirmand, accompanies the confirmand at the confirmation')
Gold_content_g = P(395, range=Quantity, label='Gold content (g)')
Google_Knowledge_Graph_ID = P(672, range=ExternalId, label='Google Knowledge Graph ID')
GOV_ID = P(1073, range=ExternalId, label='GOV-ID')
Grave = P(79, range=Item, label='Grave', description='Name the place where the person\'s grave is')
Grave_Row = P(1067, range=Quantity, label='Grave Row')
GS_vocabulary_term = P(1301, range=String, label='GS vocabulary term', description='term that belongs to Germania Sacra vocabularies')
Guardian = P(415, range=Item, label='Guardian', description='the legal representative of the person described; for incapable of business and underage (half) orphans up to the age of majority')
Hair_colour = P(643, range=Item, label='Hair colour', description='physical attribute e.g. blond')
HAIT_ID = P(1305, range=ExternalId, label='HAIT ID', description='Identifier in the Datenbank of the Hannah-Arendt-Institut für Totalitarismusforschung')
Handedness = P(640, range=Item, label='Handedness', description='whether left or right handed')
Handwritten_by = P(25, range=Item, label='Handwritten by', description='to identify the writer of a manuscript text')
Has_subclasses = P(420, range=Item, label='Has subclasses', description='to list the subclasses of a given class (P422) in a classification system')
HDS_ID = P(1129, range=ExternalId, label='HDS ID')
Heiress = P(417, range=Item, label='Heir(ess)', description='those who inherited an item')
Hex_color = P(696, range=String, label='Hex color', description='sRGB hex triplet format for subject color (e.g. 7FFFD4) specifying the 8-bit red, green and blue components')
Historic_county = P(538, range=Item, label='Historic county', description='to locate (UK places) in the respective traditional counties')
Historical_continuum = P(742, range=Item, label='Historical continuum', description='Germany\'s Weimar Republic and Third Reich, for example, have their continuity as Germany')
Historical_description = P(187, range=Text, label='Historical description', description='to quote a historical description of an object')
Homosaurus_ID_version_3 = P(727, range=ExternalId, label='Homosaurus ID (version 3)', description='international linked data vocabulary of Lesbian, Gay, Bisexual, Transgender, and Queer (LGBTQ) terms')
Honorific_prefix = P(745, range=Item, label='Honorific prefix', description='word or expression used before a name in addressing or referring to a person')
Hosted = P(210, range=Item, label='Hosted', description='to state actors or events to whom a person was offering its house as a meeting place')
House_numbering_system = P(646, range=Item, label='House numbering system', description='to state the house numbering in use')
HOV_ID = P(1156, range=ExternalId, label='HOV ID', description='Identifier for places in the Historical Place Directory of Saxony')
Iconography = P(1348, range=Item, label='Iconography', description='for example in Christianity the cross')
Identification_by = P(1296, range=Item, label='Identification by')
Ideological_political_positioning = P(661, range=Item, label='Ideological / political positioning', description='to assign a person or organization a position in the history of ideas (such as German idealism) or political ideology (such as communism)')
IdRef_ID = P(366, range=ExternalId, label='IdRef ID')
ie = P(620, range=Item, label='i.e.')
Image_content = P(705, range=Item, label='Image content', description='to state what or who is to be seen on a picture')
Image_number = P(55, range=String, label='Image number', description='property for internal use. Use (P138) if you can link a public visual source')
Image_source = P(484, range=Item, label='Image source', description='indication of an image that is not yet available on the web')
Immediate_superiors = P(456, range=Item, label='Immediate superiors', description='to name people who were immediate superiors in career positions')
Implemented_by = P(360, range=Item, label='Implemented by', description='use on a law or structural hierarchy in order to state organisations that have implemented this law or constitution')
In_consequence_of = P(464, range=Item, label='In consequence of', description='Property to refer to an event in which something happened')
In_his_her_personal_service = P(220, range=Item, label='In his/her personal service', description='to mention people who are serving in close personal contact as valet or secretary, specify "specific position" with Q166')
In_leading_position = P(14, range=Item, label='In leading position', description='the persons who runs an organization / business, use qualifier P166 position to state the respective position')
In_words = P(877, range=Text, label='In words', description='Property for resolving abbreviations')
Includes = P(9, range=Item, label='Includes', description='state components or content.')
Income = P(673, range=Quantity, label='Income', description='the income that a position, benefice brings')
Indication_the_object_existed = P(52, range=Item, label='Indication the object existed', description='if you have stated Q5 lost object use this property to indicate how we know they existed.')
INE_ID_Portugal = P(651, range=ExternalId, label='INE ID (Portugal)', description='identifier for Portuguese municipalities, districts and parishes, by the Portuguese National Statistical Institute (INE)')
INE_ID_Spain = P(650, range=ExternalId, label='INE ID (Spain)', description='identifier for Spanish municipalities, by the Spanish Statistical Office (INE)')
Infrastructure = P(881, range=Item, label='Infrastructure', description='property to name (e.g. in cities) infrastructure components such as post office, university, market')
Inpatient_treatment_in = P(1153, range=Item, label='Inpatient treatment in', description='to indicate a hospital or psychiatric institution where the person was treated')
Input_form = P(1146, range=IRI, label='Input form', description='URL for a data entry tool')
INSEE_municipality_code = P(414, range=ExternalId, label='INSEE municipality code', description='number of French statistics')
Instance_of = P(2, range=Item, label='Instance of', description='state what the item is')
Institution_addressed = P(130, range=Item, label='Institution addressed', description='to name an institution addressed in the document')
Interest_claim_per_annum = P(1012, range=Quantity, label='Interest claim (per annum)')
Internet_Archive_ID = P(1329, range=ExternalId, label='Internet Archive ID', description='identifier of archive.org')
Internetportal_Westfälische_Geschichte_ID_Persons_entry = P(1056, range=ExternalId, label='Internetportal Westfälische Geschichte ID, Persons entry')
Intervened_on_behalf_of = P(557, range=Item, label='Intervened on behalf of', description='to name interventions on behalf of Persons to be named. Add Qualifier P550 to state the persecution the respective person was facing.')
Inventory_position = P(10, range=String, label='Inventory position', description='number by which an object is referenced in a collection, library or archive; use as a qualifier under P329 statement')
Inverse_label_item = P(597, range=Item, label='Inverse label item', description='item with label/aliases of the inverse relationship of a property')
Inverse_property = P(86, range=Property, label='Inverse property', description='e.g. child one the one hand and father and mother on the other')
ISBN_10 = P(605, range=ExternalId, label='ISBN-10', description='former identifier for a book (edition), ten digits. Used for all publications up to 2006 (convertible to ISBN-13 for some online catalogs; useful for old books or facsimiles not reedited since 2007')
ISBN_13 = P(606, range=ExternalId, label='ISBN-13', description='identifier for a book (edition), thirteen digits. Standard after 2006 (replaces ISBN-10, see P605)')
ISO_3166_1_alpha_2_code = P(870, range=ExternalId, label='ISO 3166-1 alpha-2 code', description='identifier for a country in two-letter format per ISO 3166-1')
ISO_3166_1_alpha_3_code = P(871, range=ExternalId, label='ISO 3166-1 alpha-3 code', description='identifier for a country in three-letter format per ISO 3166-1')
ISO_3166_1_numeric_code = P(872, range=ExternalId, label='ISO 3166-1 numeric code', description='identifier for a country in numeric format per ISO 3166-1')
ISO_3166_2 = P(873, range=ExternalId, label='ISO 3166-2', description='identifier for a country subdivision per ISO 3166-2 (include country code)')
ISO_3166_3 = P(874, range=ExternalId, label='ISO 3166-3', description='identifier for a country name that has been deleted from ISO 3166-1 since its first publication in 1974')
ISO_639_2 = P(876, range=ExternalId, label='ISO 639-2', description='3-letter identifier for language, macro-language or language family, defined in ISO 639-2 standard')
ISO_639_5 = P(875, range=ExternalId, label='ISO 639-5', description='3-letter identifier for language family or collective code per ISO 639-5')
ISSN = P(743, range=ExternalId, label='ISSN', description='International Standard Serial Number (print or electronic)')
Issue = P(1117, range=String, label='* Issue')
ISTC_ID = P(645, range=ExternalId, label='ISTC-ID', description='to link to Incunabula Short Title Catalogue identifiers of the Consortium of Research Libraries (CERL)')
Item_count_to = P(884, range=Quantity, label='Item count to', description='Propriété permettant de préciser le deuxième volet pour un tirage de 30 000 à 35 000 exemplaires')
Joint_partners = P(191, range=Item, label='Joint partners', description='persons with business shares in a company')
Julian_calendar_stabiliser = P(88, range=String, label='Julian calendar stabiliser', description='qualifier to note the Julian date in string format (1785-03-21) to have a stabilised display on the (by default Gregorian) Query Service')
K10plus_PPN_ID = P(346, range=ExternalId, label='K10plus PPN ID', description='identifier in the K10plus union catalog of the Common Library Network (GBV) and the South-West German Library Network (SWB)')
Kalliope_ID = P(635, range=ExternalId, label='Kalliope ID', description='ID of the German Kalliope union catalogue for personal papers and autographs in libraries, archives and museums')
KATOTTH_ID = P(1050, range=ExternalId, label='KATOTTH ID')
Key_data = P(1307, range=Quantity, label='Key data', description='for example in an election: number of eligible voters, votes cast, voter turnout')
KGI4NFDI_ID = P(1340, range=ExternalId, label='KGI4NFDI ID', description='an ID in the Knowledge Graph Infrastructure (KGI) run by BASE4NFDI')
Kiel_Scholars_Directory_ID = P(1347, range=ExternalId, label='Kiel Scholars\' Directory ID')
Klosterdatenbank_ID = P(471, range=ExternalId, label='Klosterdatenbank ID', description='Entry in the database "monasteries, convents and collegiate churches", Germania Sacra')
KOATUU_ID = P(1026, range=ExternalId, label='KOATUU-ID')
Language = P(18, range=Item, label='Language', description='language of work, document, name, or concept')
Language_skills = P(460, range=Item, label='Language skills', description='specify with P621 mother tongue etc.')
Last_holding_archive_of_the_lost_object = P(348, range=Item, label='Last holding archive of the lost object', description='to state the last institution that had the (missing) object. Use if P2 had a Q5 (missing object) statement')
Last_modified = P(612, range=Time, label='Last modified', description='e.g. to state, when certain documents were first bound together in this combination, or when a file received its specific material composition')
Last_professional_status = P(211, range=Item, label='Last professional status', description='Qualifier to be added to retirement statements')
Leaseholder = P(1010, range=Item, label='Leaseholder')
Leaser = P(1011, range=Item, label='Leaser')
Legal_form = P(862, range=Item, label='Legal form', description='legal form of an entity')
Legislative_term = P(795, range=Item, label='Legislative term')
Length_distance = P(404, range=Quantity, label='Length /distance')
Level_of_qualification = P(621, range=Item, label='Level of qualification')
License = P(180, range=Item, label='License', description='state under what license information you have imported can be used.')
Licensed_by = P(733, range=Item, label='Licensed by', description='the person or authority that gave the permission for instance to publish a manuscript')
Liegelord = P(1294, range=Item, label='Liegelord')
Liegeman = P(1295, range=Item, label='Liegeman')
Likelihood_percent = P(869, range=Quantity, label='Likelihood (percent)')
Line = P(1030, range=String, label='Line')
LinkedIn_personal_profile_ID = P(709, range=ExternalId, label='LinkedIn personal profile ID', description='identifier for a person, on the LinkedIn website')
Listed_in = P(124, range=Item, label='Listed in', description='to refer to bibliographies and catalogues that noted the object (especially useful on lost items)')
Literal_statement = P(35, range=String, label='Literal statement', description='Use this as a qualifier to state how e.g. a name was actually spelled.')
Literal_translation = P(1144, range=Text, label='Literal translation', description='Qualifier that allows different translations to be added to a text quotation')
Live_stock = P(1016, range=Quantity, label='Live stock')
Living_people_protection_class = P(723, range=Item, label='Living people protection class', description='to note properties to be handled with special care where they touch personal information of living people')
Lizenznummer_of_books_printed_in_the_GDR = P(1093, range=String, label='Lizenznummer (of books printed in the GDR)')
Local_units_of_measurement = P(386, range=Item, label='Local units of measurement')
Localisation = P(47, range=Item, label='Localisation', description='geographical place of a building, an event or activity; see also P83 for place of residence')
Location_in_the_property = P(1342, range=Item, label='Location in the property', description='Description of the location of a room, an apartment, etc. in a building property, write down word statements if necessary with temporal or geographical restriction of use')
Lodge_Matriculation_number = P(669, range=Quantity, label='Lodge Matriculation number', description='use this statement as a qualifier on P430 Grand Lodge statements to state the registry number')
Maintained_by = P(1162, range=Item, label='Maintained by')
Mainzer_Ingrossaturbücher_ID = P(1057, range=ExternalId, label='Mainzer Ingrossaturbücher ID')
Maitron_ID = P(1065, range=ExternalId, label='Maitron ID')
Maps_and_plans = P(663, range=Item, label='Maps and plans', description='to list maps and plans of the location')
Married_to = P(84, range=Item, label='Married to', description='to record a registered official couple relationship')
Mass = P(397, range=Quantity, label='Mass')
Matching = P(407, range=Quantity, label='Matching', description='to state an equivalent in another currency')
Material_composition = P(401, range=Item, label='Material composition')
Matrikelportal_Rostock_since_1419_ID = P(1058, range=ExternalId, label='Matrikelportal Rostock (since 1419) ID')
Measures_taken = P(1200, range=Item, label='Measures taken')
Media_type = P(15, range=Item, label='Media type', description='e.g. manuscript, typescript, drawing')
Medical_cause_of_death = P(162, range=Item, label='Medical cause of death')
Medical_condition = P(186, range=Item, label='Medical condition', description='any state relevant to the health of an organism, especially diseases')
Medical_treatment = P(1135, range=Item, label='Medical treatment', description='qualifier that allows treatments and dosages of medications to be recorded under a P186 statement')
Medically_tended_by = P(512, range=Item, label='Medically tended by', description='to name doctors who looked after a patient')
Meeting_point_of = P(726, range=Item, label='Meeting point of', description='to state an organisation that is meeting (regularily) at the location')
Memorial_Archives_ID = P(1216, range=ExternalId, label='Memorial Archives ID', description='The Memorial Archives are the digital research platform of the Flossenbürg Concentration Camp Memorial. The online database contains information about prisoners in many camps.')
Mode_of_presentation = P(698, range=Item, label='Mode of presentation', description='to describe how a story is presented, e.g. as personal history of the central protagonist in a first person narrative')
Musical_notation = P(790, range=Item, label='Musical notation')
Named_after = P(461, range=Item, label='Named after', description='To refer to the Item that has inspired the name')
Naming = P(34, range=Text, label='Naming', description='to state historical names; use qualifiers P49/P50 or P290/P291 to date observations')
Naming_of_the_titles_central_protagonist = P(619, range=Item, label='Naming of the title\'s central protagonist')
Naming_the_plural = P(1206, range=Item, label='Naming the plural')
Naming_the_singular = P(1205, range=Item, label='Naming the singular', description='to refer to the item that has the singular')
NDBA_ID = P(1133, range=ExternalId, label='NDBA ID', description='identifier of a person in the online \'Nouveau dictionnaire de biographie alsacienne\'')
Negative_search_result = P(468, range=Item, label='Negative search result', description='use to list archives and resources that did not yield any results, give date of the result with P432')
Next_higher_rank_or_degree = P(356, range=Item, label='Next higher rank or degree', description='e.g. in a masonic system the next higher degree')
Next_version = P(219, range=Item, label='Next version', description='to identify an ensuing version of a text or work')
NNDB_People_ID = P(1203, range=ExternalId, label='NNDB People-ID')
Normalization_variant = P(868, range=Item, label='Normalization variant', description='in particular to refer to a more common standard variant in the name, which works similarly to a main category here')
Not_noted_in = P(599, range=Item, label='Not noted in', description='to state that the item is not noted in source referred to')
Not_to_be_confused_with = P(514, range=Item, label='Not to be confused with', description='use this property to warn others not to merge the items listed')
Note = P(73, range=String, label='Note', description='Field for free notes')
Number = P(90, range=String, label='Number', description='to state, for instance, the number a lodge has in a register, or a page or item number in a reference. Use P499 if all numbers are strictly numerical.')
Number_making_a_unit = P(406, range=Quantity, label='Number making a unit', description='of coins for instance: 20 shillings make one pound')
Number_of_abstentions = P(1309, range=Quantity, label='Number of abstentions', description='number of voters that were present but refrained from voting on a specific issue')
Number_of_blank_votes = P(1314, range=Quantity, label='Number of blank votes', description='number of blank votes in a voting round for a specific position in a election')
Number_of_children = P(200, range=Quantity, label='Number of children', description='to name the number of children of a father or mother')
Number_of_copies_extant = P(654, range=Quantity, label='Number of copies extant', description='to state how many copies of a (e.g. print) run can still be located')
Number_of_copies_printed = P(653, range=Quantity, label='Number of copies printed', description='in a serial production the number of objects created in the same (eg. print) run')
Number_of_female_children = P(201, range=Quantity, label='Number of female children', description='to name the number of the female children')
Number_of_integrated_items = P(613, range=Quantity, label='Number of integrated items')
Number_of_male_children = P(202, range=Quantity, label='Number of male children', description='to name the number of the male children')
Number_of_objects_within_a_collection = P(1017, range=Quantity, label='Number of objects within a collection')
Number_of_participants_members = P(666, range=Quantity, label='Number of participants /members', description='for instance of an organisation or event')
Number_of_sets_ordered = P(542, range=Quantity, label='Number of sets ordered', description='to state the number of copies ordered in a subscription')
Number_of_spoilt_votes = P(1313, range=Quantity, label='Number of spoilt votes', description='number of spoilt votes in a voting round for a specfic position in a election')
NUTS_code = P(1332, range=ExternalId, label='NUTS code', description='identifier for a region per NUTS')
OARE_ID = P(1085, range=ExternalId, label='OARE ID')
OATP_ID = P(1087, range=String, label='OATP ID')
Object_of_payment = P(688, range=Item, label='Object of payment', description='to determine what the specified payment was made for')
Object_of_procedure = P(797, range=Item, label='Object of procedure')
Object_paid = P(880, range=Quantity, label='Object paid', description='(qualifier) to specify payments from the object to the subject in the statement')
Objected_by = P(713, range=Item, label='Objected by', description='to state people who objected to a proposal')
Objects_of_interest = P(497, range=Item, label='Objects of interest')
Objects_of_knowledge = P(600, range=Item, label='Objects of knowledge', description='to state objects studied in a certain field of knowledge')
OCLC_ID = P(595, range=ExternalId, label='OCLC ID', description='identifier for a unique bibliographic record in OCLC WorldCat')
Of_importance_to = P(753, range=Item, label='Of importance to', description='general property to state persons or groups to whom the item has a particular relevance')
Official_website = P(156, range=IRI, label='Official website')
Old_inventory_position = P(30, range=String, label='Old inventory position', description='use for a shelf mark that is no longer current')
On_the_side_of = P(739, range=Item, label='On the side of', description='to name the war party or alliance for a person or a combat unit for which the operation took place')
Online_image = P(188, range=IRI, label='Online image', description='FactGrid property to refer to a web page (without Wikimedia-commons) that offers n image (e.g., a portrait)')
Online_presentation = P(596, range=IRI, label='Online presentation', description='to link to an online presentation e.g. as given at a conference')
Online_primary_documents = P(157, range=IRI, label='Online primary documents')
Online_translation = P(195, range=IRI, label='Online translation', description='state the URL of a translation')
OpenHistoricalMap_ID = P(1119, range=ExternalId, label='OpenHistoricalMap ID')
Opponent_of_the_disputation = P(390, range=Item, label='Opponent of the disputation')
Opposite_of = P(630, range=Item, label='Opposite of')
Options = P(183, range=Item, label='Options', description='to open up a framework of possibilities or list a repertoire')
ORACC_id_word = P(1086, range=String, label='ORACC id_word')
ORCID_ID = P(408, range=ExternalId, label='ORCID ID', description='ID in the Open Researcher and Contributor database')
Ordained_consecrated_by = P(1025, range=Item, label='Ordained / consecrated by')
Organisation_open_from_here = P(358, range=Item, label='Organisation open from here', description='to state the next higher structure of degrees and positions of an organisation')
Organisation_signing_responsible = P(1150, range=String, label='* Organisation signing responsible', description='string version of P66: to state the agency that takes responsibility, as recorded')
Organisational_aspects = P(1022, range=Item, label='Organisational aspects')
Original_language = P(1157, range=Item, label='Original language')
Owned_by = P(126, range=Item, label='Owned by', description='the owner of the item')
Owner_of = P(175, range=Item, label='Owner of', description='objects owned by statement\'s subject')
Page_layout = P(481, range=Item, label='Page layout', description='see the items for this property for possible answers')
Pages = P(54, range=String, label='Page(s)', description='use this to state the page or pages in an bibliographic reference')
Part_of = P(8, range=Item, label='Part of', description='to state the larger complex in which the object is a component.')
Part_of_the_collection = P(123, range=Item, label='Part of the collection', description='to state a collection to which an item belongs or belonged. (See also P323 to state the next higher level of archival integration)')
Patients = P(513, range=Item, label='Patient(s)', description='to name patients of a doctor or medical facility')
Payment_interval = P(687, range=Item, label='Payment interval', description='yearly or monthly wage, continuous revenue, or one time fee')
Payment_recipient = P(659, range=Item, label='Payment recipient', description='the recipient of a monetary transaction')
Payment_sender = P(657, range=Item, label='Payment sender', description='the giver in the monetary transaction')
Payment_transactor = P(658, range=Item, label='Payment transactor', description='the intermediary of a payment, usually a bank')
Peerage_person_ID = P(1062, range=ExternalId, label='Peerage person ID')
Percentage = P(402, range=Quantity, label='Percentage')
Person_for_whom_the_document_was_written = P(607, range=Item, label='Person for whom the document was written', description='Property for documents, especially from law firm business')
Person_signing_responsible = P(453, range=Item, label='Person signing responsible', description='to name person(s) or organization(s) responsible for the this item')
Personal_connections = P(703, range=Item, label='Personal connections', description='general property to link people in various personal or professional relationships that are not covered by the more common properties')
Personal_inspection_by = P(411, range=Item, label='Personal inspection by', description='to state those who saw a document or object')
Personal_servant_of = P(486, range=Item, label='Personal servant of', description='to state the item (person or organization) which is served by this item (person or organization)')
Persons_mentioned = P(33, range=Item, label='Persons mentioned', description='to identify persons mentioned in a text')
Persons_of_Indian_Studies_ID = P(689, range=ExternalId, label='Persons of Indian Studies ID', description='identifier for an Indologist on the \'Persons of Indian Studies\' website')
PhiloBiblon_ID = P(476, range=ExternalId, label='PhiloBiblon ID', description='Identifier of the PhiloBiblon project')
Photo_Cardboard_Manufacturer = P(1360, range=Item, label='Photo Cardboard Manufacturer', description='Property, to record the manufacturers of the cardboard plates printed with advertising, which photo studios used until about 1915 to mount albumen paper prints')
Photographic_Studio = P(1204, range=Item, label='Photographic Studio')
Pilgrimage_to = P(1130, range=Item, label='Pilgrimage to')
Place_of_address = P(83, range=Item, label='Place of address', description='use for geographic places like towns and villages, specify address with P208')
Place_of_baptism = P(169, range=Item, label='Place of baptism')
Place_of_birth = P(82, range=Item, label='Place of birth', description='place where a person was born (village, city, town)')
Place_of_death = P(168, range=Item, label='Place of death')
Place_of_detention = P(216, range=Item, label='Place of detention', description='Name here the place and the time a person was in prison')
Place_of_education = P(501, range=Item, label='Place of education', description='property to use if we cannot reference a particular school but have a place name')
Place_of_publication = P(1141, range=String, label='* Place of publication', description='string version of P241: place of publication, as given in the imprint. Also use for the place of writing a manuscript, in both cases, as recorded. Use P240 if you assume that a given publishing place is actually misleading')
Pleiades_ID = P(671, range=ExternalId, label='Pleiades ID', description='identifier for a place in Pleiades hosted at pleiades.stoa.org')
Plus = P(400, range=Quantity, label='Plus')
PMB_person_ID = P(1064, range=ExternalId, label='PMB person ID')
Position_held = P(164, range=Item, label='Position held')
Position_in_sequence = P(499, range=Quantity, label='Position in sequence', description='to state the sequence number of an item in a list; useful for sorting a list in numerical order')
Possibly_identical_to = P(120, range=Item, label='Possibly identical to', description='to propose a specific identification - for example a named person')
Post_included = P(380, range=Item, label='Post included')
Precision_of_begin_date = P(785, range=Item, label='Precision of begin date')
Precision_of_begin_date_string = P(787, range=String, label='Precision of begin date [string]')
Precision_of_date = P(467, range=Item, label='Precision of date', description='FactGrid qualifier for the specific determination of the exactness of a date')
Precision_of_end_date = P(786, range=Item, label='Precision of end date')
Precision_of_end_date_string = P(788, range=String, label='Precision of end date [string]')
Predominant_gender_usage = P(625, range=Item, label='Predominant gender usage')
Preface_by = P(179, range=Item, label='Preface by', description='to state the author of the preface to a publication')
Preferred_designation = P(1331, range=Text, label='Preferred designation')
Premiere = P(714, range=Item, label='Premiere', description='to refer to the first performance of a piece (for which a separate object should be created)')
Preservation = P(158, range=Item, label='Preservation')
Presiding_the_disputation = P(388, range=Item, label='Presiding the disputation')
Previous_version = P(218, range=Item, label='Previous version', description='to refer to a previous version of a text or object')
Primary_source = P(51, range=Item, label='Primary source', description='to state contemporary and primary sources of knowledge - like a birth certificate.')
Printed_by = P(207, range=Item, label='Printed by', description='to name the company that printed a publication')
Prisoner_of_war_of = P(752, range=Item, label='Prisoner of war of', description='to state the nation whose prisoner the person became')
Process_File_number = P(1197, range=Item, label='Process / File number')
Produced_by_brand = P(718, range=Item, label='Produced by (brand)', description='the brand name that suggests the company that produced or sold the item')
Produces_product_range = P(798, range=Item, label='Produces / product range')
Professional_address = P(865, range=Item, label='Professional address', description='street address where subject or organization is located for its activities, preferably full. Include building number, city/locality, post code, but not coun')
Programming_language = P(1319, range=Item, label='Programming language', description='the programming language(s) in which the software is developed')
Projects = P(177, range=Item, label='Projects', description='the project a person a person is/has been working on')
Pronunciation_IPA = P(1023, range=Text, label='Pronunciation (IPA)')
Property_constraint = P(627, range=Item, label='Property constraint')
Proposed_to_become_a_member_of = P(454, range=Item, label='Proposed to become a member of', description='to name an organisation the Item was proposed to join')
Pseudonym_of = P(193, range=Item, label='Pseudonym of', description='to identify people (or places) behind a specific pseudonym')
Public_awards_and_titles = P(171, range=Item, label='Public awards and titles')
Published_in = P(1137, range=String, label='* Published in', description='string version of P64: to state the publication in which an article or advertisement was published, as recorded in the publication')
Publisher = P(1140, range=String, label='* Publisher', description='entity (company or person) publishing or distributing the resource, as recorded (string version of P206)')
Publisher = P(206, range=Item, label='Publisher', description='entity (company or person) publishing or distributing the resource')
Publisher_as_misleadingly_stated = P(544, range=Item, label='Publisher as misleadingly stated', description='e.g. Pierre Marteau, Cologne')
Purpose = P(515, range=Item, label='Purpose', description='qualifier to state the task of a journey')
Qualifier = P(4, range=String, label='* Qualifier', description='use when it would be inappropriate or undesirable to create objects as an alternative to P155 (How sure is this?)')
RAG_ID = P(517, range=ExternalId, label='RAG ID', description='External identifier of the Repertorium Academicum Germanicum')
RAM_size = P(1322, range=Quantity, label='RAM size', description='random-access memory size whether required or offered')
Rank = P(1145, range=Item, label='Rank', description='position in a hierarchy')
Rank_service_number = P(1080, range=String, label='Rank service number')
re3data_D = P(1159, range=ExternalId, label='re3data D', description='Identifikator im Karlsruher re3data Repositorium')
Reason_for_deprecated_rank = P(1343, range=Item, label='Reason for deprecated rank', description='qualifier to indicate why a particular statement should have deprecated rank')
Reason_for_preferred_rank = P(1344, range=Item, label='Reason for preferred rank', description='qualifier to indicate why a particular statement should have preferred rank')
Receives_area_from = P(1337, range=Item, label='Receives area from', description='to record gains in area, for example after wars or reorganization of territories')
Recipient = P(28, range=Item, label='Recipient', description='The recipient of a letter. Add successive recipients with P499 qualifiers')
Recording_online_information = P(541, range=IRI, label='Recording, online information', description='website on a recording of a piece of music')
Regional_localisation = P(861, range=Item, label='Regional localisation', description='to refer to a region or landscape in which a place is located')
Registered_accepted_by = P(503, range=Item, label='Registered / accepted by', description='to name the person who received the person as a member of the respective organisation (not identical to P28)')
Registrar = P(738, range=Item, label='Registrar', description='person who registers a document in a register or letterbook')
Regular_meeting_point = P(209, range=Item, label='Regular meeting point', description='to name meeting points of an organisation or group')
Related_object = P(750, range=Item, label='Related object', description='open property to allow any imaginable relation between two or more objects; use qualifier P700 to state the kind of relationship')
Relation_constraint = P(628, range=Item, label='Relation constraint')
Religious_background = P(172, range=Item, label='Religious background')
Religious_order = P(746, range=Item, label='Religious order', description='to designate the membership in a religious order. Use P91 to state affiliation to a particular monastery')
Relocated_subject = P(1198, range=Item, label='Relocated subject')
Repertorium_Germanicum_ID = P(473, range=ExternalId, label='Repertorium Germanicum ID', description='Entry of the online database of the Repertorium Germanicum')
Repertorium_Poenitentiariae_Germanicum_ID = P(1128, range=ExternalId, label='Repertorium Poenitentiariae Germanicum ID')
Reported_event = P(19, range=Item, label='Reported event', description='the event which is reported')
Request_FactGrid = P(592, range=IRI, label='Request FactGrid', description='FactGrid internal property')
Request_name = P(593, range=Item, label='Request name', description='to give a name to the request as a qualifier on P592')
Research_projects_that_contributed_to_this_data_set = P(131, range=Item, label='Research projects that contributed to this data set', description='add either your personal FactGrid ID or the ID of your research project')
Research_stay_in = P(351, range=Item, label='Research stay in', description='to note journeys in research projects')
ResearchGate_profile_ID = P(712, range=ExternalId, label='ResearchGate profile ID', description='identifier for a person, used by ResearchGate profiles')
Respondent_of_the_disputation = P(389, range=Item, label='Respondent of the disputation')
Revised_by = P(22, range=Item, label='Revised by', description='the person who determined the version of the work, for example through text editing, compilation, adaptation - determine the role more precisely with P820')
RI_ID = P(791, range=ExternalId, label='RI ID')
RISM_ID = P(655, range=ExternalId, label='RISM ID', description='identifier for a person, institution, or work in the Répertoire International des Sources Musicales database')
Romanised_transcription = P(670, range=String, label='Romanised transcription', description='A Latin spelling based on a reading a non-Latin script (for transliteration see P1096)')
Room_number = P(1032, range=String, label='Room number')
Rosicrucian_code_name = P(354, range=Item, label='Rosicrucian code name', description='to state a person\'s code name in the  Rosicrucian brotherhood')
Rosicrucian_code_name_of = P(353, range=Item, label='Rosicrucian code name of', description='to state the bearer of a secret name in the Rosicrucian connection')
Said_to_be_the_same_as = P(493, range=Item, label='Said to be the same as', description='to identify traditions that claimed an identity of two items; add the P129 "according to" as a qualifier')
School_adherence = P(623, range=Item, label='School adherence')
Script_style = P(747, range=Item, label='Script style', description='the style of handwriting in a manuscript, see also typeface P748')
Seal = P(355, range=Item, label='Seal', description='to identify a seal')
Seal_ID = P(1084, range=String, label='Seal ID')
Secondary_literature_research = P(12, range=Item, label='Secondary literature / research', description='to document the reception and research literature')
Secondary_literature_research_literal = P(1053, range=String, label='Secondary literature / research [literal]')
See_also_property = P(85, range=Property, label='See also property', description='to refer to properties of a similar use')
Segmentation = P(543, range=Item, label='Segmentation', description='to state the individual parts of a book from title page and preface to index = table of contents or of other kind of publication, e.g., an article in parts')
Sejm_Wielkipl_profile_ID = P(1024, range=ExternalId, label='Sejm-Wielki.pl profile ID')
Semantic_Kompakkt_ID = P(1214, range=ExternalId, label='Semantic Kompakkt ID', description='ID in the Semantic Kompakkt Wikibase instance')
Series = P(1139, range=String, label='* Series', description='to name e.g. the journal in which an issue was published; to name the series in which a volume was published, as recorded (string version of P441)')
Set_by = P(737, range=Item, label='Set by', description='qualifier to state on whose decree a certain value or answer was set')
Sexual_orientation = P(711, range=Item, label='Sexual orientation', description='the preferred orientation in sexual relationships, use if possible contemporary self-assertions')
short_digest = P(1148, range=Text, label='short digest')
Siblings = P(203, range=Item, label='Sibling(s)', description='to name the siblings (brother, sister, etc) of a person')
Signed_by = P(410, range=Item, label='Signed by', description='to name those who contributed to a work')
Silver_content = P(403, range=Quantity, label='Silver content')
Skin_colour = P(642, range=Item, label='Skin colour', description='genetical differences in skin colour among individuals is caused by variation in pigmentation')
Source_literal = P(721, range=String, label='Source [literal]', description='compared to P129: alternative property for references for which no Q-item is available')
Spanish_Biographical_Dictionary_ID = P(707, range=ExternalId, label='Spanish Biographical Dictionary ID')
Specific_statement = P(166, range=Item, label='Specific statement')
Split_off = P(457, range=Item, label='Split-off', description='to name organisations that left the organisation')
Split_off_from = P(458, range=Item, label='Split-off from', description='to name the organisation from which the present departed')
Sponsor_supporter = P(735, range=Item, label='Sponsor / supporter', description='to state the person who offered his/her patronage')
SS_KL_Auschwitz_Garrison_ID = P(1195, range=ExternalId, label='SS KL Auschwitz Garrison ID')
SS_membership_number = P(1191, range=ExternalId, label='SS membership number')
SS_Resettlement_ID = P(1196, range=ExternalId, label='SS Resettlement ID', description='ID number of the Volksdeutsche Mittelstelle')
Start_time_of_reported_events = P(45, range=Time, label='Start time of reported events', description='e.g. first date in a diary')
Statement_denied_by = P(1160, range=Item, label='Statement denied by', description='qualifier to name persons, groups or ideological constructs that question a statement')
Statement_refers_to = P(1142, range=String, label='* Statement refers to', description='string version of P700: qualifier to specify a statement, for instance if you have two statements of height referring to different aspects, as recorded')
Statement_refers_to = P(700, range=Item, label='Statement refers to', description='qualifier to specify a statement, for instance if you have two statements of height referring to different aspects')
Stature = P(639, range=Item, label='Stature', description='e.g. slim, stout, obese, athletic')
Status_of_possesion = P(127, range=Item, label='Status of possesion', description='to make a more detailed statement on the extent to which an object belongs to an owner (such as a deposit)')
Status_of_the_deceased_husband = P(614, range=Item, label='Status of the (deceased) husband')
Stored_in = P(226, range=Item, label='Stored in', description='state the container in which the object is to be found')
Strict_Observance_order_name = P(363, range=Item, label='Strict Observance order name', description='use on the person\'s side to name the pseudonym someone has received in the Strict Observance')
Structural_hierarchies_implemented = P(359, range=Item, label='Structural hierarchies implemented', description='to state the hierarchical structures an organisation has implemented')
Student = P(190, range=Item, label='Student', description='notable student(s) of an individual')
Student_of = P(161, range=Item, label='Student of')
Subclass_of = P(3, range=Item, label='Subclass of', description='if the item is a single object to be handled under an individual name use P2 to state what it is. If it is a class to be defined rather than named use P3 to state the next larger classes in which it is contained.')
Subject_evicted = P(1199, range=Item, label='Subject evicted')
Subject_matter_that_raised_objections = P(676, range=Item, label='Subject matter that raised objections', description='to refer to things that were brought into consideration against the initiative; add a P677 qualifier to state the (e.g. legal) basis of the concern')
Subject_of_negotiation = P(674, range=Item, label='Subject of negotiation', description='notes the subject of a negotiation, for instance an office to be granted in an application process')
Subject_paid = P(879, range=Quantity, label='Subject paid', description='such as a tuition fee upon enrolment')
Subject_topic_heading = P(1094, range=Text, label='Subject / topic / heading')
Subjected = P(751, range=Item, label='Subjected', description='to name those who became subjects of a measure - for instance the person who was beheaded in on the event of a particular execution')
Subjected_to = P(550, range=Item, label='Subjected to', description='link to events to name measures of persecution such as internment or deportation in the context of the Holocaust, use in addition P216 if you want to list facilites repression')
Subsidiary = P(419, range=Item, label='Subsidiary', description='a filial organisation')
Subunit_of = P(13, range=Item, label='Subunit of', description='to give definitions for instance of coins, use P406 to state the number that makes a unit')
Subunits = P(399, range=Item, label='Subunits')
Supplied_by = P(1212, range=Item, label='Supplied by', description='to record who supplied a person or organization with goods')
Sustainability = P(999, range=Item, label='Sustainability')
Swedish_portrait_archive_ID = P(379, range=ExternalId, label='Swedish portrait archive ID')
Swiss_municipality_code = P(1081, range=ExternalId, label='Swiss municipality code')
Symbolises = P(1349, range=Item, label='Symbolises')
System_component_of = P(372, range=Item, label='System component of')
Sächsische_Biografie_ID = P(1328, range=ExternalId, label='Sächsische Biografie ID', description='Biography portal for Saxon regional history of the Institute for Saxon History and Folklore')
Target_language = P(213, range=Item, label='Target language', description='to state the language into which a dictionary is translating')
Taxable_assets = P(1324, range=Quantity, label='Taxable assets', description='assets that a person or company has to pay tax on after deducting legally determined factors')
Taxon_range = P(1158, range=Item, label='Taxon range', description='geographic area(s) where a taxon is found')
Taxonomic_name = P(632, range=String, label='Taxonomic name')
Team = P(178, range=Item, label='Team', description='to state the team members of a project. Use P166 position to state different team positions')
Term_attributed_by = P(421, range=Item, label='Term attributed by', description='Property that records who coined a particular term, such as "Axis of Evil" George W. Bush')
Text_justification_legal_basis_constitution = P(555, range=Item, label='Text justification / legal basis / constitution', description='to name the legal basis of an intervention')
Time_of_day = P(509, range=String, label='Time of day', description='use  18:22:45 format for 6 pm, 22 minutes 45 seconds. Add Property 510 to name the place or time Zone')
Title = P(11, range=String, label='Title', description='to state the name of a resource, e.g., a book, painting, or document')
Title_page_transcript = P(5, range=String, label='Title page transcript', description='give a transcript of the title page')
to = P(1346, range=Item, label='to', description='Qualifier that, for example, notes a verse available as an item up to which a passage runs')
Total_valid_votes = P(1312, range=Quantity, label='Total valid votes', description='vote count for the elections (excluding invalid votes)')
Transacted_object = P(1201, range=Item, label='Transacted object', description='broadly thought of from the house that is inherited to the judgment that is passed on someone')
Translator = P(24, range=Item, label='Translator', description='to state people who brought a text into another language')
Transliteration = P(1155, range=Text, label='Transliteration', description='string-literal transliteration, an alphabetic-syllabic hyphenated spelling of logographic or hieroglyphic writing systems (for normalization see P670)')
Tribe = P(494, range=Item, label='Tribe', description='refer to a tribe or nation, for example the tribal affiliation of a person in the biblical books')
Truth_context = P(225, range=Item, label='Truth context', description='to name a context in which the item is assumed to be real')
Type_of_treatment = P(792, range=Item, label='Type of treatment')
Type_of_work = P(121, range=Item, label='Type of work', description='Use this property to organise works according to types of production')
Typeface = P(748, range=Item, label='Typeface', description='style of type used in a print publication')
Typology = P(754, range=Item, label='Typology', description='to indicate the typologies to which the type belongs')
Underlying_problem = P(677, range=Item, label='Underlying problem', description='in particular a qualifier to open up the problem that arose with the statement')
URL = P(887, range=IRI, label='URL', description='to provide a link to a data set made available online')
URN_formatter = P(744, range=String, label='URN formatter', description='formatter to generate Uniform Resource Name (URN) from property value. Include $1 to be replaced with property value')
USTC_editions_ID = P(647, range=ExternalId, label='USTC editions ID', description='Identifier of the Universal Short Title Catalogue')
Value_price = P(545, range=Quantity, label='Value / price', description='to collect e.g. information on prices - to be fixed to objects and services')
Vasserot_ID_streets_of_Paris = P(1193, range=ExternalId, label='Vasserot ID (streets of Paris)', description='table of parcel plans from the Vasserot Atlas (1810-1836) for a public road in Paris')
VD16_ID = P(368, range=ExternalId, label='VD16 ID')
VD17_ID = P(369, range=ExternalId, label='VD17 ID')
VD18_ID = P(370, range=ExternalId, label='VD18 ID')
Verdict = P(483, range=Item, label='Verdict', description='decision in a trial before a panel (to be named) with place and date')
Vergue_ID = P(660, range=ExternalId, label='Vergue ID', description='identifier in the Vergue online collection of photographs')
VIAF_ID = P(378, range=ExternalId, label='VIAF ID')
Visual_work_component = P(801, range=Item, label='Visual work component')
Visual_work_components_by = P(611, range=Item, label='Visual work components by', description='property for all forms of visual design, qualify with P166 "painter", "engraver" etc.')
Voice_type = P(638, range=Item, label='Voice type', description='e.g. mezzo soprano')
Volume_as_a_quantity = P(1091, range=Quantity, label='Volume as a quantity')
Watermark = P(749, range=Item, label='Watermark', description='faint sign in a paper, usually as a company mark of the manufacturer; by extension the equivalent in digital facsimiles')
Well_Known_Text_Geometry = P(1035, range=String, label='Well-Known Text Geometry')
What_supports_this_identification = P(118, range=Item, label='What supports this identification', description='FactGrid qualifier to state a specific identification')
WIAG_ID = P(601, range=ExternalId, label='WIAG ID', description='identifier of the Göttingen academy project')
WIAG_Office_in_Sequence_ID = P(1100, range=ExternalId, label='WIAG Office in Sequence ID')
Wider_field_of_genres = P(122, range=Item, label='Wider field of genres', description='to capture a broader spectrum of genres')
Wikimedia_language_code = P(53, range=String, label='Wikimedia language code', description='identifier for a language on Wikimedia projects; usually but not always a standard language code from ISO 639')
With_manuscript_notes_by = P(352, range=Item, label='With manuscript notes by', description='to identify annotations in books and other documents')
Without = P(706, range=Item, label='Without', description='to state components that are missing in the item')
Work_to_be_subscribed = P(540, range=Item, label='Work to be subscribed', description='the work advertised in a subscription scheme')
Works_published_or_unpublished = P(174, range=Item, label='Works, published or unpublished', description='name objects produced by the person')
WorldCat_Identities_ID = P(594, range=ExternalId, label='WorldCat Identities ID', description='entity on WorldCat, use P595 OCLC control number for books')
Writing_surface = P(480, range=Item, label='Writing surface', description='in documents e.g. parchment, paper')
X_post_ID = P(1334, range=ExternalId, label='X post ID', description='identifier of a status on X/Twitter')
Yad_Vashem_name_genealogy_ID = P(549, range=ExternalId, label='Yad Vashem name genealogy ID', description='prosopographic database of the Yad Vashem Holocaust memorial Centre')
Zeitschriften_database_ID = P(1061, range=ExternalId, label='Zeitschriften database ID')
ZOBODAT_People_ID = P(1357, range=ExternalId, label='ZOBODAT-People-ID')
ZOBODAT_Publication_Article_ID = P(1359, range=ExternalId, label='ZOBODAT-Publication-Article-ID')
ZOBODAT_Publication_Series_ID = P(1358, range=ExternalId, label='ZOBODAT-Publication Series-ID')

__all__ = (
    '_1st_carry',
    '_2nd_carry',
    '_3D_model_external',
    'Abbot',
    'Accessibility',
    'According_to',
    'Accounts_held_in',
    'Accusation_of',
    'Actually_addressed_to',
    'ADB_Wikisource',
    'Additional_name_attributes',
    'Address_item',
    'Addressees_of_deliveries',
    'Admission_requirement_required_membership',
    'Adversary',
    'Age_from',
    'Age_up_to',
    'Akademie_der_Künste_Berlin_Member_ID',
    'Alleged_member_of',
    'Alternatively',
    'Amount_in_dispute',
    'Amount_of_the_penalty_payment',
    'Annex',
    'Answered_with',
    'Apartment',
    'Approved_by',
    'Archived_at_the_URL',
    'Archives_at',
    'Area',
    'Area_changes_to',
    'Area_ID',
    'Aristocratic_tenures',
    'Aristocratic_title',
    'Arolsen_Archives_Persons_ID',
    'Arrival',
    'Art_and_Architecture_Thesaurus_ID',
    'Article',
    'Associated_person',
    'Authenticated_by',
    'Author',
    'Author_as_strangely_stated',
    'BAG_code_for_Dutch_places_of_residence',
    'Ballots_cast',
    'Banns_of_marriage_date',
    'Based_on',
    'Bayrisches_Musiker_Lexikon_Online_ID',
    'Bearer',
    'Bearer_of_the_Coat_of_Arms',
    'Begin_date',
    'Begin_text_span',
    'Beginning_of_composition',
    'Best_practice_notice',
    'Bestellnummer_of_books_printed_in_the_GDR',
    'Binding',
    'Biographical_notes',
    'Blood_type',
    'BNE_ID',
    'BnF_ID',
    'Bossu_ID',
    'Buchenwald_satellite_camp_ID',
    'Canonization_status',
    'Capacity',
    'Capital',
    'Capital_burden',
    'Capital_of',
    'Capital_return_of_the_property',
    'Career_statement',
    'Catalogus_Professorum_Halensis_ID',
    'Catholic_Hierarchy_ID',
    'Catholic_religious_name_of',
    'Cause_of_end',
    'Cause_of_loss',
    'CDLI_ID',
    'CDLI_ID2',
    'CERL_Thesaurus_ID',
    'Choice_of_title_in_Prozent',
    'Chronology',
    'CIDOC_CRM_class',
    'CIDOC_CRM_property',
    'Circumcision_Date_religious',
    'Circumstances_of_death',
    'Citizen_of',
    'City_Wiki_Dresden_ID',
    'Claimbase_ID',
    'classification_of_the_data_provider',
    'Collation',
    'Collected_by',
    'Collegiate_church',
    'Colour',
    'Columns',
    'Commentator',
    'Competent_Jurisdiction',
    'Complete_Bible_Genealogy_ID',
    'Complex_Evaluation',
    'Composer',
    'Composite_ID',
    'Compulsory_obligation_towards',
    'Conference_participations',
    'Confirmed_by',
    'Conflict_parties',
    'Constituted_by',
    'constraint_scope',
    'Contains_documents_of',
    'Contemporary_witness_document',
    'Continuation_of',
    'Continued_by',
    'Contributor',
    'Contributor_to',
    'Copy_of',
    'Copyright_holder',
    'Correlation',
    'Cosignatory_in',
    'Country_of_citizenship',
    'Cousin',
    'Creator',
    'Credit_receiver_of',
    'CTHS_ID_person',
    'CTHS_ID_society',
    'Curriculum_Vitae',
    'Dansk_Biografisk_Leksikon_ID',
    'Data_BnF_ID',
    'Data_set_wanting_a_statement_on',
    'Data_size',
    'Dataset',
    'Dataset_complaint',
    'Dataset_editing',
    'Dataset_status',
    'Datatype',
    'Date_after',
    'Date_as_stated',
    'Date_before',
    'Date_of_baptism',
    'Date_of_birth',
    'Date_of_burial',
    'Date_of_confirmation',
    'Date_of_creation',
    'Date_of_death',
    'Date_of_first_publication',
    'Date_of_last_will',
    'Date_of_premiere',
    'Date_of_publication',
    'Date_of_receipt',
    'Date_of_retirement',
    'Dedicatee',
    'Degree_system',
    'Degrees_worked',
    'Den_Store_Danske_ID',
    'Departure',
    'Design_planning',
    'Destimation_Arrival_point',
    'Deutsche_Biographie_GND_ID',
    'Deutsche_Fotothek_object_ID',
    'Deutsche_Inschriften_Online_ID',
    'Deutsches_Literaturarchiv_Marbach_ID',
    'Deutsches_Rechtswörterbuch',
    'Dewey_Decimal_Classification',
    'DFG_subject_classification',
    'Diameter',
    'Diccionari_de_la_Literatura_Catalana_ID',
    'Dictionary_of_Swedish_National_Biography_ID',
    'Digest',
    'Discovered_invented_developed_by',
    'Distance_between_addresses',
    'DNB_Info_ID',
    'Docker_Hub_repository',
    'Documented_object',
    'DOI',
    'Download_link',
    'Duration',
    'Duration_of_the_prison_sentence',
    'Ecclesiastical_province',
    'Economic_sector_of_the_career_statement',
    'Editorial_responsibility',
    'Educating_institution',
    'Education_level_academic_degree',
    'Edvard_Munchs_correspondance_person_ID',
    'EHAK_ID',
    'EHRI_ghetto_ID',
    'Election_results_by_candidate',
    'Eligible_voters',
    'Email_contact_page',
    'Employers_status',
    'End_date',
    'End_of_events_reported',
    'End_text_span',
    'Enzyklopädie_der_Russlanddeutschen_ID',
    'epidat_Database_ID',
    'Equivalent_in_grams_of_copper',
    'Equivalent_in_grams_of_gold',
    'Equivalent_in_grams_of_silver',
    'Equivalent_multilingual_item',
    'Espacenet_ID_for_patents',
    'Ethnic_background',
    'Europeana_Entity',
    'Events_attended',
    'Events_in_the_sequence',
    'Excipit',
    'Exclusion_criterion_incompatible_with_Membership_in',
    'Executor',
    'Exemplary_FactGrid_item',
    'Exlibris_of',
    'Extra_stemmatic_relationship',
    'Extract',
    'Extramarital_relationship_to_procure_a_child',
    'Eye_colour',
    'Facial_hair',
    'FactGrid_keyword',
    'FactGrid_List',
    'FactGrid_locality_type',
    'FactGrid_map_House_numbers',
    'FactGrid_properties_in_which_this_item_can_serve_as_an_answer',
    'FactGrid_property',
    'FactGrid_property_complaint',
    'FactGrid_user_page',
    'FactGrid_visualisation',
    'family_database_Juden_im_Deutschen_Reich_ID',
    'Family_various',
    'Fathers_status',
    'Fellow_student',
    'Feudal_obligation',
    'Field_of_engagement_expertise',
    'Field_of_knowledge',
    'Field_of_offices_in_the_Roman_Catholic_Church',
    'Field_of_research',
    'Finding_spot',
    'Fineness_1000',
    'First_documented_in',
    'Folios',
    'Font_size',
    'Footnote',
    'Format',
    'format_as_a_regular_expression',
    'Formed_a_set_with',
    'Forum_München_ID',
    'Francke_Foundations_Bio_ID',
    'Frankfurter_Personenlexikon',
    'Frauen_in_Bewegung_1848_1938_ID',
    'Friends_with',
    'Fruitbearing_Society_Member_ID',
    'Funeral_speech_by',
    'fuzzy_sl_ID',
    'Genealogycom_ID',
    'Genicom_profile_ID',
    'GeoNames_ID',
    'German_municipality_key',
    'Germania_Sacra_database_of_persons_ID',
    'Getty_Thesaurus_of_Geographic_Names_ID',
    'GitHub_username',
    'Glottolog_ID',
    'GND_input_field',
    'GND_network_graph',
    'Godfather_of_the_confirmand',
    'Gold_content_g',
    'Google_Knowledge_Graph_ID',
    'GOV_ID',
    'Grave',
    'Grave_Row',
    'GS_vocabulary_term',
    'Guardian',
    'Hair_colour',
    'HAIT_ID',
    'Handedness',
    'Handwritten_by',
    'Has_subclasses',
    'HDS_ID',
    'Heiress',
    'Hex_color',
    'Historic_county',
    'Historical_continuum',
    'Historical_description',
    'Homosaurus_ID_version_3',
    'Honorific_prefix',
    'Hosted',
    'House_numbering_system',
    'HOV_ID',
    'Iconography',
    'Identification_by',
    'Ideological_political_positioning',
    'IdRef_ID',
    'ie',
    'Image_content',
    'Image_number',
    'Image_source',
    'Immediate_superiors',
    'Implemented_by',
    'In_consequence_of',
    'In_his_her_personal_service',
    'In_leading_position',
    'In_words',
    'Includes',
    'Income',
    'Indication_the_object_existed',
    'INE_ID_Portugal',
    'INE_ID_Spain',
    'Infrastructure',
    'Inpatient_treatment_in',
    'Input_form',
    'INSEE_municipality_code',
    'Instance_of',
    'Institution_addressed',
    'Interest_claim_per_annum',
    'Internet_Archive_ID',
    'Internetportal_Westfälische_Geschichte_ID_Persons_entry',
    'Intervened_on_behalf_of',
    'Inventory_position',
    'Inverse_label_item',
    'Inverse_property',
    'ISBN_10',
    'ISBN_13',
    'ISO_3166_1_alpha_2_code',
    'ISO_3166_1_alpha_3_code',
    'ISO_3166_1_numeric_code',
    'ISO_3166_2',
    'ISO_3166_3',
    'ISO_639_2',
    'ISO_639_5',
    'ISSN',
    'Issue',
    'ISTC_ID',
    'Item_count_to',
    'Joint_partners',
    'Julian_calendar_stabiliser',
    'K10plus_PPN_ID',
    'Kalliope_ID',
    'KATOTTH_ID',
    'Key_data',
    'KGI4NFDI_ID',
    'Kiel_Scholars_Directory_ID',
    'Klosterdatenbank_ID',
    'KOATUU_ID',
    'Language',
    'Language_skills',
    'Last_holding_archive_of_the_lost_object',
    'Last_modified',
    'Last_professional_status',
    'Leaseholder',
    'Leaser',
    'Legal_form',
    'Legislative_term',
    'Length_distance',
    'Level_of_qualification',
    'License',
    'Licensed_by',
    'Liegelord',
    'Liegeman',
    'Likelihood_percent',
    'Line',
    'LinkedIn_personal_profile_ID',
    'Listed_in',
    'Literal_statement',
    'Literal_translation',
    'Live_stock',
    'Living_people_protection_class',
    'Lizenznummer_of_books_printed_in_the_GDR',
    'Local_units_of_measurement',
    'Localisation',
    'Location_in_the_property',
    'Lodge_Matriculation_number',
    'Maintained_by',
    'Mainzer_Ingrossaturbücher_ID',
    'Maitron_ID',
    'Maps_and_plans',
    'Married_to',
    'Mass',
    'Matching',
    'Material_composition',
    'Matrikelportal_Rostock_since_1419_ID',
    'Measures_taken',
    'Media_type',
    'Medical_cause_of_death',
    'Medical_condition',
    'Medical_treatment',
    'Medically_tended_by',
    'Meeting_point_of',
    'Memorial_Archives_ID',
    'Mode_of_presentation',
    'Musical_notation',
    'Named_after',
    'Naming',
    'Naming_of_the_titles_central_protagonist',
    'Naming_the_plural',
    'Naming_the_singular',
    'NDBA_ID',
    'Negative_search_result',
    'Next_higher_rank_or_degree',
    'Next_version',
    'NNDB_People_ID',
    'Normalization_variant',
    'Not_noted_in',
    'Not_to_be_confused_with',
    'Note',
    'Number',
    'Number_making_a_unit',
    'Number_of_abstentions',
    'Number_of_blank_votes',
    'Number_of_children',
    'Number_of_copies_extant',
    'Number_of_copies_printed',
    'Number_of_female_children',
    'Number_of_integrated_items',
    'Number_of_male_children',
    'Number_of_objects_within_a_collection',
    'Number_of_participants_members',
    'Number_of_sets_ordered',
    'Number_of_spoilt_votes',
    'NUTS_code',
    'OARE_ID',
    'OATP_ID',
    'Object_of_payment',
    'Object_of_procedure',
    'Object_paid',
    'Objected_by',
    'Objects_of_interest',
    'Objects_of_knowledge',
    'OCLC_ID',
    'Of_importance_to',
    'Official_website',
    'Old_inventory_position',
    'On_the_side_of',
    'Online_image',
    'Online_presentation',
    'Online_primary_documents',
    'Online_translation',
    'OpenHistoricalMap_ID',
    'Opponent_of_the_disputation',
    'Opposite_of',
    'Options',
    'ORACC_id_word',
    'ORCID_ID',
    'Ordained_consecrated_by',
    'Organisation_open_from_here',
    'Organisation_signing_responsible',
    'Organisational_aspects',
    'Original_language',
    'Owned_by',
    'Owner_of',
    'Page_layout',
    'Pages',
    'Part_of',
    'Part_of_the_collection',
    'Patients',
    'Payment_interval',
    'Payment_recipient',
    'Payment_sender',
    'Payment_transactor',
    'Peerage_person_ID',
    'Percentage',
    'Person_for_whom_the_document_was_written',
    'Person_signing_responsible',
    'Personal_connections',
    'Personal_inspection_by',
    'Personal_servant_of',
    'Persons_mentioned',
    'Persons_of_Indian_Studies_ID',
    'PhiloBiblon_ID',
    'Photo_Cardboard_Manufacturer',
    'Photographic_Studio',
    'Pilgrimage_to',
    'Place_of_address',
    'Place_of_baptism',
    'Place_of_birth',
    'Place_of_death',
    'Place_of_detention',
    'Place_of_education',
    'Place_of_publication',
    'Pleiades_ID',
    'Plus',
    'PMB_person_ID',
    'Position_held',
    'Position_in_sequence',
    'Possibly_identical_to',
    'Post_included',
    'Precision_of_begin_date',
    'Precision_of_begin_date_string',
    'Precision_of_date',
    'Precision_of_end_date',
    'Precision_of_end_date_string',
    'Predominant_gender_usage',
    'Preface_by',
    'Preferred_designation',
    'Premiere',
    'Preservation',
    'Presiding_the_disputation',
    'Previous_version',
    'Primary_source',
    'Printed_by',
    'Prisoner_of_war_of',
    'Process_File_number',
    'Produced_by_brand',
    'Produces_product_range',
    'Professional_address',
    'Programming_language',
    'Projects',
    'Pronunciation_IPA',
    'Property_constraint',
    'Proposed_to_become_a_member_of',
    'Pseudonym_of',
    'Public_awards_and_titles',
    'Published_in',
    'Publisher',
    'Publisher',
    'Publisher_as_misleadingly_stated',
    'Purpose',
    'Qualifier',
    'RAG_ID',
    'RAM_size',
    'Rank',
    'Rank_service_number',
    're3data_D',
    'Reason_for_deprecated_rank',
    'Reason_for_preferred_rank',
    'Receives_area_from',
    'Recipient',
    'Recording_online_information',
    'Regional_localisation',
    'Registered_accepted_by',
    'Registrar',
    'Regular_meeting_point',
    'Related_object',
    'Relation_constraint',
    'Religious_background',
    'Religious_order',
    'Relocated_subject',
    'Repertorium_Germanicum_ID',
    'Repertorium_Poenitentiariae_Germanicum_ID',
    'Reported_event',
    'Request_FactGrid',
    'Request_name',
    'Research_projects_that_contributed_to_this_data_set',
    'Research_stay_in',
    'ResearchGate_profile_ID',
    'Respondent_of_the_disputation',
    'Revised_by',
    'RI_ID',
    'RISM_ID',
    'Romanised_transcription',
    'Room_number',
    'Rosicrucian_code_name',
    'Rosicrucian_code_name_of',
    'Said_to_be_the_same_as',
    'School_adherence',
    'Script_style',
    'Seal',
    'Seal_ID',
    'Secondary_literature_research',
    'Secondary_literature_research_literal',
    'See_also_property',
    'Segmentation',
    'Sejm_Wielkipl_profile_ID',
    'Semantic_Kompakkt_ID',
    'Series',
    'Set_by',
    'Sexual_orientation',
    'short_digest',
    'Siblings',
    'Signed_by',
    'Silver_content',
    'Skin_colour',
    'Source_literal',
    'Spanish_Biographical_Dictionary_ID',
    'Specific_statement',
    'Split_off',
    'Split_off_from',
    'Sponsor_supporter',
    'SS_KL_Auschwitz_Garrison_ID',
    'SS_membership_number',
    'SS_Resettlement_ID',
    'Start_time_of_reported_events',
    'Statement_denied_by',
    'Statement_refers_to',
    'Statement_refers_to',
    'Stature',
    'Status_of_possesion',
    'Status_of_the_deceased_husband',
    'Stored_in',
    'Strict_Observance_order_name',
    'Structural_hierarchies_implemented',
    'Student',
    'Student_of',
    'Subclass_of',
    'Subject_evicted',
    'Subject_matter_that_raised_objections',
    'Subject_of_negotiation',
    'Subject_paid',
    'Subject_topic_heading',
    'Subjected',
    'Subjected_to',
    'Subsidiary',
    'Subunit_of',
    'Subunits',
    'Supplied_by',
    'Sustainability',
    'Swedish_portrait_archive_ID',
    'Swiss_municipality_code',
    'Symbolises',
    'System_component_of',
    'Sächsische_Biografie_ID',
    'Target_language',
    'Taxable_assets',
    'Taxon_range',
    'Taxonomic_name',
    'Team',
    'Term_attributed_by',
    'Text_justification_legal_basis_constitution',
    'Time_of_day',
    'Title',
    'Title_page_transcript',
    'to',
    'Total_valid_votes',
    'Transacted_object',
    'Translator',
    'Transliteration',
    'Tribe',
    'Truth_context',
    'Type_of_treatment',
    'Type_of_work',
    'Typeface',
    'Typology',
    'Underlying_problem',
    'URL',
    'URN_formatter',
    'USTC_editions_ID',
    'Value_price',
    'Vasserot_ID_streets_of_Paris',
    'VD16_ID',
    'VD17_ID',
    'VD18_ID',
    'Verdict',
    'Vergue_ID',
    'VIAF_ID',
    'Visual_work_component',
    'Visual_work_components_by',
    'Voice_type',
    'Volume_as_a_quantity',
    'Watermark',
    'Well_Known_Text_Geometry',
    'What_supports_this_identification',
    'WIAG_ID',
    'WIAG_Office_in_Sequence_ID',
    'Wider_field_of_genres',
    'Wikimedia_language_code',
    'With_manuscript_notes_by',
    'Without',
    'Work_to_be_subscribed',
    'Works_published_or_unpublished',
    'WorldCat_Identities_ID',
    'Writing_surface',
    'X_post_ID',
    'Yad_Vashem_name_genealogy_ID',
    'Zeitschriften_database_ID',
    'ZOBODAT_People_ID',
    'ZOBODAT_Publication_Article_ID',
    'ZOBODAT_Publication_Series_ID',
)

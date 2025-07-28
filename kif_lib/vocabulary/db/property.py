# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...model import IRI, Item, Quantity, String, Text, Time
from .prelude import op

# autopep8: off
# flake8: noqa

abbeychurchBlessing = op('abbeychurchBlessing', range=String, label='abbey church blessing')
abbeychurchBlessingCharge = op('abbeychurchBlessingCharge', range=String, label='abbey church blessing charge')
abbreviation = op('abbreviation', range=String, label='abbreviation')
ableToGrind = op('ableToGrind', range=String, label='able to grind')
absoluteMagnitude = op('absoluteMagnitude', range=Quantity, label='absolute magnitude')
abstentions = op('abstentions', range=Quantity, label='abstentions')
abstract = op('abstract', range=Text, label='has abstract')
academicAdvisor = op('academicAdvisor', range=Item, label='academic advisor')
academyAward = op('academyAward', range=Item, label='Academy Award')
acceleration = op('acceleration', range=Quantity, label='acceleration (s)')
access = op('access', range=String, label='access')
accessDate = op('accessDate', range=Time, label='access date')
acquirementDate = op('acquirementDate', range=Time, label='date of acquirement')
actingHeadteacher = op('actingHeadteacher', range=Item, label='acting headteacher')
activeCases = op('activeCases', range=Quantity, label='Active Cases')
activeYears = op('activeYears', range=String, label='active years')
activeYearsEndDate = op('activeYearsEndDate', range=Time, label='active years end date')
activeYearsEndDateMgr = op('activeYearsEndDateMgr', range=String, label='active years end date manager')
activeYearsEndYear = op('activeYearsEndYear', range=Time, label='active years end year')
activeYearsEndYearMgr = op('activeYearsEndYearMgr', range=Time, label='active years end year manager')
activeYearsStartDate = op('activeYearsStartDate', range=Time, label='active years start date')
activeYearsStartDateMgr = op('activeYearsStartDateMgr', range=Time, label='active years start date manager')
activeYearsStartYear = op('activeYearsStartYear', range=Time, label='active years start year')
activeYearsStartYearMgr = op('activeYearsStartYearMgr', range=Time, label='active years start year manager')
address = op('address', range=Text, label='address')
adjacentSettlement = op('adjacentSettlement', range=Item, label='adjacent settlement of a switzerland settlement')
administrativeCenter = op('administrativeCenter', range=Item, label='administrative center')
administrativeCollectivity = op('administrativeCollectivity', range=Item, label='administrative collectivity')
administrativeDistrict = op('administrativeDistrict', range=Item, label='administrative district')
administrativeHeadCity = op('administrativeHeadCity', range=Item, label='head city')
administrativeStatus = op('administrativeStatus', range=String, label='administrative status')
administrator = op('administrator', range=Item, label='administrator')
afdbId = op('afdbId', range=String, label='afdb id')
affair = op('affair', range=String, label='affair')
affiliate = op('affiliate', range=String, label='affiliate')
affiliation = op('affiliation', range=Item, label='affiliation')
afiAward = op('afiAward', range=Item, label='AFI Award')
age = op('age', range=Quantity, label='age')
agencyStationCode = op('agencyStationCode', range=String, label='agency station code')
ageRange = op('ageRange', range=Quantity, label='age range')
agglomeration = op('agglomeration', range=Item, label='agglomeration')
agglomerationArea = op('agglomerationArea', range=Item, label='agglomeration area')
agglomerationDemographics = op('agglomerationDemographics', range=Item, label='agglomeration demographics')
agglomerationPopulation = op('agglomerationPopulation', range=Item, label='agglomeration population')
agglomerationPopulationTotal = op('agglomerationPopulationTotal', range=Quantity, label='agglomeration population total')
agglomerationPopulationYear = op('agglomerationPopulationYear', range=String, label='agglomerationPopulationYear')
aggregation = op('aggregation', range=String, label='Aggregation')
aircraftAttack = op('aircraftAttack', range=Item, label='aircraft attack')
aircraftBomber = op('aircraftBomber', range=Item, label='aircraft bomber')
aircraftElectronic = op('aircraftElectronic', range=Item, label='aircraft electronic')
aircraftFighter = op('aircraftFighter', range=Item, label='aircraft fighter')
aircraftHelicopter = op('aircraftHelicopter', range=Item, label='aircraft helicopter')
aircraftHelicopterAttack = op('aircraftHelicopterAttack', range=Item, label='aircraft helicopter attack')
aircraftHelicopterCargo = op('aircraftHelicopterCargo', range=Item, label='aircraft helicopter cargo')
aircraftHelicopterMultirole = op('aircraftHelicopterMultirole', range=Item, label='aircraft helicopter multirole')
aircraftHelicopterObservation = op('aircraftHelicopterObservation', range=Item, label='aircraft helicopter observation')
aircraftHelicopterTransport = op('aircraftHelicopterTransport', range=Item, label='aircraft helicopter transport')
aircraftHelicopterUtility = op('aircraftHelicopterUtility', range=Item, label='aircraft helicopter utility')
aircraftInterceptor = op('aircraftInterceptor', range=Item, label='aircraft interceptor')
aircraftPatrol = op('aircraftPatrol', range=Item, label='aircraft patrol')
aircraftRecon = op('aircraftRecon', range=Item, label='aircraft recon')
aircraftTrainer = op('aircraftTrainer', range=Item, label='aircraft trainer')
aircraftTransport = op('aircraftTransport', range=Item, label='aircraft transport')
aircraftType = op('aircraftType', range=String, label='aircraft type')
aircraftUser = op('aircraftUser', range=Item, label='aircraft user')
airDate = op('airDate', range=Time, label='airdate')
airportUsing = op('airportUsing', range=String, label='Different usage of an airport')
aitaCode = op('aitaCode', range=String, label='aita code')
albedo = op('albedo', range=Quantity, label='albedo')
album = op('album', range=Item, label='album')
albumRuntime = op('albumRuntime', range=Quantity, label='album duration (s)')
alias = op('alias', range=Text, label='alias')
allcinemaId = op('allcinemaId', range=String, label='allcinema id')
allegiance = op('allegiance', range=String, label='allegiance')
almaMater = op('almaMater', range=Item, label='alma mater')
alongside = op('alongside', range=Item, label='alongside')
alpsGroup = op('alpsGroup', range=Item, label='Alps group')
alpsMainPart = op('alpsMainPart', range=Item, label='Alps main part')
alpsMajorSector = op('alpsMajorSector', range=Item, label='Alps major sector')
alpsSection = op('alpsSection', range=Item, label='Alps section')
alpsSoiusaCode = op('alpsSoiusaCode', range=String, label='Alps SOIUSA code')
alpsSubgroup = op('alpsSubgroup', range=Item, label='Alps subgroup')
alpsSubsection = op('alpsSubsection', range=Item, label='Alps subsection')
alpsSupergroup = op('alpsSupergroup', range=Item, label='Alps supergroup')
alternativeName = op('alternativeName', range=Text, label='alternative name')
alternativeText = op('alternativeText', range=String, label='alternative text')
alternativeTitle = op('alternativeTitle', range=Text, label='alternative title')
altitude = op('altitude', range=Item, label='altitude')
alumni = op('alumni', range=Item, label='alumni')
amateurDefeat = op('amateurDefeat', range=Quantity, label='amateur defeat')
amateurFight = op('amateurFight', range=Quantity, label='amateur fight')
amateurKo = op('amateurKo', range=Quantity, label='amateur ko')
amateurNoContest = op('amateurNoContest', range=Quantity, label='amateur no contest')
amateurTeam = op('amateurTeam', range=Item, label='amateur team')
amateurTie = op('amateurTie', range=Quantity, label='amateur tie')
amateurTitle = op('amateurTitle', range=String, label='amateur title')
amateurVictory = op('amateurVictory', range=Quantity, label='amateur victory')
amateurYear = op('amateurYear', range=String, label='amateur year')
americanComedyAward = op('americanComedyAward', range=Item, label='American Comedy Award')
amgid = op('amgid', range=String, label='amgId')
amsterdamCode = op('amsterdamCode', range=String, label='Amsterdam Code')
analogChannel = op('analogChannel', range=String, label='analog channel')
animal = op('animal', range=Item, label='animal')
animator = op('animator', range=Item, label='animator')
anniversary = op('anniversary', range=Time, label='anniversary')
announcedFrom = op('announcedFrom', range=Item, label='announcedFrom')
annualTemperature = op('annualTemperature', range=Quantity, label='annual temperature (K)')
anthem = op('anthem', range=Item, label='anthem')
aoCloassification = op('aoCloassification', range=String, label='AO')
apcPresident = op('apcPresident', range=Item, label='apc president')
apoapsis = op('apoapsis', range=Quantity, label='apoapsis (μ)')
apofocus = op('apofocus', range=String, label='apofocus')
apparentMagnitude = op('apparentMagnitude', range=Quantity, label='apparent magnitude')
appearance = op('appearance', range=String, label='appearance')
appearancesInLeague = op('appearancesInLeague', range=Quantity, label='appearances in league')
appearancesInNationalTeam = op('appearancesInNationalTeam', range=Quantity, label='appearances in national team')
appointer = op('appointer', range=Item, label='appointer')
apprehended = op('apprehended', range=Time, label='apprehended')
approvedByLowerParliament = op('approvedByLowerParliament', range=Time, label='date of approval by lower parliament')
approvedByUpperParliament = op('approvedByUpperParliament', range=Time, label='date of approval by upper parliament')
approximateCalories = op('approximateCalories', range=Quantity, label='approximate calories (J)')
apskritis = op('apskritis', range=String, label='apskritis')
architect = op('architect', range=Item, label='architect')
architectualBureau = op('architectualBureau', range=Item, label='architectual bureau')
architecturalMovement = op('architecturalMovement', range=String, label='architectural movement')
area = op('area', range=Quantity, label='area (m2)')
areaCode = op('areaCode', range=String, label='area code')
areaDate = op('areaDate', range=Time, label='area date')
areaLand = op('areaLand', range=Quantity, label='area land (m2)')
areaMetro = op('areaMetro', range=Quantity, label='area metro (m2)')
areaOfCatchment = op('areaOfCatchment', range=Quantity, label='area of catchment (m2)')
areaOfCatchmentQuote = op('areaOfCatchmentQuote', range=String, label='area of catchment quote')
areaOfSearch = op('areaOfSearch', range=Item, label='area of search')
areaQuote = op('areaQuote', range=String, label='area quote')
areaRank = op('areaRank', range=String, label='area rank')
areaRural = op('areaRural', range=Quantity, label='area rural (m2)')
areaTotal = op('areaTotal', range=Quantity, label='area total (m2)')
areaTotalRanking = op('areaTotalRanking', range=Quantity, label='total area ranking')
areaUrban = op('areaUrban', range=Quantity, label='area urban (m2)')
areaWater = op('areaWater', range=Quantity, label='area water (m2)')
argueDate = op('argueDate', range=Time, label='argue date')
arielAward = op('arielAward', range=Item, label='Ariel Award')
arm = op('arm', range=String, label='arm')
army = op('army', range=String, label='army')
arrestDate = op('arrestDate', range=Time, label='arrest date')
arrondissement = op('arrondissement', range=Item, label='arrondissement')
artery = op('artery', range=Item, label='artery')
artificialSnowArea = op('artificialSnowArea', range=Quantity, label='artificial snow area')
artist = op('artist', range=Item, label='performer')
artistFunction = op('artistFunction', range=String, label='artist function')
artisticFunction = op('artisticFunction', range=String, label='artistic function')
artPatron = op('artPatron', range=Item, label='patron (art)')
ascent = op('ascent', range=String, label='ascent')
asiaChampionship = op('asiaChampionship', range=String, label='asia championship')
aSide = op('aSide', range=String, label='a side')
assets = op('assets', range=Quantity, label='assets ($)')
assetUnderManagement = op('assetUnderManagement', range=Quantity, label='asset under management ($)')
associate = op('associate', range=Item, label='associate')
associatedAct = op('associatedAct', range=Item, label='associated act')
associatedBand = op('associatedBand', range=Item, label='associated band')
associatedMusicalArtist = op('associatedMusicalArtist', range=Item, label='associated musical artist')
associatedRocket = op('associatedRocket', range=Item, label='associated rocket')
associateEditor = op('associateEditor', range=Item, label='associate editor')
associateStar = op('associateStar', range=Item, label='associateStar')
associationOfLocalGovernment = op('associationOfLocalGovernment', range=Item, label='association of local government')
astrazenca = op('astrazenca', range=String, label='Astrazenca')
astrazencaCumul = op('astrazencaCumul', range=Quantity, label='AstrazencaCumulativeDoses')
asWikiText = op('asWikiText', range=String, label='Contains a WikiText representation of this thing')
atcCode = op('atcCode', range=String, label='ATC code')
atcPrefix = op('atcPrefix', range=String, label='ATC prefix')
atcSuffix = op('atcSuffix', range=String, label='ATC suffix')
athleticsDiscipline = op('athleticsDiscipline', range=Item, label='athletics discipline')
atomicNumber = op('atomicNumber', range=Quantity, label='atomic number')
atPage = op('atPage', range=String, label='page number')
atRowNumber = op('atRowNumber', range=String, label='row number')
attorneyGeneral = op('attorneyGeneral', range=Item, label='attorney general')
aunt = op('aunt', range=Item, label='aunt')
australiaOpenDouble = op('australiaOpenDouble', range=String, label='australia open double')
australiaOpenMixed = op('australiaOpenMixed', range=String, label='australia open mixed')
australiaOpenSingle = op('australiaOpenSingle', range=String, label='australia open single')
author = op('author', range=Item, label='author')
authorityMandate = op('authorityMandate', range=String, label='authority mandate')
authorityTitle = op('authorityTitle', range=String, label='authority title of a romanian settlement')
automobileModel = op('automobileModel', range=String, label='automobile model')
automobilePlatform = op('automobilePlatform', range=Item, label='automobile platform')
average = op('average', range=Quantity, label='average')
averageAnnualGeneration = op('averageAnnualGeneration', range=Quantity, label='average annual gross power generation (J)')
averageClassSize = op('averageClassSize', range=Quantity, label='average class size')
averageDepth = op('averageDepth', range=Quantity, label='average depth (μ)')
averageDepthQuote = op('averageDepthQuote', range=String, label='average depth quote')
averageSpeed = op('averageSpeed', range=Quantity, label='average speed (kmh)')
avgRevSizePerMonth = op('avgRevSizePerMonth', range=IRI, label='Average size of the revision per month')
avgRevSizePerYear = op('avgRevSizePerYear', range=IRI, label='Average size of the revision per year')
avifaunaPopulation = op('avifaunaPopulation', range=String, label='avifauna population')
award = op('award', range=Item, label='award')
awardName = op('awardName', range=String, label='awardName')
awayColourHexCode = op('awayColourHexCode', range=String, label='colour hex code of away jersey or its parts')
background = op('background', range=String, label='background')
backhand = op('backhand', range=String, label='backhand')
badGuy = op('badGuy', range=String, label='bad guy')
baftaAward = op('baftaAward', range=Item, label='BAFTA Award')
band = op('band', range=String, label='band')
bandMember = op('bandMember', range=Item, label='band member')
barangays = op('barangays', range=String, label='barangays')
barPassRate = op('barPassRate', range=Quantity, label='bar pass rate')
basedOn = op('basedOn', range=Item, label='based on')
battery = op('battery', range=Item, label='battery')
battingSide = op('battingSide', range=String, label='batting side')
battle = op('battle', range=Item, label='battle')
battleHonours = op('battleHonours', range=String, label='battle honours')
bbr = op('bbr', range=String, label='BBR')
beatifiedBy = op('beatifiedBy', range=Item, label='beatified by')
beatifiedDate = op('beatifiedDate', range=Time, label='beatified date')
beatifiedPlace = op('beatifiedPlace', range=Item, label='beatified place')
bedCount = op('bedCount', range=Quantity, label='bed count')
believers = op('believers', range=String, label='Believers')
beltwayCity = op('beltwayCity', range=Item, label='beltway city')
bestFinish = op('bestFinish', range=String, label='best ranking finish')
bestLap = op('bestLap', range=String, label='best lap')
bestRankDouble = op('bestRankDouble', range=String, label='best rank double')
bestRankSingle = op('bestRankSingle', range=String, label='best rank single')
bestWsopRank = op('bestWsopRank', range=Quantity, label='best wsop rank')
bestYearWsop = op('bestYearWsop', range=Time, label='best year wsop')
bgafdId = op('bgafdId', range=String, label='bgafd id')
bibsysId = op('bibsysId', range=String, label='BIBSYS Id')
bicycleInformation = op('bicycleInformation', range=String, label='bicycle information')
biggestCity = op('biggestCity', range=Item, label='biggest city')
bigPoolRecord = op('bigPoolRecord', range=String, label='big pool record')
billed = op('billed', range=Item, label='billed')
bioavailability = op('bioavailability', range=Quantity, label='Bioavailability')
bioclimate = op('bioclimate', range=String, label='bioclimate')
bird = op('bird', range=Item, label='bird')
birthDate = op('birthDate', range=Time, label='birth date')
birthName = op('birthName', range=Text, label='birth name')
birthPlace = op('birthPlace', range=Item, label='birth place')
birthYear = op('birthYear', range=Time, label='birth year')
blackLongDistancePisteNumber = op('blackLongDistancePisteNumber', range=Quantity, label='long distance piste number')
blackSkiPisteNumber = op('blackSkiPisteNumber', range=Quantity, label='black ski piste number')
blazon = op('blazon', range=String, label='blazon')
blazonCaption = op('blazonCaption', range=String, label='Blazon caption')
blazonLink = op('blazonLink', range=String, label='blazon link')
blazonRatio = op('blazonRatio', range=Quantity, label='blazon ratio')
block = op('block', range=String, label='block')
bloodGroup = op('bloodGroup', range=String, label='blood group')
blueLongDistancePisteNumber = op('blueLongDistancePisteNumber', range=Quantity, label='blue long distance piste number')
blueSkiPisteNumber = op('blueSkiPisteNumber', range=Quantity, label='blue ski piste number')
bnfId = op('bnfId', range=String, label='BNF Id')
bodyDiscovered = op('bodyDiscovered', range=Item, label='body discovered')
boilingPoint = op('boilingPoint', range=Quantity, label='boiling point (K)')
book = op('book', range=String, label='name')
booster = op('booster', range=Item, label='booster')
border = op('border', range=Item, label='border')
borough = op('borough', range=Item, label='borough')
bourgmestre = op('bourgmestre', range=Item, label='bourgmestre')
bowlingSide = op('bowlingSide', range=String, label='bowling side')
bowlRecord = op('bowlRecord', range=String, label='bowl record')
boxerStyle = op('boxerStyle', range=Item, label='boxing style')
bpnId = op('bpnId', range=String, label='BPN Id')
brainInfoNumber = op('brainInfoNumber', range=String, label='brain info number')
brainInfoType = op('brainInfoType', range=String, label='brain info type')
branchFrom = op('branchFrom', range=Item, label='branch from')
branchTo = op('branchTo', range=Item, label='branch to')
brand = op('brand', range=Item, label='brand')
breeder = op('breeder', range=Item, label='breeder')
bridgeCarries = op('bridgeCarries', range=String, label='bridge carries')
brinCode = op('brinCode', range=String, label='BRIN code')
britishComedyAwards = op('britishComedyAwards', range=Item, label='British Comedy Awards')
britishOpen = op('britishOpen', range=String, label='britishOpen')
broadcastArea = op('broadcastArea', range=Item, label='broadcast area')
broadcastNetwork = op('broadcastNetwork', range=Item, label='broadcast network')
broadcastRepeater = op('broadcastRepeater', range=String, label='broadcast repeater')
broadcastStationClass = op('broadcastStationClass', range=String, label='broadcast station class')
broadcastTranslator = op('broadcastTranslator', range=String, label='broadcast translator')
bronzeMedalDouble = op('bronzeMedalDouble', range=String, label='bronze medal double')
bronzeMedalist = op('bronzeMedalist', range=Item, label='bronze medalist')
bronzeMedalMixed = op('bronzeMedalMixed', range=String, label='bronze medal mixed')
bronzeMedalSingle = op('bronzeMedalSingle', range=String, label='bronze medal single')
brother = op('brother', range=Item, label='brother')
bSide = op('bSide', range=String, label='b side')
budget = op('budget', range=Quantity, label='budget ($)')
budgetYear = op('budgetYear', range=String, label='budget year')
building = op('building', range=Item, label='building')
buildingEndDate = op('buildingEndDate', range=String, label='building end date')
buildingEndYear = op('buildingEndYear', range=Time, label='building end year')
buildingStartDate = op('buildingStartDate', range=String, label='building start date')
buildingStartYear = op('buildingStartYear', range=Time, label='building start year')
bustSize = op('bustSize', range=Quantity, label='bust size (μ)')
bustWaistHipSize = op('bustWaistHipSize', range=String, label='bust-waist-hip Size')
cableCar = op('cableCar', range=Quantity, label='cable car')
callSign = op('callSign', range=String, label='call sign')
callsignMeaning = op('callsignMeaning', range=String, label='call sign meaning')
campusSize = op('campusSize', range=Quantity, label='campus size (m2)')
campusType = op('campusType', range=Text, label='campus type')
canBaggageChecked = op('canBaggageChecked', range=Quantity, label='can baggage checked')
cannonNumber = op('cannonNumber', range=Quantity, label='cannon number')
canonizedBy = op('canonizedBy', range=Item, label='canonized by')
canonizedDate = op('canonizedDate', range=Time, label='canonized date')
canonizedPlace = op('canonizedPlace', range=Item, label='canonized place')
canton = op('canton', range=Item, label='canton')
capacity = op('capacity', range=Quantity, label='capacity')
capacityFactor = op('capacityFactor', range=Quantity, label='capacity factor')
capital = op('capital', range=Item, label='capital')
capitalCoordinates = op('capitalCoordinates', range=String, label='capital coordinates')
capitalCountry = op('capitalCountry', range=Item, label='capital country')
capitalDistrict = op('capitalDistrict', range=Item, label='capital district')
capitalElevation = op('capitalElevation', range=Quantity, label='capital elevation (μ)')
capitalMountain = op('capitalMountain', range=Item, label='capital mountain')
capitalPlace = op('capitalPlace', range=Item, label='capital place')
capitalRegion = op('capitalRegion', range=Item, label='capital region')
captureDate = op('captureDate', range=Time, label='capture date')
carbohydrate = op('carbohydrate', range=Quantity, label='carbohydrate (g)')
carcinogen = op('carcinogen', range=String, label='carcinogen')
careerPoints = op('careerPoints', range=Quantity, label='career points')
careerPrizeMoney = op('careerPrizeMoney', range=Quantity, label='career prize money ($)')
careerStation = op('careerStation', range=Item, label='career station')
cargoFuel = op('cargoFuel', range=Quantity, label='cargo fuel (g)')
cargoGas = op('cargoGas', range=Quantity, label='cargo gas (g)')
cargoWater = op('cargoWater', range=Quantity, label='cargo water (g)')
carNumber = op('carNumber', range=Quantity, label='car number')
case = op('case', range=String, label='case')
casNumber = op('casNumber', range=String, label='CAS number')
casSupplemental = op('casSupplemental', range=String, label='CAS supplemental')
casualties = op('casualties', range=Quantity, label='casualties')
catch = op('catch', range=String, label='catch')
caterer = op('caterer', range=Item, label='caterer')
catholicPercentage = op('catholicPercentage', range=String, label='catholic percentage')
causalties = op('causalties', range=String, label='causalties')
causeOfDeath = op('causeOfDeath', range=String, label='cause of death')
ccaState = op('ccaState', range=String, label='cca state')
ceeb = op('ceeb', range=String, label='ceeb')
ceiling = op('ceiling', range=Quantity, label='ceiling')
cemetery = op('cemetery', range=Item, label='cemetery')
censusYear = op('censusYear', range=Time, label='census year')
center = op('center', range=String, label='norwegian center')
centuryBreaks = op('centuryBreaks', range=Quantity, label='century breaks')
ceo = op('ceo', range=Item, label='chief executive officer')
ceremonialCounty = op('ceremonialCounty', range=Item, label='Ceremonial County')
certification = op('certification', range=String, label='certification')
certificationDate = op('certificationDate', range=Time, label='certification date')
cesarAward = op('cesarAward', range=Item, label='Cesar Award')
chain = op('chain', range=Item, label='chaîne')
chairman = op('chairman', range=Item, label='chairman')
chairmanTitle = op('chairmanTitle', range=Text, label='chairman title')
chairperson = op('chairperson', range=Item, label='chairperson')
champion = op('champion', range=Item, label='champion')
championInDouble = op('championInDouble', range=Item, label='champion in double')
championInDoubleFemale = op('championInDoubleFemale', range=Item, label='champion in double female')
championInDoubleMale = op('championInDoubleMale', range=Item, label='champion in double male')
championInMixedDouble = op('championInMixedDouble', range=Item, label='champion in mixed double')
championInSingle = op('championInSingle', range=Item, label='champion in single')
championInSingleFemale = op('championInSingleFemale', range=Item, label='champion in single female')
championInSingleMale = op('championInSingleMale', range=Item, label='champion in single male')
championships = op('championships', range=Quantity, label='championships')
chancellor = op('chancellor', range=Item, label='chancellor')
channel = op('channel', range=Item, label='channel')
chaplain = op('chaplain', range=Item, label='chaplain')
characterInPlay = op('characterInPlay', range=String, label='character in play')
chEBI = op('chEBI', range=String, label='ChEBI')
chef = op('chef', range=Item, label='chef')
chEMBL = op('chEMBL', range=String, label='ChEMBL')
chemicalFormula = op('chemicalFormula', range=String, label='chemical formula')
chemSpiderId = op('chemSpiderId', range=String, label='ChemSpider Id')
chief = op('chief', range=Item, label='chief')
chiefEditor = op('chiefEditor', range=Item, label='chief editor')
chiefPlace = op('chiefPlace', range=Item, label='chief place')
child = op('child', range=Item, label='child')
childOrganisation = op('childOrganisation', range=Item, label='child organisation')
choreographer = op('choreographer', range=Item, label='choreographer')
chorusCharacterInPlay = op('chorusCharacterInPlay', range=String, label='chorus character in play')
christeningDate = op('christeningDate', range=Time, label='date of christening')
chromosome = op('chromosome', range=String, label='chromosome')
cinematography = op('cinematography', range=Item, label='cinematography')
circle = op('circle', range=String, label='region')
circuitLength = op('circuitLength', range=Quantity, label='circuit length (μ)')
circuitName = op('circuitName', range=Text, label='circuit name')
circulation = op('circulation', range=Quantity, label='circulation')
circumcised = op('circumcised', range=String, label='circumcised')
cites = op('cites', range=String, label='cites')
city = op('city', range=Item, label='city')
cityLink = op('cityLink', range=String, label='city link')
cityRank = op('cityRank', range=Quantity, label='city rank')
citySince = op('citySince', range=String, label='city since')
cityType = op('cityType', range=String, label='city type')
classes = op('classes', range=Quantity, label='classes')
classification = op('classification', range=String, label='classification')
climbUpNumber = op('climbUpNumber', range=Quantity, label='clip up number')
closed = op('closed', range=Time, label='closed')
closeTo = op('closeTo', range=Item, label='is close to')
closingDate = op('closingDate', range=Time, label='closing date')
closingFilm = op('closingFilm', range=Item, label='closing film')
closingYear = op('closingYear', range=Time, label='closing year')
clothingSize = op('clothingSize', range=String, label='clothing size')
clothSize = op('clothSize', range=String, label='cloth size')
club = op('club', range=Item, label='club')
clubsRecordGoalscorer = op('clubsRecordGoalscorer', range=Item, label='clubs record goalscorer')
cmpEvaDuration = op('cmpEvaDuration', range=Quantity, label='CMP EVA duration (s)')
cmykCoordinateBlack = op('cmykCoordinateBlack', range=Quantity, label='black coordinate in the CMYK space')
cmykCoordinateCyanic = op('cmykCoordinateCyanic', range=Quantity, label='cyanic coordinate in the CMYK space')
cmykCoordinateMagenta = op('cmykCoordinateMagenta', range=Quantity, label='magenta coordinate in the CMYK space')
cmykCoordinateYellow = op('cmykCoordinateYellow', range=Quantity, label='yellow coordinate in the CMYK space')
co2Emission = op('co2Emission', range=Quantity, label='CO2 emission (g/km)')
coach = op('coach', range=Item, label='coach')
coachClub = op('coachClub', range=Item, label='coach club')
coachedTeam = op('coachedTeam', range=Item, label='coached team')
coachingRecord = op('coachingRecord', range=String, label='coaching record')
coachSeason = op('coachSeason', range=String, label='coach season')
coalition = op('coalition', range=String, label='coalition')
coastLength = op('coastLength', range=Quantity, label='length of a coast')
coastLine = op('coastLine', range=Quantity, label='coast line (μ)')
code = op('code', range=String, label='code')
codeBook = op('codeBook', range=String, label='code book')
codeDistrict = op('codeDistrict', range=String, label='City district code')
codeIndex = op('codeIndex', range=String, label='code on index')
codeListOfHonour = op('codeListOfHonour', range=String, label='code on List of Honour')
codeMemorial = op('codeMemorial', range=String, label='memorial ID number')
codeMunicipalMonument = op('codeMunicipalMonument', range=String, label='monument code (municipal)')
coden = op('coden', range=String, label='CODEN')
codeNationalMonument = op('codeNationalMonument', range=String, label='monument code (national)')
codeProvincialMonument = op('codeProvincialMonument', range=String, label='monument code (provinciall)')
codeSettlement = op('codeSettlement', range=String, label='settlement code')
codeStockExchange = op('codeStockExchange', range=String, label='code Stock Exchange')
coemperor = op('coemperor', range=Item, label='coemperor')
coExecutiveProducer = op('coExecutiveProducer', range=Item, label='co executive producer')
collaboration = op('collaboration', range=Item, label='collaboration')
colleague = op('colleague', range=Item, label='colleague')
collection = op('collection', range=String, label='collection')
college = op('college', range=Item, label='college')
collegeHof = op('collegeHof', range=String, label='college hof')
colonialName = op('colonialName', range=String, label='colonial name')
colorChart = op('colorChart', range=String, label='colorChart')
colour = op('colour', range=Item, label='colour')
colourHexCode = op('colourHexCode', range=String, label='colour hex code')
colourName = op('colourName', range=Text, label='colour name')
combatant = op('combatant', range=String, label='combatant')
comic = op('comic', range=Item, label='comic')
comitat = op('comitat', range=String, label='comitat of a settlement')
command = op('command', range=String, label='command')
commandant = op('commandant', range=Item, label='commandant')
commander = op('commander', range=Item, label='commander')
commandModule = op('commandModule', range=String, label='command module')
commandStructure = op('commandStructure', range=Item, label='command structure')
comment = op('comment', range=String, label='comment')
commissioner = op('commissioner', range=String, label='commissioner')
commissionerDate = op('commissionerDate', range=String, label='commissioner date')
commissioningDate = op('commissioningDate', range=Time, label='commissioning date')
committee = op('committee', range=String, label='committee')
commonName = op('commonName', range=Text, label='common name')
commune = op('commune', range=Item, label='commune')
communityIsoCode = op('communityIsoCode', range=String, label='iso code of a community')
company = op('company', range=Item, label='company')
comparable = op('comparable', range=Item, label='comparable')
competition = op('competition', range=Item, label='competition')
competitionTitle = op('competitionTitle', range=Item, label='competition title')
compiler = op('compiler', range=Item, label='compiler')
completionDate = op('completionDate', range=Time, label='completion date')
complexity = op('complexity', range=String, label='complexity')
complications = op('complications', range=String, label='complications')
component = op('component', range=Item, label='component')
composer = op('composer', range=Item, label='composer')
compressionRatio = op('compressionRatio', range=String, label='compression ratio')
configuration = op('configuration', range=String, label='configuration')
confirmedCases = op('confirmedCases', range=Quantity, label='Confirmed Cases')
conflict = op('conflict', range=Item, label='conflict')
consecration = op('consecration', range=String, label='consecration')
conservationStatus = op('conservationStatus', range=String, label='conservation status')
conservationStatusSystem = op('conservationStatusSystem', range=String, label='conservation status system')
constituencyDistrict = op('constituencyDistrict', range=Item, label='constituency district')
contest = op('contest', range=Item, label='contest')
continent = op('continent', range=Item, label='continent')
continentalTournament = op('continentalTournament', range=Item, label='continental tournament')
continentalTournamentBronze = op('continentalTournamentBronze', range=Quantity, label='continental tournament bronze')
continentalTournamentGold = op('continentalTournamentGold', range=Quantity, label='continental tournament gold')
continentalTournamentSilver = op('continentalTournamentSilver', range=Quantity, label='continental tournament silver')
continentRank = op('continentRank', range=Quantity, label='continent rank')
contractAward = op('contractAward', range=Time, label='contract award')
contractor = op('contractor', range=Item, label='contractor')
convictionDate = op('convictionDate', range=Time, label='conviction date')
copilote = op('copilote', range=Item, label='copilote')
coProducer = op('coProducer', range=Item, label='co producer')
coronationDate = op('coronationDate', range=Time, label='coronation date')
cosparId = op('cosparId', range=String, label='COSPAR id')
cost = op('cost', range=Quantity, label='cost ($)')
costumeDesigner = op('costumeDesigner', range=Item, label='costume designer')
council = op('council', range=String, label='council of a liechtenstein settlement')
councilArea = op('councilArea', range=Item, label='Council area')
country = op('country', range=Item, label='country')
countryCode = op('countryCode', range=String, label='country code')
countryOrigin = op('countryOrigin', range=Item, label='country origin')
countryRank = op('countryRank', range=Quantity, label='country rank')
countryWithFirstAstronaut = op('countryWithFirstAstronaut', range=Item, label='country with first astronaut')
countryWithFirstSatellite = op('countryWithFirstSatellite', range=Item, label='country with first satellite')
countryWithFirstSatelliteLaunched = op('countryWithFirstSatelliteLaunched', range=Item, label='country with first satellite launched')
countryWithFirstSpaceflight = op('countryWithFirstSpaceflight', range=Item, label='country with first spaceflight')
county = op('county', range=Item, label='county')
course = op('course', range=Quantity, label='course (μ)')
courseArea = op('courseArea', range=Quantity, label='course area (m2)')
cousurper = op('cousurper', range=Item, label='cousurper')
coverArtist = op('coverArtist', range=Item, label='cover artist')
created = op('created', range=Item, label='created')
creationChristianBishop = op('creationChristianBishop', range=String, label='creation christian bishop')
creationYear = op('creationYear', range=Time, label='year of creation')
creativeDirector = op('creativeDirector', range=Item, label='creative director')
creator = op('creator', range=Item, label='creator (agent)')
creatorOfDish = op('creatorOfDish', range=Item, label='creator of dish')
credit = op('credit', range=String, label='credit')
crew = op('crew', range=Item, label='crew')
crewMember = op('crewMember', range=Item, label='crew member')
crews = op('crews', range=Quantity, label='crews')
crewSize = op('crewSize', range=Quantity, label='crew size')
criminalCharge = op('criminalCharge', range=String, label='criminal charge')
criteria = op('criteria', range=String, label='criteria')
crosses = op('crosses', range=Item, label='crosses')
crownDependency = op('crownDependency', range=String, label='crown dependency')
cuisine = op('cuisine', range=String, label='cuisine')
cultivatedVariety = op('cultivatedVariety', range=Item, label='cultivar')
curator = op('curator', range=Item, label='curator')
currency = op('currency', range=Item, label='currency')
currencyCode = op('currencyCode', range=String, label='currency code')
currentCity = op('currentCity', range=Item, label='current city')
currentLeague = op('currentLeague', range=Item, label='current league')
currentlyUsedFor = op('currentlyUsedFor', range=String, label='currently used for')
currentMember = op('currentMember', range=Item, label='current member')
currentPartner = op('currentPartner', range=Item, label='current partner')
currentRank = op('currentRank', range=Quantity, label='current rank')
currentRecord = op('currentRecord', range=String, label='current record')
currentStatus = op('currentStatus', range=String, label='current status')
currentTeam = op('currentTeam', range=Item, label='current team')
currentTeamManager = op('currentTeamManager', range=Item, label='current team manager')
currentTeamMember = op('currentTeamMember', range=Item, label='current team member')
currentWorldChampion = op('currentWorldChampion', range=Item, label='current world champion')
custodian = op('custodian', range=Item, label='custodian')
cylinderBore = op('cylinderBore', range=Quantity, label='cylinder bore (μ)')
cylinderCount = op('cylinderCount', range=Quantity, label='cylinder count')
dailyVaccinationsPerMillion = op('dailyVaccinationsPerMillion', range=Item, label='Daily Vaccinations Per Million')
dailyVaccinationsRaw = op('dailyVaccinationsRaw', range=Item, label='Daily Vaccinations Raw')
daira = op('daira', range=Item, label='daira')
dam = op('dam', range=Item, label='dam')
damage = op('damage', range=Item, label='damage amount')
damsire = op('damsire', range=Item, label='damsire')
danseCompetition = op('danseCompetition', range=String, label='danse competition')
danseScore = op('danseScore', range=String, label='danse score')
date = op('date', range=Time, label='date')
dateAct = op('dateAct', range=Time, label='date act')
dateAgreement = op('dateAgreement', range=Time, label='date of an agreement')
dateBudget = op('dateBudget', range=Time, label='date budget')
dateClosed = op('dateClosed', range=Time, label='date closed')
dateCompleted = op('dateCompleted', range=Time, label='date completed')
dateConstruction = op('dateConstruction', range=Time, label='date construction')
dateExtended = op('dateExtended', range=Time, label='date extended')
dateLastUpdated = op('dateLastUpdated', range=Time, label='Date Last Updated')
dateOfAbandonment = op('dateOfAbandonment', range=Time, label='date of abandonment')
dateOfBurial = op('dateOfBurial', range=Time, label='date of burial')
dateUnveiled = op('dateUnveiled', range=Time, label='date unveiled')
dateUse = op('dateUse', range=Time, label='date use')
daughter = op('daughter', range=Item, label='daughter')
day = op('day', range=Time, label='day')
dbnlCodeDutch = op('dbnlCodeDutch', range=String, label='Digital Library code NL')
dcc = op('dcc', range=String, label='Dewey Decimal Classification')
deadInFightDate = op('deadInFightDate', range=String, label='dead in fight date')
deadInFightPlace = op('deadInFightPlace', range=String, label='dead in fight place')
dean = op('dean', range=Item, label='dean')
deanery = op('deanery', range=Item, label='deanery')
deathAge = op('deathAge', range=Quantity, label='death age')
deathDate = op('deathDate', range=Time, label='death date')
deathPlace = op('deathPlace', range=Item, label='death place')
deaths = op('deaths', range=Item, label='Deaths')
deathYear = op('deathYear', range=Time, label='death year')
debut = op('debut', range=Time, label='debut')
debutTeam = op('debutTeam', range=Item, label='debut team')
debutWork = op('debutWork', range=Item, label='debutWork')
dec = op('dec', range=String, label='dec')
decay = op('decay', range=Time, label='decay')
decideDate = op('decideDate', range=Time, label='decide date')
declination = op('declination', range=Quantity, label='declination')
decommissioningDate = op('decommissioningDate', range=Time, label='decommissioning date')
deFactoLanguage = op('deFactoLanguage', range=Item, label='de facto language')
defeat = op('defeat', range=Quantity, label='defeat')
defeatAsMgr = op('defeatAsMgr', range=Quantity, label='defeat as team manager')
definition = op('definition', range=String, label='definition')
defunct = op('defunct', range=Quantity, label='Defunct')
delegateMayor = op('delegateMayor', range=Item, label='delegate mayor')
delegation = op('delegation', range=String, label='delegation')
deliveryDate = op('deliveryDate', range=Time, label='delivery date')
deme = op('deme', range=String, label='deme')
demographics = op('demographics', range=Item, label='demographics')
demographicsAsOf = op('demographicsAsOf', range=Time, label='demographics as of')
demolitionDate = op('demolitionDate', range=Time, label='demolition date')
demolitionYear = op('demolitionYear', range=Time, label='demolition year')
demonym = op('demonym', range=Text, label='demonym')
density = op('density', range=Quantity, label='density (μ3)')
department = op('department', range=Item, label='department')
departmentCode = op('departmentCode', range=String, label='محکمہ کا کوڈ')
departmentPosition = op('departmentPosition', range=String, label='geolocDepartment')
depictionDescription = op('depictionDescription', range=Text, label='depiction description (caption)')
depth = op('depth', range=Quantity, label='depth (μ)')
depthQuote = op('depthQuote', range=String, label='depth quote')
depths = op('depths', range=Item, label='depths')
deputy = op('deputy', range=Item, label='deputy')
derivative = op('derivative', range=Item, label='derivative')
derivedWord = op('derivedWord', range=String, label='derived word')
description = op('description', range=Text, label='description')
designCompany = op('designCompany', range=Item, label='designer company')
designer = op('designer', range=Item, label='designer')
destination = op('destination', range=Item, label='destination')
destructionDate = op('destructionDate', range=Time, label='destruction date')
detectionMethod = op('detectionMethod', range=String, label='Method of discovery')
detractor = op('detractor', range=Item, label='detractor')
developer = op('developer', range=Item, label='developer')
diameter = op('diameter', range=Quantity, label='diameter (μ)')
digitalChannel = op('digitalChannel', range=String, label='digital channel')
digitalSubChannel = op('digitalSubChannel', range=String, label='digital sub channel')
diocese = op('diocese', range=Item, label='diocese')
diploma = op('diploma', range=Item, label='diploma')
director = op('director', range=Item, label='film director')
disappearanceDate = op('disappearanceDate', range=Time, label='date disappearance of a populated place')
disbanded = op('disbanded', range=Time, label='disbanded')
discharge = op('discharge', range=Quantity, label='discharge (m³/s)')
dischargeAverage = op('dischargeAverage', range=Quantity, label='discharge average (m³/s)')
disciple = op('disciple', range=Item, label='disciple')
discontinued = op('discontinued', range=Time, label='discontinued')
discovered = op('discovered', range=Time, label='discovery date')
discoverer = op('discoverer', range=Item, label='discoverer')
discovery = op('discovery', range=String, label='date when the island has been discovered')
disease = op('disease', range=Item, label='disease')
diseasesDb = op('diseasesDb', range=String, label='diseasesDb')
diseasesDB = op('diseasesDB', range=String, label='DiseasesDB')
displacement = op('displacement', range=Quantity, label='displacement (μ³)')
dissolutionDate = op('dissolutionDate', range=Time, label='dissolution date')
dissolutionYear = op('dissolutionYear', range=Time, label='dissolution year')
dissolved = op('dissolved', range=Time, label='dissolved')
dist_ly = op('dist_ly', range=String, label='dist_ly')
dist_pc = op('dist_pc', range=Quantity, label='dist_pc')
distance = op('distance', range=Quantity, label='distance (μ)')
distanceLaps = op('distanceLaps', range=Quantity, label='distance laps')
distanceToBelfast = op('distanceToBelfast', range=Quantity, label='distance to Belfast (μ)')
distanceToCapital = op('distanceToCapital', range=Quantity, label='distance to capital (μ)')
distanceToCardiff = op('distanceToCardiff', range=Quantity, label='distance to Cardiff (μ)')
distanceToCharingCross = op('distanceToCharingCross', range=Quantity, label='distance to Charing Cross (μ)')
distanceToDouglas = op('distanceToDouglas', range=Quantity, label='distance to Douglas (μ)')
distanceToDublin = op('distanceToDublin', range=Quantity, label='distance to Dublin (μ)')
distanceToEdinburgh = op('distanceToEdinburgh', range=Quantity, label='distance to Edinburgh (μ)')
distanceToLondon = op('distanceToLondon', range=Quantity, label='distance to London (μ)')
distanceToNearestCity = op('distanceToNearestCity', range=Quantity, label='distance to nearest city (μ)')
distanceTraveled = op('distanceTraveled', range=Quantity, label='distance traveled (μ)')
distributingCompany = op('distributingCompany', range=Item, label='distributing company')
distributingLabel = op('distributingLabel', range=Item, label='distributing label')
distributor = op('distributor', range=Item, label='distributor')
district = op('district', range=Item, label='district')
dockedTime = op('dockedTime', range=Quantity, label='docked time (s)')
doctoralAdvisor = op('doctoralAdvisor', range=Item, label='doctoral advisor')
doctoralStudent = op('doctoralStudent', range=Item, label='doctoral student')
documentDesignation = op('documentDesignation', range=String, label='String designation of the WrittenWork describing the resource')
documentNumber = op('documentNumber', range=String, label='document number')
dorlandsId = op('dorlandsId', range=String, label='DorlandsID')
dorlandsPrefix = op('dorlandsPrefix', range=String, label='Dorlands prefix')
dorlandsSuffix = op('dorlandsSuffix', range=String, label='Dorlands suffix')
dose = op('dose', range=Quantity, label='Dose')
dosesFirst = op('dosesFirst', range=Quantity, label='DosesFirst')
dosesSecond = op('dosesSecond', range=Quantity, label='DosesSecond')
draft = op('draft', range=String, label='draft')
draftLeague = op('draftLeague', range=String, label='draft league')
draftPick = op('draftPick', range=String, label='draft pick')
draftPosition = op('draftPosition', range=Quantity, label='draft position')
draftRound = op('draftRound', range=String, label='draft round')
draftTeam = op('draftTeam', range=Item, label='draft team')
draftYear = op('draftYear', range=Time, label='draft year')
drainsFrom = op('drainsFrom', range=Item, label='drains from')
drainsTo = op('drainsTo', range=Item, label='drains to')
drama = op('drama', range=Item, label='drama')
dressCode = op('dressCode', range=String, label='dress code')
drug = op('drug', range=Text, label='Drug')
drugbank = op('drugbank', range=String, label='DrugBank')
dryCargo = op('dryCargo', range=Quantity, label='dry cargo (g)')
dubber = op('dubber', range=Item, label='dubber')
duration = op('duration', range=Quantity, label='duration (s)')
dutchArtworkCode = op('dutchArtworkCode', range=String, label='Dutch artwork code')
dutchCOROPCode = op('dutchCOROPCode', range=String, label='Dutch COROP code')
dutchMIPCode = op('dutchMIPCode', range=String, label='monument code for the Monuments Inventory Project')
dutchNAIdentifier = op('dutchNAIdentifier', range=String, label='Identifier for Duch National Archive')
dutchPPNCode = op('dutchPPNCode', range=String, label='Dutch PPN code')
dutchRKDCode = op('dutchRKDCode', range=String, label='Dutch RKD code')
dutchWinkelID = op('dutchWinkelID', range=String, label='Dutch PPN code')
eastPlace = op('eastPlace', range=Item, label='east place')
ecNumber = op('ecNumber', range=String, label='EC number')
editing = op('editing', range=Item, label='editing')
editor = op('editor', range=Item, label='editor')
editorTitle = op('editorTitle', range=Text, label='editor title')
educationPlace = op('educationPlace', range=Item, label='education place')
effectiveRadiatedPower = op('effectiveRadiatedPower', range=Quantity, label='effectiveRadiatedPower (W)')
egafdId = op('egafdId', range=String, label='egafd id')
einecsNumber = op('einecsNumber', range=String, label='EINECS number')
ekatteCode = op('ekatteCode', range=String, label='EKATTE code')
electionDate = op('electionDate', range=Time, label='election date')
electionDateLeader = op('electionDateLeader', range=Time, label='election date leader')
electionMajority = op('electionMajority', range=Quantity, label='election majority')
elementAbove = op('elementAbove', range=Item, label='element above')
elementBlock = op('elementBlock', range=String, label='element block')
elementGroup = op('elementGroup', range=Quantity, label='element group')
elementPeriod = op('elementPeriod', range=Quantity, label='element period')
elevation = op('elevation', range=Quantity, label='elevation (μ)')
elevationQuote = op('elevationQuote', range=String, label='elevation quote')
elevatorCount = op('elevatorCount', range=Quantity, label='elevator count')
elo = op('elo', range=Quantity, label='ELO rating')
eloRecord = op('eloRecord', range=Quantity, label='maximum ELO rating')
emblem = op('emblem', range=String, label='emblem')
eMedicineSubject = op('eMedicineSubject', range=Text, label='eMedicine subject')
eMedicineTopic = op('eMedicineTopic', range=Text, label='eMedicine topic')
emmyAward = op('emmyAward', range=Item, label='Emmy Award')
employer = op('employer', range=Item, label='employer')
employersCelebration = op('employersCelebration', range=String, label='employer\'s celebration')
end = op('end', range=Time, label='end')
endangeredSince = op('endangeredSince', range=Time, label='endangered since')
endCareer = op('endCareer', range=String, label='end career')
endDate = op('endDate', range=Time, label='end date')
endDateTime = op('endDateTime', range=Time, label='end date and time')
endingTheme = op('endingTheme', range=Item, label='ending theme')
endOccupation = op('endOccupation', range=String, label='end occupation')
endowment = op('endowment', range=Quantity, label='endowment ($)')
endPoint = op('endPoint', range=Item, label='end point')
endYear = op('endYear', range=Time, label='end year')
endYearOfInsertion = op('endYearOfInsertion', range=Time, label='end year of insertion')
endYearOfSales = op('endYearOfSales', range=Time, label='end year of sales')
enemy = op('enemy', range=Item, label='enemy')
engine = op('engine', range=Item, label='engine')
engineer = op('engineer', range=Item, label='engineer')
enginePower = op('enginePower', range=Quantity, label='engine power')
ensembl = op('ensembl', range=String, label='ensemble')
enshrinedDeity = op('enshrinedDeity', range=Item, label='enshrined deity')
entourage = op('entourage', range=Item, label='entourage')
entrezgene = op('entrezgene', range=String, label='EntrezGene')
episode = op('episode', range=String, label='episode')
episodeNumber = op('episodeNumber', range=Quantity, label='episode number')
epoch = op('epoch', range=String, label='epoch')
eptFinalTable = op('eptFinalTable', range=Quantity, label='ept final table')
eptItm = op('eptItm', range=Quantity, label='ept itm')
eptTitle = op('eptTitle', range=String, label='ept title')
equity = op('equity', range=Quantity, label='equity ($)')
eruption = op('eruption', range=String, label='eruption')
eruptionYear = op('eruptionYear', range=Time, label='eruption date')
escalafon = op('escalafon', range=String, label='escalafon')
escapeVelocity = op('escapeVelocity', range=Quantity, label='escape velocity (kmh)')
espnId = op('espnId', range=Quantity, label='ESPN id')
established = op('established', range=String, label='Established')
establishment = op('establishment', range=Quantity, label='Establishment')
eTeatrId = op('eTeatrId', range=String, label='e-teatr.pl id')
ethnicGroup = op('ethnicGroup', range=Item, label='ethnic group')
ethnicGroupsInYear = op('ethnicGroupsInYear', range=Time, label='ethnic groups in year')
ethnicity = op('ethnicity', range=Item, label='ethnicity')
eurobabeIndexId = op('eurobabeIndexId', range=String, label='eurobabe index id')
europeanChampionship = op('europeanChampionship', range=String, label='european championship')
europeanUnionEntranceDate = op('europeanUnionEntranceDate', range=Time, label='european union entrance date')
event = op('event', range=Item, label='event')
eventDate = op('eventDate', range=Time, label='event date')
eventDescription = op('eventDescription', range=String, label='event description')
executiveHeadteacher = op('executiveHeadteacher', range=Item, label='executive headteacher')
executiveProducer = op('executiveProducer', range=Item, label='executive producer')
exhibition = op('exhibition', range=String, label='exhibition')
expedition = op('expedition', range=String, label='expedition')
externalOrnament = op('externalOrnament', range=String, label='external ornament')
extinctionDate = op('extinctionDate', range=Time, label='extinction date')
extinctionYear = op('extinctionYear', range=Time, label='extinction year')
eyeColor = op('eyeColor', range=String, label='eye color')
eyeColour = op('eyeColour', range=String, label='eye colour')
eyes = op('eyes', range=String, label='eyes')
faaLocationIdentifier = op('faaLocationIdentifier', range=String, label='FAA Location Identifier')
facilityId = op('facilityId', range=Quantity, label='facility id')
facultySize = op('facultySize', range=Quantity, label='faculty size')
failedLaunches = op('failedLaunches', range=Quantity, label='failed launches')
family = op('family', range=Item, label='family')
familyMember = op('familyMember', range=Item, label='family member')
fansgroup = op('fansgroup', range=String, label='fansgroup')
fareZone = op('fareZone', range=String, label='fare zone')
fastestDriver = op('fastestDriver', range=Item, label='fastest driver')
fastestDriverCountry = op('fastestDriverCountry', range=Item, label='fastest driver country')
fastestDriverTeam = op('fastestDriverTeam', range=Item, label='fastest driver team')
fastestLap = op('fastestLap', range=Quantity, label='fastest lap')
fat = op('fat', range=Quantity, label='fat (g)')
fatalityRate = op('fatalityRate', range=Quantity, label='Fatality Rate')
fate = op('fate', range=Text, label='fate')
father = op('father', range=Item, label='father')
fauna = op('fauna', range=String, label='fauna')
fc = op('fc', range=Quantity, label='FC')
fcRuns = op('fcRuns', range=Quantity, label='FC runs')
fdaUniiCode = op('fdaUniiCode', range=String, label='FDA UNII code')
feastDay = op('feastDay', range=Time, label='feast day, holiday')
feat = op('feat', range=String, label='feat')
feature = op('feature', range=String, label='feature')
features = op('features', range=Item, label='features')
featuring = op('featuring', range=Item, label='featuring')
fedCup = op('fedCup', range=String, label='fed cup')
federalState = op('federalState', range=Item, label='federal state')
federation = op('federation', range=Item, label='federation')
fees = op('fees', range=Quantity, label='fees ($)')
fibahof = op('fibahof', range=String, label='fibahof')
fight = op('fight', range=Quantity, label='fight')
fighter = op('fighter', range=String, label='fighter')
fileExtension = op('fileExtension', range=String, label='The extension of this file')
filename = op('filename', range=String, label='filename')
fileSize = op('fileSize', range=Quantity, label='size (B)')
fileURL = op('fileURL', range=Item, label='The URL at which this file can be downloaded')
fillingStation = op('fillingStation', range=Item, label='filling station')
film = op('film', range=Item, label='film')
filmAudioType = op('filmAudioType', range=String, label='film audio type')
filmColourType = op('filmColourType', range=String, label='film colour type')
filmFareAward = op('filmFareAward', range=Item, label='Film Fare Award')
filmNumber = op('filmNumber', range=Quantity, label='film number')
filmPolskiId = op('filmPolskiId', range=String, label='FilmPolski.pl id')
filmRuntime = op('filmRuntime', range=Quantity, label='film runtime (s)')
filmVersion = op('filmVersion', range=Item, label='film version')
finalFlight = op('finalFlight', range=Time, label='final flight')
finalLost = op('finalLost', range=Quantity, label='final lost')
finalLostDouble = op('finalLostDouble', range=String, label='final lost double')
finalLostSingle = op('finalLostSingle', range=String, label='final lost single')
finalLostTeam = op('finalLostTeam', range=String, label='final lost team')
finalPublicationDate = op('finalPublicationDate', range=Time, label='final publication date')
finalPublicationYear = op('finalPublicationYear', range=Time, label='final publication year')
fipsCode = op('fipsCode', range=String, label='fips code')
firstAirDate = op('firstAirDate', range=Time, label='first air date')
firstAppearance = op('firstAppearance', range=String, label='first appearance')
firstAscent = op('firstAscent', range=String, label='first ascent')
firstAscentPerson = op('firstAscentPerson', range=Item, label='person that first ascented a mountain')
firstAscentYear = op('firstAscentYear', range=Time, label='year of first ascent')
firstBroadcast = op('firstBroadcast', range=String, label='first broadcast')
firstDriver = op('firstDriver', range=Item, label='first driver')
firstDriverCountry = op('firstDriverCountry', range=Item, label='first driver country')
firstDriverTeam = op('firstDriverTeam', range=Item, label='winning team')
firstFlight = op('firstFlight', range=Item, label='first flight')
firstFlightEndDate = op('firstFlightEndDate', range=Time, label='first flight end date')
firstFlightStartDate = op('firstFlightStartDate', range=Time, label='first flight start date')
firstGame = op('firstGame', range=String, label='first game')
firstLaunch = op('firstLaunch', range=Time, label='first launch')
firstLaunchDate = op('firstLaunchDate', range=Time, label='first launch date')
firstLaunchRocket = op('firstLaunchRocket', range=Item, label='first launch rocket')
firstLeader = op('firstLeader', range=Item, label='firstLeader')
firstMention = op('firstMention', range=String, label='first mention')
firstOlympicEvent = op('firstOlympicEvent', range=Item, label='first olympic event')
firstOwner = op('firstOwner', range=Item, label='first owner')
firstPlace = op('firstPlace', range=String, label='first place')
firstPopularVote = op('firstPopularVote', range=Item, label='firstPopularVote')
firstProMatch = op('firstProMatch', range=String, label='first pro match')
firstPublicationDate = op('firstPublicationDate', range=Time, label='first publication date')
firstPublicationYear = op('firstPublicationYear', range=Time, label='first publication year')
firstPublisher = op('firstPublisher', range=Item, label='first publisher')
firstRace = op('firstRace', range=Item, label='first race')
firstWin = op('firstWin', range=Item, label='first win')
firstWinner = op('firstWinner', range=Item, label='first winner')
flag = op('flag', range=String, label='flag (image)')
flagBearer = op('flagBearer', range=Item, label='flag bearer')
flagBorder = op('flagBorder', range=String, label='flag border')
flagCaption = op('flagCaption', range=String, label='flag caption')
flagLink = op('flagLink', range=String, label='flag Link')
flagSize = op('flagSize', range=Quantity, label='flagSize')
flashPoint = op('flashPoint', range=Quantity, label='flash point')
floodingDate = op('floodingDate', range=Time, label='flooding date')
floorArea = op('floorArea', range=Quantity, label='floor area (m2)')
floorCount = op('floorCount', range=Quantity, label='floor count')
flora = op('flora', range=String, label='flora')
flower = op('flower', range=Item, label='flower')
flyingHours = op('flyingHours', range=Quantity, label='flying hours (s)')
foalDate = op('foalDate', range=Time, label='foal date')
followingEvent = op('followingEvent', range=Item, label='following event')
foot = op('foot', range=String, label='foot')
footedness = op('footedness', range=Item, label='Footedness')
forces = op('forces', range=String, label='forces')
formationDate = op('formationDate', range=Time, label='formation date')
formationYear = op('formationYear', range=Time, label='formation year')
formerBandMember = op('formerBandMember', range=Item, label='former band member')
formerBroadcastNetwork = op('formerBroadcastNetwork', range=Item, label='former broadcast network')
formerCallsign = op('formerCallsign', range=String, label='former call sign')
formerChannel = op('formerChannel', range=String, label='former channel')
formerChoreographer = op('formerChoreographer', range=Item, label='former choreographer')
formerCoach = op('formerCoach', range=Item, label='former coach')
formerHighschool = op('formerHighschool', range=Item, label='former highschool')
formerName = op('formerName', range=Text, label='former name')
formerPartner = op('formerPartner', range=Item, label='former partner')
formerTeam = op('formerTeam', range=Item, label='former team')
formula = op('formula', range=String, label='formula')
fossil = op('fossil', range=Item, label='fossil')
foundation = op('foundation', range=String, label='foundation')
foundationPlace = op('foundationPlace', range=Item, label='foundation place')
foundedBy = op('foundedBy', range=Item, label='founded by')
founder = op('founder', range=Item, label='founder')
foundingDate = op('foundingDate', range=Time, label='founding date')
foundingYear = op('foundingYear', range=Time, label='founding year')
fourthCommander = op('fourthCommander', range=Item, label='fourth commander')
frazioni = op('frazioni', range=Item, label='frazioni')
free = op('free', range=String, label='free')
freeDanseScore = op('freeDanseScore', range=String, label='free danse score')
freeFlightTime = op('freeFlightTime', range=Quantity, label='free flight time (s)')
freeLabel = op('freeLabel', range=String, label='freeLabel')
freeProgCompetition = op('freeProgCompetition', range=String, label='free prog competition')
freeProgScore = op('freeProgScore', range=String, label='free prog score')
freeScoreCompetition = op('freeScoreCompetition', range=String, label='free score competition')
frequency = op('frequency', range=Quantity, label='frequency (Hz)')
frequencyOfPublication = op('frequencyOfPublication', range=String, label='frequency of publication')
frequentlyUpdated = op('frequentlyUpdated', range=String, label='frequently updated')
friend = op('friend', range=Item, label='friend')
frontierLength = op('frontierLength', range=Quantity, label='length of a frontier')
frozen = op('frozen', range=String, label='frozen')
fuelCapacity = op('fuelCapacity', range=Quantity, label='fuel capacity (μ³)')
fuelConsumption = op('fuelConsumption', range=String, label='fuel consumption')
fuelTypeName = op('fuelTypeName', range=Text, label='fuel type')
fullCompetition = op('fullCompetition', range=String, label='full competition')
fullScore = op('fullScore', range=String, label='full score')
functionEndDate = op('functionEndDate', range=Time, label='function end date')
functionEndYear = op('functionEndYear', range=Time, label='function end year')
functionStartDate = op('functionStartDate', range=Time, label='function start date')
functionStartYear = op('functionStartYear', range=Time, label='function start year')
fundedBy = op('fundedBy', range=Item, label='funded by')
galicianSpeakersDate = op('galicianSpeakersDate', range=Time, label='galicianSpeakersDate')
galicianSpeakersPercentage = op('galicianSpeakersPercentage', range=String, label='galicianSpeakersPercentage')
galleryItem = op('galleryItem', range=Item, label='gallery item')
gameArtist = op('gameArtist', range=Item, label='game artist')
gameModus = op('gameModus', range=String, label='Modus the game can be played in')
games = op('games', range=String, label='games')
garrison = op('garrison', range=Item, label='garrison')
gasChambers = op('gasChambers', range=String, label='gas chambers')
gaudiAward = op('gaudiAward', range=Item, label='Gaudí Award')
gdpPerCapita = op('gdpPerCapita', range=Quantity, label='gross domestic product (GDP) per capita')
geminiAward = op('geminiAward', range=Item, label='Gemini Award')
geneLocation = op('geneLocation', range=Item, label='Gene Location')
geneLocationEnd = op('geneLocationEnd', range=Quantity, label='gene location end')
geneLocationStart = op('geneLocationStart', range=Quantity, label='gene location start')
generalCouncil = op('generalCouncil', range=Item, label='general council')
generalManager = op('generalManager', range=Item, label='general manager')
generationUnits = op('generationUnits', range=Text, label='generation units')
geneReviewsId = op('geneReviewsId', range=String, label='geneReviewsId')
geneReviewsName = op('geneReviewsName', range=Text, label='geneReviewsName')
genomeDB = op('genomeDB', range=String, label='Genome DB')
genre = op('genre', range=Item, label='genre')
geolocDepartment = op('geolocDepartment', range=Item, label='geolocDepartment')
geolocDual = op('geolocDual', range=String, label='geolocdual')
geologicPeriod = op('geologicPeriod', range=String, label='geologic period')
geology = op('geology', range=String, label='geology')
giniCoefficient = op('giniCoefficient', range=Quantity, label='gini coefficient')
giniCoefficientAsOf = op('giniCoefficientAsOf', range=Time, label='gini coefficient as of')
giniCoefficientRanking = op('giniCoefficientRanking', range=Quantity, label='gini coefficient ranking')
glycemicIndex = op('glycemicIndex', range=Quantity, label='glycemic index')
gnisCode = op('gnisCode', range=String, label='gnis code')
gnl = op('gnl', range=String, label='gnl')
goalsInLeague = op('goalsInLeague', range=Quantity, label='goals in league')
goalsInNationalTeam = op('goalsInNationalTeam', range=Quantity, label='goals in national team')
goldenCalfAward = op('goldenCalfAward', range=Item, label='Golden Calf Award')
goldenGlobeAward = op('goldenGlobeAward', range=Item, label='Golden Globe Award')
goldenRaspberryAward = op('goldenRaspberryAward', range=Item, label='Golden Raspberry Award')
goldMedalDouble = op('goldMedalDouble', range=String, label='gold medal double')
goldMedalist = op('goldMedalist', range=Item, label='gold medalist')
goldMedalMixed = op('goldMedalMixed', range=String, label='gold medal mixed')
goldMedalSingle = op('goldMedalSingle', range=String, label='gold medal single')
governingBody = op('governingBody', range=Item, label='governing body')
governmentCountry = op('governmentCountry', range=Item, label='government country')
governmentElevation = op('governmentElevation', range=Quantity, label='government elevation (μ)')
governmentMountain = op('governmentMountain', range=Item, label='government mountain')
governmentPlace = op('governmentPlace', range=Item, label='government place')
governmentRegion = op('governmentRegion', range=Item, label='government region')
governmentType = op('governmentType', range=Item, label='government type')
governor = op('governor', range=Item, label='governor')
governorate = op('governorate', range=String, label='governorate')
governorGeneral = op('governorGeneral', range=Item, label='governor general')
goyaAward = op('goyaAward', range=Item, label='Goya Award')
gradName = op('gradName', range=String, label='GARDName')
gradNum = op('gradNum', range=String, label='GARDNum')
grammyAward = op('grammyAward', range=Item, label='Grammy Award')
grandsire = op('grandsire', range=Item, label='grandsire')
grave = op('grave', range=String, label='grave')
grayPage = op('grayPage', range=Quantity, label='Gray page')
graySubject = op('graySubject', range=Quantity, label='Gray subject')
greekName = op('greekName', range=String, label='name in ancient Greek')
greenLongDistancePisteNumber = op('greenLongDistancePisteNumber', range=Quantity, label='green long distance piste number')
greenSkiPisteNumber = op('greenSkiPisteNumber', range=Quantity, label='green ski piste number')
gridReference = op('gridReference', range=String, label='grid reference')
grindingCapability = op('grindingCapability', range=String, label='grinding capability')
gross = op('gross', range=Quantity, label='gross ($)')
grossDomesticProduct = op('grossDomesticProduct', range=Quantity, label='gross domestic product (GDP)')
grossDomesticProductAsOf = op('grossDomesticProductAsOf', range=Time, label='gross domestic product as of')
grossDomesticProductNominalPerCapita = op('grossDomesticProductNominalPerCapita', range=Item, label='gross domestic product nominal per capita')
grossDomesticProductPerPeople = op('grossDomesticProductPerPeople', range=String, label='gross domestic product per people')
grossDomesticProductPurchasingPowerParityPerCapita = op('grossDomesticProductPurchasingPowerParityPerCapita', range=Item, label='gross domestic product purchasing power parity per capita')
grossDomesticProductRank = op('grossDomesticProductRank', range=String, label='gross domestic product rank')
ground = op('ground', range=Item, label='ground')
groundsForLiquidation = op('groundsForLiquidation', range=Text, label='grounds for termination of activities')
groupCommemorated = op('groupCommemorated', range=String, label='group commemorated')
growingGrape = op('growingGrape', range=Item, label='growing grape')
guest = op('guest', range=Item, label='guest')
gun = op('gun', range=String, label='aircraft gun')
hairColor = op('hairColor', range=String, label='hair color')
hairColour = op('hairColour', range=String, label='hair colour')
hairs = op('hairs', range=String, label='hairs')
hallOfFame = op('hallOfFame', range=String, label='hall of fame')
handisport = op('handisport', range=String, label='handisport')
hasAbsorbedMunicipality = op('hasAbsorbedMunicipality', range=Item, label='the previous municipality from which this one has been created or enlarged')
hasAnnotation = op('hasAnnotation', range=Item, label='Indicates an annotation associated with this document')
hasInsidePlace = op('hasInsidePlace', range=Item, label='has inside place')
hasJunctionWith = op('hasJunctionWith', range=Item, label='has junction with')
hasKMLData = op('hasKMLData', range=String, label='Has KML data associated with it (usually because of KML overlays)')
hasNaturalBust = op('hasNaturalBust', range=String, label='has natural bust')
hasOutsidePlace = op('hasOutsidePlace', range=Item, label='has outside place')
head = op('head', range=Item, label='head')
headChef = op('headChef', range=Item, label='head chef')
headLabel = op('headLabel', range=Text, label='head label')
headOfFamily = op('headOfFamily', range=Item, label='family head')
headquarter = op('headquarter', range=Item, label='headquarter')
headteacher = op('headteacher', range=Item, label='head teacher')
height = op('height', range=Quantity, label='height (μ)')
heightAboveAverageTerrain = op('heightAboveAverageTerrain', range=Quantity, label='height above average terrain (μ)')
heightAgainst = op('heightAgainst', range=String, label='height against')
heightAttack = op('heightAttack', range=String, label='height attack')
heir = op('heir', range=Item, label='heir')
heisman = op('heisman', range=String, label='heisman')
hgncid = op('hgncid', range=String, label='HGNCid')
highest = op('highest', range=Item, label='highest')
highestAltitude = op('highestAltitude', range=Item, label='highest altitude')
highestBreak = op('highestBreak', range=Quantity, label='highest break')
highestBuildingInYear = op('highestBuildingInYear', range=Time, label='highest building in year')
highestMountain = op('highestMountain', range=Item, label='highest mountain')
highestPlace = op('highestPlace', range=Item, label='highest place')
highestPoint = op('highestPoint', range=Item, label='highest point')
highestPointIsland = op('highestPointIsland', range=String, label='highest point of the island')
highestRank = op('highestRank', range=Quantity, label='highest rank')
highestRegion = op('highestRegion', range=Item, label='highest region')
highestState = op('highestState', range=Item, label='highest state')
highschool = op('highschool', range=Item, label='highschool')
hipSize = op('hipSize', range=Quantity, label='hip size (μ)')
historicalMap = op('historicalMap', range=String, label='historical map')
historicalName = op('historicalName', range=Text, label='historical name')
historicalRegion = op('historicalRegion', range=String, label='historical region')
hof = op('hof', range=String, label='hof')
homage = op('homage', range=String, label='homage')
homeArena = op('homeArena', range=Item, label='home arena')
homeColourHexCode = op('homeColourHexCode', range=String, label='colour hex code of home jersey or its parts')
homeport = op('homeport', range=Item, label='homeport')
homeStadium = op('homeStadium', range=Item, label='home stadium')
hometown = op('hometown', range=Item, label='home town')
hopmanCup = op('hopmanCup', range=String, label='hopman cup')
horseRidingDiscipline = op('horseRidingDiscipline', range=Item, label='horse riding discipline')
house = op('house', range=Item, label='house')
hraState = op('hraState', range=String, label='hra state')
hsvCoordinateHue = op('hsvCoordinateHue', range=Quantity, label='hue coordinate in the HSV colour space')
hsvCoordinateSaturation = op('hsvCoordinateSaturation', range=Quantity, label='saturation coordinate in the HSV colour space')
hsvCoordinateValue = op('hsvCoordinateValue', range=Quantity, label='value coordinate in the HSV colour space')
hubAirport = op('hubAirport', range=Item, label='hub airport')
humanDevelopmentIndex = op('humanDevelopmentIndex', range=Quantity, label='Human Development Index (HDI)')
humanDevelopmentIndexAsOf = op('humanDevelopmentIndexAsOf', range=Time, label='human development index as of')
humanDevelopmentIndexRank = op('humanDevelopmentIndexRank', range=String, label='human development index rank')
hybrid = op('hybrid', range=Item, label='hybrid')
iafdId = op('iafdId', range=String, label='iafd id')
iataAirlineCode = op('iataAirlineCode', range=String, label='IATA code')
iataLocationIdentifier = op('iataLocationIdentifier', range=String, label='IATA Location Identifier')
ibdbId = op('ibdbId', range=String, label='IBDB ID')
icaoAirlineCode = op('icaoAirlineCode', range=String, label='ICAO code')
icaoLocationIdentifier = op('icaoLocationIdentifier', range=String, label='ICAO Location Identifier')
icd1 = op('icd1', range=String, label='ICD1')
icd10 = op('icd10', range=String, label='ICD10')
icd9 = op('icd9', range=String, label='ICD9')
icdo = op('icdo', range=String, label='ICDO')
iconographicAttributes = op('iconographicAttributes', range=Text, label='iconographic attributes')
id = op('id', range=String, label='id')
idAllocine = op('idAllocine', range=String, label='Allocine ID')
identificationSymbol = op('identificationSymbol', range=String, label='identification symbol')
ideology = op('ideology', range=Item, label='ideology')
idNumber = op('idNumber', range=Quantity, label='id number')
iftaAward = op('iftaAward', range=Item, label='IFTA Award')
iihfHof = op('iihfHof', range=String, label='lihf hof')
illiteracy = op('illiteracy', range=Quantity, label='illiteracy')
illustrator = op('illustrator', range=Item, label='illustrator')
imageSize = op('imageSize', range=Quantity, label='image size (px)')
imdbId = op('imdbId', range=String, label='IMDB id')
impactFactor = op('impactFactor', range=Quantity, label='impact factor')
impactFactorAsOf = op('impactFactorAsOf', range=Time, label='impact factor as of')
importantStation = op('importantStation', range=Item, label='important station')
imposedDanseCompetition = op('imposedDanseCompetition', range=String, label='imposed danse competition')
imposedDanseScore = op('imposedDanseScore', range=String, label='imposed danse score')
inCemetery = op('inCemetery', range=Item, label='in cemetery')
inchi = op('inchi', range=String, label='The IUPAC International Chemical Identifier')
inclination = op('inclination', range=Quantity, label='inclination')
income = op('income', range=String, label='income')
incumbent = op('incumbent', range=Item, label='incumbent')
individualisedGnd = op('individualisedGnd', range=String, label='individualised GND number')
individualisedPnd = op('individualisedPnd', range=Quantity, label='individualised PND number')
infantMortality = op('infantMortality', range=Quantity, label='infant mortality')
inflow = op('inflow', range=Item, label='inflow')
information = op('information', range=String, label='information')
informationName = op('informationName', range=String, label='information name')
ingredientName = op('ingredientName', range=String, label='ingredient name (literal)')
initiallyUsedFor = op('initiallyUsedFor', range=String, label='initally used for')
inn = op('inn', range=String, label='INN')
innervates = op('innervates', range=Item, label='innervates')
inscription = op('inscription', range=String, label='inscription')
inseeCode = op('inseeCode', range=String, label='INSEE code')
installedCapacity = op('installedCapacity', range=Quantity, label='installed capacity (W)')
institution = op('institution', range=Item, label='institution')
instrument = op('instrument', range=Item, label='instrument')
intercommunality = op('intercommunality', range=Item, label='intercommunality')
interest = op('interest', range=String, label='interest')
internationally = op('internationally', range=Quantity, label='internationally')
internationalPhonePrefix = op('internationalPhonePrefix', range=String, label='international phone prefix')
internationalPhonePrefixLabel = op('internationalPhonePrefixLabel', range=String, label='international phone prefix label')
introduced = op('introduced', range=Time, label='introduced')
introductionDate = op('introductionDate', range=Time, label='introduction date')
iobdbId = op('iobdbId', range=String, label='IOBDB ID')
isbn = op('isbn', range=String, label='ISBN')
isCityState = op('isCityState', range=String, label='is a city state')
isHandicappedAccessible = op('isHandicappedAccessible', range=Quantity, label='is handicapped accessible')
isil = op('isil', range=String, label='International Standard Identifier for Libraries and Related Organizations (ISIL)')
island = op('island', range=Item, label='island')
isMinorRevision = op('isMinorRevision', range=Quantity, label='Is a minor revision')
isniId = op('isniId', range=String, label='ISNI Id')
iso31661Code = op('iso31661Code', range=String, label='ISO 3166-1 code')
iso6391Code = op('iso6391Code', range=String, label='ISO 639-1 code')
iso6392Code = op('iso6392Code', range=String, label='ISO 639-2 code')
iso6393Code = op('iso6393Code', range=String, label='ISO 639-3 code')
isoCode = op('isoCode', range=String, label='iso code of a place')
isoCodeRegion = op('isoCodeRegion', range=String, label='ISO region code')
isPartOfAnatomicalStructure = op('isPartOfAnatomicalStructure', range=Item, label='is part of anatomical structure')
isPartOfMilitaryConflict = op('isPartOfMilitaryConflict', range=Item, label='is part of military conflict')
isPartOfName = op('isPartOfName', range=String, label='is part of (literal)')
isPartOfWineRegion = op('isPartOfWineRegion', range=Item, label='is part of wine region')
isPeerReviewed = op('isPeerReviewed', range=Quantity, label='is peer reviewed')
isRouteStop = op('isRouteStop', range=Item, label='is route stop')
issDockings = op('issDockings', range=Quantity, label='iss dockings')
issn = op('issn', range=String, label='issn')
ist = op('ist', range=String, label='ist')
istat = op('istat', range=String, label='code istat')
italicTitle = op('italicTitle', range=String, label='italic title')
ithfDate = op('ithfDate', range=String, label='ithf date')
iucnCategory = op('iucnCategory', range=String, label='iucn category')
iupacName = op('iupacName', range=Text, label='IUPAC name')
jockey = op('jockey', range=Item, label='jockey')
jointCommunity = op('jointCommunity', range=Item, label='joint community')
jstor = op('jstor', range=String, label='JSTOR')
judge = op('judge', range=Item, label='judge')
juniorTeam = op('juniorTeam', range=Item, label='junior team')
juniorYearsEndYear = op('juniorYearsEndYear', range=Time, label='junior years end year')
juniorYearsStartYear = op('juniorYearsStartYear', range=Time, label='junior years start year')
jureLanguage = op('jureLanguage', range=Item, label='jure language')
jutsu = op('jutsu', range=String, label='jutsu')
kegg = op('kegg', range=String, label='KEGG')
keyPerson = op('keyPerson', range=Item, label='key person')
khlDraft = op('khlDraft', range=String, label='khl draft year')
khlDraftTeam = op('khlDraftTeam', range=Item, label='khl draft team')
khlDraftYear = op('khlDraftYear', range=String, label='khl draft year')
killedBy = op('killedBy', range=String, label='killed by')
kindOfCoordinate = op('kindOfCoordinate', range=String, label='kind of coordinate')
kindOfCriminal = op('kindOfCriminal', range=String, label='kind of criminal')
kindOfCriminalAction = op('kindOfCriminalAction', range=String, label='kind of criminal action')
kindOfRock = op('kindOfRock', range=String, label='kind of rock')
kinOfLanguage = op('kinOfLanguage', range=String, label='kindOfLanguage')
ko = op('ko', range=Quantity, label='ko')
lahHof = op('lahHof', range=String, label='lah hof')
lake = op('lake', range=Item, label='vastest lake')
land = op('land', range=Item, label='land')
landArea = op('landArea', range=Quantity, label='area of a land (m2)')
landeshauptmann = op('landeshauptmann', range=Item, label='landeshauptmann')
landingDate = op('landingDate', range=Time, label='landing date')
landingSite = op('landingSite', range=String, label='landing site')
landingVehicle = op('landingVehicle', range=Item, label='landing vehicle')
landPercentage = op('landPercentage', range=Quantity, label='land percentage of a place')
landRegistryCode = op('landRegistryCode', range=String, label='land registry code')
landskap = op('landskap', range=String, label='norwegian landskap')
landtag = op('landtag', range=String, label='austrian land tag')
landtagMandate = op('landtagMandate', range=String, label='austrian land tag mandate')
language = op('language', range=Item, label='language')
languageCode = op('languageCode', range=String, label='language code')
languageRegulator = op('languageRegulator', range=Item, label='language regulator or academy')
largestCity = op('largestCity', range=Item, label='largest city')
largestMetro = op('largestMetro', range=Item, label='largest metro')
largestSettlement = op('largestSettlement', range=Item, label='largest settlement')
largestWin = op('largestWin', range=String, label='largest win')
lastAirDate = op('lastAirDate', range=Time, label='last air date')
lastElectionDate = op('lastElectionDate', range=Time, label='last election date')
lastFamilyMember = op('lastFamilyMember', range=Item, label='last family member')
lastFlight = op('lastFlight', range=Item, label='last flight')
lastFlightEndDate = op('lastFlightEndDate', range=Time, label='last flight end date')
lastFlightStartDate = op('lastFlightStartDate', range=Time, label='last flight start date')
lastLaunch = op('lastLaunch', range=Time, label='last launch')
lastLaunchDate = op('lastLaunchDate', range=Time, label='last launch date')
lastLaunchRocket = op('lastLaunchRocket', range=Item, label='last launch rocket')
lastPosition = op('lastPosition', range=Quantity, label='last position')
lastProMatch = op('lastProMatch', range=String, label='last pro match')
lastPublicationDate = op('lastPublicationDate', range=Time, label='last publication date')
lastRace = op('lastRace', range=Item, label='last race')
lastSeason = op('lastSeason', range=Time, label='last season')
lastWin = op('lastWin', range=Item, label='last win')
laterality = op('laterality', range=String, label='laterality')
latestElection = op('latestElection', range=Time, label='date of latest election')
latestPreviewDate = op('latestPreviewDate', range=Time, label='latest preview date')
latestPreviewVersion = op('latestPreviewVersion', range=String, label='latest preview version')
latestReleaseDate = op('latestReleaseDate', range=Time, label='latest release date')
latestReleaseVersion = op('latestReleaseVersion', range=String, label='latest release version')
latinName = op('latinName', range=String, label='name in latin')
launch = op('launch', range=Time, label='launch')
launchDate = op('launchDate', range=Time, label='launch date')
launches = op('launches', range=Quantity, label='launches')
launchPad = op('launchPad', range=Item, label='launch pad')
launchSite = op('launchSite', range=Item, label='launch site')
laurenceOlivierAward = op('laurenceOlivierAward', range=Item, label='Laurence Olivier Award')
lawCountry = op('lawCountry', range=String, label='law country')
layingDown = op('layingDown', range=Time, label='laying down')
lcc = op('lcc', range=String, label='LCC')
lccn = op('lccn', range=String, label='LCCN')
lccnId = op('lccnId', range=String, label='LCCN Id')
lchfDraft = op('lchfDraft', range=String, label='lchf draft year')
lchfDraftTeam = op('lchfDraftTeam', range=Item, label='lchf draft team')
lchfDraftYear = op('lchfDraftYear', range=String, label='lchf draft year')
leader = op('leader', range=Item, label='leader')
leaderFunction = op('leaderFunction', range=Item, label='leaderFunction')
leaderName = op('leaderName', range=Item, label='leader name')
leadership = op('leadership', range=String, label='leadership')
leaderTitle = op('leaderTitle', range=Text, label='leader title')
leadTeam = op('leadTeam', range=Item, label='lead team')
leadYear = op('leadYear', range=String, label='lead year')
league = op('league', range=Item, label='league')
leagueManager = op('leagueManager', range=Item, label='league manager')
leftChild = op('leftChild', range=Item, label='left child')
leftTributary = op('leftTributary', range=Item, label='left tributary')
legalArrondissement = op('legalArrondissement', range=String, label='legal arrondissement')
legalArticle = op('legalArticle', range=String, label='legal article')
legislativePeriodName = op('legislativePeriodName', range=String, label='legislative period name')
legislature = op('legislature', range=Item, label='legislature')
length = op('length', range=Quantity, label='length (μ)')
lengthQuote = op('lengthQuote', range=String, label='length quote')
lengthReference = op('lengthReference', range=String, label='length reference')
lethalOnChickens = op('lethalOnChickens', range=String, label='lethal when given to chickens')
lethalOnMice = op('lethalOnMice', range=String, label='lethal when given to mice')
lethalOnRabbits = op('lethalOnRabbits', range=String, label='lethal when given to rabbits')
lethalOnRats = op('lethalOnRats', range=String, label='lethal when given to rats')
liberationDate = op('liberationDate', range=String, label='date of liberation')
libretto = op('libretto', range=String, label='libretto')
licenceLetter = op('licenceLetter', range=String, label='licence letter of a german settlement')
licenceNumber = op('licenceNumber', range=String, label='licence number')
licenceNumberLabel = op('licenceNumberLabel', range=String, label='licence number label')
licensee = op('licensee', range=String, label='licensee')
lieutenancy = op('lieutenancy', range=String, label='lieutenancy')
lieutenancyArea = op('lieutenancyArea', range=Item, label='Lieutenancy area')
lieutenant = op('lieutenant', range=Item, label='lieutenant')
lifeExpectancy = op('lifeExpectancy', range=String, label='life expectancy')
limit = op('limit', range=String, label='limit')
lineLength = op('lineLength', range=Quantity, label='line length (μ)')
linkedSpace = op('linkedSpace', range=String, label='linked space')
linkedTo = op('linkedTo', range=Item, label='linked to')
littlePoolRecord = op('littlePoolRecord', range=String, label='little pool record')
livingPlace = op('livingPlace', range=Item, label='livingPlace')
loadLimit = op('loadLimit', range=Quantity, label='load limit (g)')
locality = op('locality', range=String, label='locality of a switzerland settlement')
localization = op('localization', range=String, label='localization of the island')
localizationThumbnailCaption = op('localizationThumbnailCaption', range=String, label='legend thumbnail localization')
localPhonePrefix = op('localPhonePrefix', range=Quantity, label='local phone prefix')
locatedInArea = op('locatedInArea', range=Item, label='located in area')
location = op('location', range=Item, label='location')
locationCity = op('locationCity', range=Item, label='location city')
locationCountry = op('locationCountry', range=Item, label='państwo')
locationIdentifier = op('locationIdentifier', range=String, label='Location Identifier')
locationName = op('locationName', range=String, label='locationName')
locomotive = op('locomotive', range=Item, label='locomotive')
locusSupplementaryData = op('locusSupplementaryData', range=String, label='locus supplementary data')
logo = op('logo', range=String, label='logo')
longDistancePisteKilometre = op('longDistancePisteKilometre', range=Quantity, label='long distance piste kilometre (μ)')
longDistancePisteNumber = op('longDistancePisteNumber', range=Quantity, label='long distance piste number')
longName = op('longName', range=Text, label='longName')
longtype = op('longtype', range=String, label='longtype')
lowerAge = op('lowerAge', range=Quantity, label='lower age')
lowerEarthOrbitPayload = op('lowerEarthOrbitPayload', range=Quantity, label='lower earth orbit payload (g)')
lowest = op('lowest', range=String, label='lowest')
lowestAltitude = op('lowestAltitude', range=Item, label='lowest altitude')
lowestMountain = op('lowestMountain', range=Item, label='lowest mountain')
lowestPlace = op('lowestPlace', range=Item, label='lowest place')
lowestPoint = op('lowestPoint', range=Item, label='lowest point')
lowestRegion = op('lowestRegion', range=Item, label='lowest region')
lowestState = op('lowestState', range=Item, label='lowest state')
lunarEvaTime = op('lunarEvaTime', range=Quantity, label='lunar EVA time (s)')
lunarLandingSite = op('lunarLandingSite', range=String, label='lunar landing site')
lunarModule = op('lunarModule', range=String, label='lunar module')
lunarOrbitTime = op('lunarOrbitTime', range=Quantity, label='lunar orbit time (s)')
lunarRover = op('lunarRover', range=Item, label='lunar rover')
lunarSampleMass = op('lunarSampleMass', range=Quantity, label='lunar sample mass (g)')
lunarSurfaceTime = op('lunarSurfaceTime', range=Quantity, label='lunar surface time (s)')
lymph = op('lymph', range=Item, label='lymph')
lyrics = op('lyrics', range=Item, label='lyrics')
magazine = op('magazine', range=Item, label='magazine')
maidenFlight = op('maidenFlight', range=Time, label='maiden flight')
maidenFlightRocket = op('maidenFlightRocket', range=Item, label='maiden flight rocket')
maidenVoyage = op('maidenVoyage', range=Time, label='maiden voyage')
mainArtist = op('mainArtist', range=Item, label='main artist')
mainBuilding = op('mainBuilding', range=String, label='main building')
mainCharacter = op('mainCharacter', range=Item, label='main character')
mainFamilyBranch = op('mainFamilyBranch', range=Item, label='main branch')
mainIsland = op('mainIsland', range=Item, label='main island')
mainIslands = op('mainIslands', range=String, label='main islands')
mainspan = op('mainspan', range=Quantity, label='mainspan (μ)')
majorIsland = op('majorIsland', range=Item, label='major island')
majorityFloorLeader = op('majorityFloorLeader', range=Quantity, label='majority floor leader')
majorityLeader = op('majorityLeader', range=Quantity, label='majority leader')
makeupArtist = op('makeupArtist', range=Item, label='makeup artist')
managementCountry = op('managementCountry', range=Item, label='management country')
managementElevation = op('managementElevation', range=Quantity, label='management elevation (μ)')
managementMountain = op('managementMountain', range=Item, label='management mountain')
managementPlace = op('managementPlace', range=Item, label='management place')
managementRegion = op('managementRegion', range=Item, label='management region')
manager = op('manager', range=Item, label='manager')
managerClub = op('managerClub', range=Item, label='manager club')
managerTitle = op('managerTitle', range=String, label='manager title')
managerYears = op('managerYears', range=Time, label='manager years')
managerYearsEndYear = op('managerYearsEndYear', range=Time, label='manager years end year')
managerYearsStartYear = op('managerYearsStartYear', range=Time, label='manager years start year')
managingEditor = op('managingEditor', range=Item, label='managing editor')
mandate = op('mandate', range=String, label='political mandate')
manufactory = op('manufactory', range=Item, label='manufactory')
manufacturer = op('manufacturer', range=Item, label='manufacturer')
mapCaption = op('mapCaption', range=String, label='map caption')
mapDescription = op('mapDescription', range=String, label='map description')
march = op('march', range=Item, label='march')
marketCapitalisation = op('marketCapitalisation', range=Quantity, label='market capitalisation ($)')
mascot = op('mascot', range=String, label='mascot')
mass = op('mass', range=Quantity, label='mass (g)')
massif = op('massif', range=Item, label='massif')
matchPoint = op('matchPoint', range=String, label='match point')
max = op('max', range=Quantity, label='max')
maxAbsoluteMagnitude = op('maxAbsoluteMagnitude', range=Quantity, label='maximum absolute magnitude')
maxApparentMagnitude = op('maxApparentMagnitude', range=Quantity, label='maximum apparent magnitude')
maximumArea = op('maximumArea', range=String, label='maximum area')
maximumAreaQuote = op('maximumAreaQuote', range=String, label='maximum area quote')
maximumBoatBeam = op('maximumBoatBeam', range=Quantity, label='maximum boat beam (μ)')
maximumBoatLength = op('maximumBoatLength', range=Quantity, label='maximum boat length (μ)')
maximumDepth = op('maximumDepth', range=Quantity, label='maximum depth (μ)')
maximumDepthQuote = op('maximumDepthQuote', range=String, label='maximum depth quote')
maximumDischarge = op('maximumDischarge', range=Quantity, label='maximum discharge (m³/s)')
maximumElevation = op('maximumElevation', range=Quantity, label='maximum elevation (μ)')
maximumInclination = op('maximumInclination', range=Quantity, label='maximum inclination')
maximumTemperature = op('maximumTemperature', range=Quantity, label='maximum temperature (K)')
maxTime = op('maxTime', range=Quantity, label='maximum preparation time (s)')
mayor = op('mayor', range=Item, label='mayor')
mayorArticle = op('mayorArticle', range=String, label='mayor article')
mayorCouncillor = op('mayorCouncillor', range=String, label='mayor councillor')
mayorFunction = op('mayorFunction', range=String, label='mayor function of a switzerland settlement')
mayorMandate = op('mayorMandate', range=String, label='mayorMandate')
mayorTitle = op('mayorTitle', range=Text, label='mayor title of a hungarian settlement')
mbaId = op('mbaId', range=String, label='MBA Id')
meaning = op('meaning', range=String, label='meaning')
meanRadius = op('meanRadius', range=Quantity, label='mean radius (μ)')
meanTemperature = op('meanTemperature', range=Quantity, label='mean temperature (K)')
measurements = op('measurements', range=String, label='measurements')
medalist = op('medalist', range=Item, label='medalist')
mediaItem = op('mediaItem', range=Item, label='media item')
medicalSpecialty = op('medicalSpecialty', range=Item, label='medical specialty')
medlinePlus = op('medlinePlus', range=String, label='MedlinePlus')
meetingBuilding = op('meetingBuilding', range=Item, label='meeting building')
meetingCity = op('meetingCity', range=Item, label='meeting city')
meetingRoad = op('meetingRoad', range=Item, label='meeting road')
meltingPoint = op('meltingPoint', range=Quantity, label='melting point (K)')
member = op('member', range=String, label='member')
memberOfParliament = op('memberOfParliament', range=Item, label='Member of Parliament')
membership = op('membership', range=Text, label='membership')
membershipAsOf = op('membershipAsOf', range=Time, label='date membership established')
mentor = op('mentor', range=Item, label='mentor')
mergedSettlement = op('mergedSettlement', range=Item, label='merged settlement')
mergedWith = op('mergedWith', range=Item, label='merged with')
mergerDate = op('mergerDate', range=Time, label='merger date')
meshId = op('meshId', range=String, label='MeSH ID')
meshName = op('meshName', range=Text, label='MeSH name')
meshNumber = op('meshNumber', range=String, label='MeSH number')
messierName = op('messierName', range=String, label='Messier name')
metropolitanBorough = op('metropolitanBorough', range=Item, label='metropolitan borough')
mgiid = op('mgiid', range=String, label='mgiid')
militaryBranch = op('militaryBranch', range=Item, label='military branch')
militaryCommand = op('militaryCommand', range=String, label='military command')
militaryFunction = op('militaryFunction', range=String, label='military function')
militaryGovernment = op('militaryGovernment', range=String, label='military government')
militaryService = op('militaryService', range=Item, label='military service')
militaryUnit = op('militaryUnit', range=Item, label='military unit')
militaryUnitSize = op('militaryUnitSize', range=String, label='military unit size')
millsCodeBE = op('millsCodeBE', range=String, label='mill code BE')
millsCodeDutch = op('millsCodeDutch', range=String, label='mill code NL')
millsCodeNL = op('millsCodeNL', range=String, label='mill code NL')
millsCodeNLVerdwenen = op('millsCodeNLVerdwenen', range=String, label='mill dissapeared code NL')
millsCodeNLWindmotoren = op('millsCodeNLWindmotoren', range=String, label='millsCodeNLWindmotoren')
millSpan = op('millSpan', range=Quantity, label='mill span (μ)')
min = op('min', range=Quantity, label='min')
minimumArea = op('minimumArea', range=String, label='minimum area')
minimumAreaQuote = op('minimumAreaQuote', range=String, label='minimum area quote')
minimumDischarge = op('minimumDischarge', range=Quantity, label='minimum discharge (m³/s)')
minimumElevation = op('minimumElevation', range=Quantity, label='minimum elevation (μ)')
minimumInclination = op('minimumInclination', range=Quantity, label='minimum inclination')
minimumTemperature = op('minimumTemperature', range=Quantity, label='minimum temperature (K)')
minister = op('minister', range=Item, label='minister')
minority = op('minority', range=Item, label='minority')
minorityFloorLeader = op('minorityFloorLeader', range=Quantity, label='minority floor leader')
minorityLeader = op('minorityLeader', range=Quantity, label='minority leader')
minTime = op('minTime', range=Quantity, label='minimum preparation time (s)')
mirDockings = op('mirDockings', range=Quantity, label='mir dockings')
mission = op('mission', range=Item, label='mission')
missionDuration = op('missionDuration', range=Quantity, label='mission duration (s)')
missions = op('missions', range=Quantity, label='missions')
model = op('model', range=String, label='model')
modelEndDate = op('modelEndDate', range=Time, label='model end date')
modelEndYear = op('modelEndYear', range=Time, label='model end year')
modelLineVehicle = op('modelLineVehicle', range=String, label='type series')
modelStartDate = op('modelStartDate', range=Time, label='model start date')
modelStartYear = op('modelStartYear', range=Time, label='model start year')
moderna = op('moderna', range=String, label='Moderna')
modernaCumul = op('modernaCumul', range=Quantity, label='ModernaCumulativeDoses')
molarMass = op('molarMass', range=Quantity, label='molar mass')
molecularWeight = op('molecularWeight', range=Quantity, label='molecular weight')
monarch = op('monarch', range=Item, label='monarch')
month = op('month', range=String, label='month')
mood = op('mood', range=String, label='mood')
mostDownPoint = op('mostDownPoint', range=Item, label='most down point of a norwegian settlement')
mostSuccessfulPlayer = op('mostSuccessfulPlayer', range=Item, label='most successful player')
mother = op('mother', range=Item, label='mother')
motive = op('motive', range=String, label='motive')
motto = op('motto', range=String, label='motto')
mount = op('mount', range=String, label='mount')
mountainRange = op('mountainRange', range=Item, label='mountain range')
mouthCountry = op('mouthCountry', range=Item, label='mouth country')
mouthDistrict = op('mouthDistrict', range=Item, label='mouth district')
mouthElevation = op('mouthElevation', range=Quantity, label='mouth elevation (μ)')
mouthMountain = op('mouthMountain', range=Item, label='mouth mountain')
mouthPlace = op('mouthPlace', range=Item, label='mouth place')
mouthRegion = op('mouthRegion', range=Item, label='mouth region')
mouthState = op('mouthState', range=Item, label='mouth state')
movie = op('movie', range=Item, label='movie')
mukhtar = op('mukhtar', range=String, label='mukthar of a lebanon settlement')
municipality = op('municipality', range=Item, label='municipality')
municipalityAbsorbedBy = op('municipalityAbsorbedBy', range=Item, label='absorbed by')
municipalityCode = op('municipalityCode', range=String, label='municipality code')
municipalityRenamedTo = op('municipalityRenamedTo', range=String, label='a municipality\'s new name')
municipalityType = op('municipalityType', range=String, label='type of municipality')
museum = op('museum', range=Item, label='museum')
musicalArtist = op('musicalArtist', range=Item, label='musical artist')
musicalBand = op('musicalBand', range=Item, label='musical band')
musicalKey = op('musicalKey', range=String, label='musical key')
musicBand = op('musicBand', range=Item, label='Music Band')
musicBrainzArtistId = op('musicBrainzArtistId', range=String, label='MusicBrainz artist id')
musicBy = op('musicBy', range=Item, label='music by')
musicComposer = op('musicComposer', range=Item, label='music composer')
musicFormat = op('musicFormat', range=String, label='musicFormat')
musicFusionGenre = op('musicFusionGenre', range=Item, label='music fusion genre')
musicians = op('musicians', range=Item, label='musicians')
musicSubgenre = op('musicSubgenre', range=Item, label='music subgenre')
muteCharacterInPlay = op('muteCharacterInPlay', range=String, label='mute character in play')
mvp = op('mvp', range=String, label='mvp')
naacpImageAward = op('naacpImageAward', range=Item, label='NAACP Image Award')
name = op('name', range=Text, label='name')
nameAsOf = op('nameAsOf', range=Time, label='so named since')
nameDay = op('nameDay', range=Time, label='name day')
namedByLanguage = op('namedByLanguage', range=Item, label='named by language')
nameInCantoneseChinese = op('nameInCantoneseChinese', range=Text, label='name in Yue Chinese')
nameInHangulKorean = op('nameInHangulKorean', range=Text, label='name in Hangul-written Korean')
nameInHanjaKorean = op('nameInHanjaKorean', range=Text, label='name in Hanja-written (traditional) Korean')
nameInJapanese = op('nameInJapanese', range=Text, label='name in Japanese')
nameInMindongyuChinese = op('nameInMindongyuChinese', range=Text, label='name in Mindongyu Chinese')
nameInMinnanyuChinese = op('nameInMinnanyuChinese', range=Text, label='name in Minnanyu Chinese')
nameInPinyinChinese = op('nameInPinyinChinese', range=Text, label='name in Pinyin Chinese')
nameInSimplifiedChinese = op('nameInSimplifiedChinese', range=Text, label='name in Simplified Chinese')
nameInTraditionalChinese = op('nameInTraditionalChinese', range=Text, label='name in Traditional Chinese')
nameInWadeGilesChinese = op('nameInWadeGilesChinese', range=Text, label='name in the Wade-Giles transscription of Chinese')
names = op('names', range=Text, label='names')
narrator = op('narrator', range=Item, label='narrator')
nation = op('nation', range=String, label='nation')
nationalChampionship = op('nationalChampionship', range=String, label='national championship')
nationalFilmAward = op('nationalFilmAward', range=Item, label='National Film Award')
nationality = op('nationality', range=Item, label='nationality')
nationalRanking = op('nationalRanking', range=Quantity, label='national ranking')
nationalTeam = op('nationalTeam', range=Item, label='national team')
nationalTeamMatchPoint = op('nationalTeamMatchPoint', range=String, label='national team match point')
nationalTeamYear = op('nationalTeamYear', range=String, label='national team year')
nationalTopographicSystemMapNumber = op('nationalTopographicSystemMapNumber', range=String, label='National Topographic System map number')
nationalTournament = op('nationalTournament', range=Item, label='National tournament')
nationalTournamentBronze = op('nationalTournamentBronze', range=Quantity, label='national tournament bronze')
nationalTournamentGold = op('nationalTournamentGold', range=Quantity, label='national tournament gold')
nationalTournamentSilver = op('nationalTournamentSilver', range=Quantity, label='national tournament silver')
nationalYears = op('nationalYears', range=Time, label='national years')
nbRevPerMonth = op('nbRevPerMonth', range=IRI, label='Number of revision per month')
nbRevPerYear = op('nbRevPerYear', range=IRI, label='Number of revision per year')
nbUniqueContrib = op('nbUniqueContrib', range=Quantity, label='Number of unique contributors')
ncaaSeason = op('ncaaSeason', range=String, label='ncaa season')
ncaaTeam = op('ncaaTeam', range=Item, label='ncaa team')
ncbhof = op('ncbhof', range=String, label='ncbhof')
nciId = op('nciId', range=String, label='NCI')
ndlId = op('ndlId', range=String, label='NDL id')
nearestCity = op('nearestCity', range=Item, label='nearest city')
neighboringMunicipality = op('neighboringMunicipality', range=Item, label='neighboring municipality')
neighbourConstellations = op('neighbourConstellations', range=String, label='neighbour constellations')
neighbourhood = op('neighbourhood', range=String, label='neighbourhood of a hungarian settlement')
neighbourRegion = op('neighbourRegion', range=String, label='neighbour region')
nerve = op('nerve', range=Item, label='nerve')
netIncome = op('netIncome', range=Quantity, label='net income ($)')
network = op('network', range=Item, label='network')
networth = op('networth', range=Quantity, label='networth ($)')
newspaper = op('newspaper', range=Item, label='newspaper')
nextEntity = op('nextEntity', range=Item, label='next entity')
nextEvent = op('nextEvent', range=Item, label='next event')
nextMission = op('nextMission', range=Item, label='next mission')
nextTrackNumber = op('nextTrackNumber', range=Quantity, label='number of the next track')
nflCode = op('nflCode', range=String, label='nfl code')
nflSeason = op('nflSeason', range=String, label='nfl season')
nflTeam = op('nflTeam', range=Item, label='nfl team')
ngcName = op('ngcName', range=String, label='NGC name')
nisCode = op('nisCode', range=String, label='NIS code')
nlaId = op('nlaId', range=String, label='NLA Id')
nndbId = op('nndbId', range=String, label='NNDB id')
nobelLaureates = op('nobelLaureates', range=Item, label='nobel laureates')
noContest = op('noContest', range=Quantity, label='no contest')
nominee = op('nominee', range=Item, label='nominee')
nonProfessionalCareer = op('nonProfessionalCareer', range=String, label='non professional career')
nord = op('nord', range=String, label='NORD')
northEastPlace = op('northEastPlace', range=Item, label='north-east place')
northPlace = op('northPlace', range=Item, label='north place')
northWestPlace = op('northWestPlace', range=Item, label='north-west place')
notableCommander = op('notableCommander', range=Item, label='notable commander')
notableFeatures = op('notableFeatures', range=String, label='notable features')
notableStudent = op('notableStudent', range=Item, label='notable student')
notableWork = op('notableWork', range=Item, label='notable work')
note = op('note', range=String, label='note')
noteOnPlaceOfBurial = op('noteOnPlaceOfBurial', range=String, label='note on place of burial')
noteOnRestingPlace = op('noteOnRestingPlace', range=String, label='note on resting place')
notes = op('notes', range=String, label='notes')
notifyDate = op('notifyDate', range=Time, label='notify date')
notSolubleIn = op('notSolubleIn', range=Item, label='not soluble in')
novel = op('novel', range=Item, label='novel')
nrhpReferenceNumber = op('nrhpReferenceNumber', range=String, label='NRHP Reference Number')
nssdcId = op('nssdcId', range=String, label='NSSDC ID')
number = op('number', range=Quantity, label='number')
numberBuilt = op('numberBuilt', range=Quantity, label='number built')
numberOfAcademicStaff = op('numberOfAcademicStaff', range=Quantity, label='number of academic staff')
numberOfAlbums = op('numberOfAlbums', range=Quantity, label='number of albums')
numberOfArrondissement = op('numberOfArrondissement', range=Quantity, label='number of arrondissement')
numberOfBombs = op('numberOfBombs', range=Quantity, label='number of bombs')
numberOfBronzeMedalsWon = op('numberOfBronzeMedalsWon', range=Quantity, label='number of bronze medals won')
numberOfCanton = op('numberOfCanton', range=Quantity, label='number of canton')
numberOfCantons = op('numberOfCantons', range=Quantity, label='Number Of Cantons')
numberOfCapitalDeputies = op('numberOfCapitalDeputies', range=Quantity, label='Number Of Capital Deputies')
numberOfCity = op('numberOfCity', range=Quantity, label='number of contries inside en continent')
numberOfClasses = op('numberOfClasses', range=Quantity, label='numberOfClasses')
numberOfClassesWithResource = op('numberOfClassesWithResource', range=Quantity, label='numberOfClassesWithResource')
numberOfClubs = op('numberOfClubs', range=Quantity, label='number of clubs')
numberOfCollectionItems = op('numberOfCollectionItems', range=Quantity, label='number of items in collection')
numberOfCompetitors = op('numberOfCompetitors', range=Quantity, label='number of competitors')
numberOfCounties = op('numberOfCounties', range=Quantity, label='number of counties')
numberOfCountries = op('numberOfCountries', range=Quantity, label='number of countries')
numberOfCrew = op('numberOfCrew', range=Quantity, label='number of crew')
numberOfDeaths = op('numberOfDeaths', range=String, label='number of deaths')
numberOfDependency = op('numberOfDependency', range=Quantity, label='number of dependency')
numberOfDisambiguates = op('numberOfDisambiguates', range=Quantity, label='numberOfDisambiguates')
numberOfDistrict = op('numberOfDistrict', range=Quantity, label='number of district')
numberOfDistricts = op('numberOfDistricts', range=Quantity, label='number of districts')
numberOfDoctoralStudents = op('numberOfDoctoralStudents', range=Quantity, label='number of doctoral students')
numberOfDoors = op('numberOfDoors', range=Quantity, label='number of doors')
numberOfEmployees = op('numberOfEmployees', range=Quantity, label='number of employees')
numberOfEntrances = op('numberOfEntrances', range=Quantity, label='number of entrances')
numberOfEpisodes = op('numberOfEpisodes', range=Quantity, label='number of episodes')
numberOfEtoilesMichelin = op('numberOfEtoilesMichelin', range=Quantity, label='number of étoiles Michelin')
numberOfFederalDeputies = op('numberOfFederalDeputies', range=Quantity, label='Number Of Federal Deputies')
numberOfFilms = op('numberOfFilms', range=Quantity, label='number of films')
numberOfGoals = op('numberOfGoals', range=Quantity, label='number of goals scored')
numberOfGoldMedalsWon = op('numberOfGoldMedalsWon', range=Quantity, label='number of gold medals won')
numberOfGraduateStudents = op('numberOfGraduateStudents', range=Quantity, label='number of graduate students')
numberOfGraves = op('numberOfGraves', range=String, label='number of graves')
numberOfHoles = op('numberOfHoles', range=Quantity, label='number of holes')
numberOfHouses = op('numberOfHouses', range=String, label='number of houses present)')
numberOfIndegree = op('numberOfIndegree', range=Quantity, label='number of all indegrees in dbpedia (same ourdegrees are counting repeatedly)')
numberOfIntercommunality = op('numberOfIntercommunality', range=Quantity, label='number of intercommunality')
numberOfIsland = op('numberOfIsland', range=String, label='number of islands')
numberOfIslands = op('numberOfIslands', range=Quantity, label='number of islands')
numberOfLanes = op('numberOfLanes', range=Quantity, label='number of lanes')
numberOfLaps = op('numberOfLaps', range=Quantity, label='number of laps')
numberOfLaunches = op('numberOfLaunches', range=Quantity, label='number of launches')
numberOfLawyers = op('numberOfLawyers', range=Quantity, label='number of lawyers')
numberOfLifts = op('numberOfLifts', range=Quantity, label='number of lifts')
numberOfLines = op('numberOfLines', range=Quantity, label='number of lines')
numberOfLiveAlbums = op('numberOfLiveAlbums', range=Quantity, label='number of live albums')
numberOfLocations = op('numberOfLocations', range=Quantity, label='number of locations')
numberOfMatches = op('numberOfMatches', range=Quantity, label='number of matches or caps')
numberOfMembers = op('numberOfMembers', range=Quantity, label='number of members')
numberOfMembersAsOf = op('numberOfMembersAsOf', range=Time, label='number of members as of')
numberOfMinistries = op('numberOfMinistries', range=Quantity, label='number of ministries')
numberOfMunicipalities = op('numberOfMunicipalities', range=Quantity, label='Number Of Municipalities')
numberOfMusicalArtistEntities = op('numberOfMusicalArtistEntities', range=Quantity, label='number of MuscialArtist class (entities) in DBpedia')
numberOfMusicalArtistInstrument = op('numberOfMusicalArtistInstrument', range=Quantity, label='number of all MuscialArtist playing the instrument')
numberOfMusicalArtistStyle = op('numberOfMusicalArtistStyle', range=Quantity, label='number of all MuscialArtist playing the style')
numberOfNeighbourhood = op('numberOfNeighbourhood', range=Quantity, label='number of neighbourhood')
numberOfNewlyIntroducedSports = op('numberOfNewlyIntroducedSports', range=Quantity, label='number of newly introduced sports')
numberOfOffices = op('numberOfOffices', range=Quantity, label='number of offices')
numberOfOfficials = op('numberOfOfficials', range=Quantity, label='number of officials')
numberOfOrbits = op('numberOfOrbits', range=Quantity, label='number of orbits')
numberOfOutdegree = op('numberOfOutdegree', range=Quantity, label='numberOfOutdegree')
numberOfPads = op('numberOfPads', range=Quantity, label='number of pads')
numberOfPages = op('numberOfPages', range=Quantity, label='number of pages')
numberOfParkingSpaces = op('numberOfParkingSpaces', range=Quantity, label='number of parking spaces')
numberOfParticipatingAthletes = op('numberOfParticipatingAthletes', range=Quantity, label='number of participating athletes')
numberOfParticipatingFemaleAthletes = op('numberOfParticipatingFemaleAthletes', range=Quantity, label='number of participating female athletes')
numberOfParticipatingMaleAthletes = op('numberOfParticipatingMaleAthletes', range=Quantity, label='number of participating male athletes')
numberOfParticipatingNations = op('numberOfParticipatingNations', range=Quantity, label='number of participating nations')
numberOfPassengers = op('numberOfPassengers', range=Quantity, label='number of passengers')
numberOfPeopleAttending = op('numberOfPeopleAttending', range=Quantity, label='number of people attending')
numberOfPeopleLicensed = op('numberOfPeopleLicensed', range=Quantity, label='number of licensed')
numberOfPersonBornInPlace = op('numberOfPersonBornInPlace', range=Quantity, label='number of entities of Person class born in the place')
numberOfPersonEntities = op('numberOfPersonEntities', range=Quantity, label='number of Person class (entities) in DBpedia')
numberOfPersonFromUniversity = op('numberOfPersonFromUniversity', range=Quantity, label='number of entities of Person class who graduated from the university')
numberOfPersonInOccupation = op('numberOfPersonInOccupation', range=Quantity, label='number of person in one occupation')
numberOfPiersInWater = op('numberOfPiersInWater', range=Quantity, label='number of piers in water')
numberOfPixels = op('numberOfPixels', range=Quantity, label='number of pixels (millions)')
numberOfPlatformLevels = op('numberOfPlatformLevels', range=Quantity, label='number of platform levels')
numberOfPlayers = op('numberOfPlayers', range=Quantity, label='number of players')
numberOfPostgraduateStudents = op('numberOfPostgraduateStudents', range=Quantity, label='number of postgraduate students')
numberOfPredicates = op('numberOfPredicates', range=Quantity, label='numberOfPredicates')
numberOfProfessionals = op('numberOfProfessionals', range=Quantity, label='number of professionals')
numberOfProperties = op('numberOfProperties', range=Quantity, label='numberOfProperties')
numberOfPropertiesUsed = op('numberOfPropertiesUsed', range=Quantity, label='numberOfPropertiesUsed')
numberOfReactors = op('numberOfReactors', range=Quantity, label='number of reactors')
numberOfRedirectedResource = op('numberOfRedirectedResource', range=Quantity, label='numberOfRedirectedResource')
numberOfResource = op('numberOfResource', range=Quantity, label='numberOfResource')
numberOfResourceOfClass = op('numberOfResourceOfClass', range=Quantity, label='number of all resource / entities of a class')
numberOfResourceOfType = op('numberOfResourceOfType', range=Quantity, label='number of resource / entities for concrete type of subject')
numberOfResourceWithType = op('numberOfResourceWithType', range=Quantity, label='nmberOfResourceWithType')
numberOfRestaurants = op('numberOfRestaurants', range=Quantity, label='number of restaurants')
numberOfRockets = op('numberOfRockets', range=Quantity, label='number of rockets')
numberOfRooms = op('numberOfRooms', range=Quantity, label='number of rooms')
numberOfRun = op('numberOfRun', range=Quantity, label='number of run')
numberOfSeasons = op('numberOfSeasons', range=Quantity, label='number of seasons')
numberOfSeats = op('numberOfSeats', range=Quantity, label='number of seats')
numberOfSeatsInParliament = op('numberOfSeatsInParliament', range=Quantity, label='number of seats in parliament')
numberOfSettlement = op('numberOfSettlement', range=Quantity, label='number of settlement')
numberOfSettlementsInCountry = op('numberOfSettlementsInCountry', range=Quantity, label='number of entities of Settlement class in country')
numberOfSilverMedalsWon = op('numberOfSilverMedalsWon', range=Quantity, label='number of silver medals won')
numberOfSoccerPlayerInCountryRepre = op('numberOfSoccerPlayerInCountryRepre', range=Quantity, label='number of SoccerPlayers in Country Repre')
numberOfSoccerPlayersBornInPlace = op('numberOfSoccerPlayersBornInPlace', range=Quantity, label='number of SoccerPlayers born in Place')
numberOfSoccerPlayersInTeam = op('numberOfSoccerPlayersInTeam', range=Quantity, label='number of SoccerPlayers in entity of SoccerClub')
numberOfSpans = op('numberOfSpans', range=Quantity, label='number of spans')
numberOfSpeakers = op('numberOfSpeakers', range=Quantity, label='number of speakers')
numberOfSports = op('numberOfSports', range=Quantity, label='number of sports')
numberOfSportsEvents = op('numberOfSportsEvents', range=Quantity, label='number of sports events')
numberOfStaff = op('numberOfStaff', range=Quantity, label='number of staff')
numberOfStars = op('numberOfStars', range=Quantity, label='number of stars')
numberOfStateDeputies = op('numberOfStateDeputies', range=Quantity, label='Number Of State Deputies')
numberOfStations = op('numberOfStations', range=Quantity, label='number of stations')
numberOfStores = op('numberOfStores', range=Quantity, label='number of sores')
numberOfStudents = op('numberOfStudents', range=Quantity, label='number of students')
numberOfStudioAlbums = op('numberOfStudioAlbums', range=Quantity, label='number of studio albums')
numberOfSuites = op('numberOfSuites', range=Quantity, label='number of suites')
numberOfTeams = op('numberOfTeams', range=Quantity, label='number of teams')
numberOfTracks = op('numberOfTracks', range=Quantity, label='number of tracks')
numberOfTrails = op('numberOfTrails', range=Quantity, label='number of trails')
numberOfTriples = op('numberOfTriples', range=Quantity, label='numberOfTriples')
numberOfTurns = op('numberOfTurns', range=Quantity, label='number of turns')
numberOfUndergraduateStudents = op('numberOfUndergraduateStudents', range=Quantity, label='number of undergraduate students')
numberOfUniqeResources = op('numberOfUniqeResources', range=Quantity, label='numberOfUniqeResources')
numberOfUseOfProperty = op('numberOfUseOfProperty', range=Quantity, label='number of use of a property')
numberOfVehicles = op('numberOfVehicles', range=Quantity, label='number of vehicles')
numberOfVillages = op('numberOfVillages', range=Quantity, label='number of villages')
numberOfVineyards = op('numberOfVineyards', range=Quantity, label='number of vineyards')
numberOfVisitors = op('numberOfVisitors', range=Quantity, label='number of visitors')
numberOfVisitorsAsOf = op('numberOfVisitorsAsOf', range=Time, label='number of visitors as of')
numberOfVolumes = op('numberOfVolumes', range=Quantity, label='number of volumes')
numberOfVolunteers = op('numberOfVolunteers', range=Quantity, label='number of volunteers')
numberOfWineries = op('numberOfWineries', range=Quantity, label='number of wineries')
numberSold = op('numberSold', range=Quantity, label='number sold')
nutsCode = op('nutsCode', range=String, label='NUTS code')
observatory = op('observatory', range=String, label='observatory')
occupation = op('occupation', range=Item, label='occupation')
oclc = op('oclc', range=String, label='OCLC')
odor = op('odor', range=String, label='Odor')
offeredClasses = op('offeredClasses', range=String, label='offered classes')
office = op('office', range=String, label='(political) office')
officerInCharge = op('officerInCharge', range=Item, label='officer in charge')
officialLanguage = op('officialLanguage', range=Item, label='official language')
officialName = op('officialName', range=Text, label='official name')
officialOpenedBy = op('officialOpenedBy', range=Item, label='official opened by')
officialSchoolColour = op('officialSchoolColour', range=String, label='official school colour')
ofsCode = op('ofsCode', range=String, label='ofs code of a settlement')
okatoCode = op('okatoCode', range=String, label='okato code')
oldcode = op('oldcode', range=String, label='oldcode')
oldDistrict = op('oldDistrict', range=Item, label='old district')
oldName = op('oldName', range=String, label='old name')
oldProvince = op('oldProvince', range=Item, label='old province')
oldTeamCoached = op('oldTeamCoached', range=Item, label='old team coached')
olivierAward = op('olivierAward', range=Item, label='Olivier Award')
olympicGames = op('olympicGames', range=Item, label='olympic games')
olympicGamesBronze = op('olympicGamesBronze', range=Quantity, label='olympic games bronze')
olympicGamesGold = op('olympicGamesGold', range=Quantity, label='olympic games gold')
olympicGamesSilver = op('olympicGamesSilver', range=Quantity, label='olympic games silver')
olympicGamesWins = op('olympicGamesWins', range=String, label='olympic games wins')
olympicOathSwornBy = op('olympicOathSwornBy', range=Item, label='olympic oath sworn by')
olympicOathSwornByAthlete = op('olympicOathSwornByAthlete', range=Item, label='olympic oath sworn by athlete')
olympicOathSwornByJudge = op('olympicOathSwornByJudge', range=Item, label='olympic oath sworn by judge')
omim = op('omim', range=Quantity, label='OMIM id')
onChromosome = op('onChromosome', range=Quantity, label='on chromosome')
ons = op('ons', range=Quantity, label='ONS ID (Office national des statistiques) Algeria')
openAccessContent = op('openAccessContent', range=String, label='open access content')
openingDate = op('openingDate', range=Time, label='opening date')
openingFilm = op('openingFilm', range=Item, label='opening film')
openingTheme = op('openingTheme', range=Item, label='opening theme')
openingYear = op('openingYear', range=Time, label='opening year')
operatingIncome = op('operatingIncome', range=Quantity, label='operating income ($)')
opponent = op('opponent', range=Item, label='opponent')
orbitalEccentricity = op('orbitalEccentricity', range=Quantity, label='orbital eccentricity')
orbitalFlights = op('orbitalFlights', range=Quantity, label='orbital flights')
orbitalInclination = op('orbitalInclination', range=Quantity, label='orbital inclination')
orbitalPeriod = op('orbitalPeriod', range=Quantity, label='orbital period (s)')
orbits = op('orbits', range=Quantity, label='orbits')
orcidId = op('orcidId', range=String, label='ORCID Id')
orderDate = op('orderDate', range=Time, label='order date')
orderInOffice = op('orderInOffice', range=String, label='order in office')
ordination = op('ordination', range=Time, label='Ordination')
organ = op('organ', range=Item, label='organ')
organisation = op('organisation', range=Item, label='organisation')
organisationMember = op('organisationMember', range=Item, label='organisation member')
organSystem = op('organSystem', range=Item, label='organ system')
orientation = op('orientation', range=String, label='orientation')
origin = op('origin', range=Item, label='origin')
originalDanseCompetition = op('originalDanseCompetition', range=String, label='original danse competititon')
originalDanseScore = op('originalDanseScore', range=String, label='original danse score')
originalEndPoint = op('originalEndPoint', range=Item, label='original end point')
originalLanguage = op('originalLanguage', range=Item, label='original language')
originallyUsedFor = op('originallyUsedFor', range=String, label='originally used for')
originalMaximumBoatBeam = op('originalMaximumBoatBeam', range=Quantity, label='original maximum boat beam (μ)')
originalMaximumBoatLength = op('originalMaximumBoatLength', range=Quantity, label='original maximum boat length (μ)')
originalName = op('originalName', range=Text, label='original name')
originalNotLatinTitle = op('originalNotLatinTitle', range=Text, label='titre original non latin')
originalStartPoint = op('originalStartPoint', range=Item, label='original start point')
originalTitle = op('originalTitle', range=Text, label='original title')
origo = op('origo', range=Item, label='origo')
orpha = op('orpha', range=String, label='ORPHA')
orthologousGene = op('orthologousGene', range=Item, label='Orthologous Gene')
other = op('other', range=Quantity, label='other')
otherActivity = op('otherActivity', range=String, label='other activity')
otherAppearances = op('otherAppearances', range=Item, label='other appearances')
otherChannel = op('otherChannel', range=String, label='other channel')
otherFamilyBranch = op('otherFamilyBranch', range=Item, label='other branch')
otherInformation = op('otherInformation', range=String, label='other information of a settlement')
otherLanguage = op('otherLanguage', range=String, label='other language of a settlement')
otherMedia = op('otherMedia', range=Item, label='other media')
otherName = op('otherName', range=Text, label='other name')
otherOccupation = op('otherOccupation', range=Item, label='other occupation')
otherParty = op('otherParty', range=Item, label='other party')
otherServingLines = op('otherServingLines', range=String, label='other serving lines')
otherSportsExperience = op('otherSportsExperience', range=Item, label='otherSportsExperience')
otherWins = op('otherWins', range=Quantity, label='other wins')
otherWorks = op('otherWorks', range=Item, label='other works')
outflow = op('outflow', range=Item, label='outflow')
output = op('output', range=Quantity, label='output')
outputHistory = op('outputHistory', range=String, label='output history')
outskirts = op('outskirts', range=String, label='outskirts')
overallRecord = op('overallRecord', range=String, label='overall record')
oversight = op('oversight', range=String, label='oversight')
owner = op('owner', range=Item, label='owner')
owningCompany = op('owningCompany', range=Item, label='owning company')
owningOrganisation = op('owningOrganisation', range=Item, label='owning organisation')
owns = op('owns', range=Item, label='owns')
painter = op('painter', range=Item, label='painter')
pandemic = op('pandemic', range=Item, label='Pandemic')
pandemicDeaths = op('pandemicDeaths', range=Quantity, label='Deaths')
parent = op('parent', range=Item, label='parent')
parentCompany = op('parentCompany', range=Item, label='parent company')
parentMountainPeak = op('parentMountainPeak', range=Item, label='parent mountain peak')
parentOrganisation = op('parentOrganisation', range=Item, label='parent organisation')
parish = op('parish', range=Item, label='parish')
parkingInformation = op('parkingInformation', range=String, label='parking information')
parkingLotsCars = op('parkingLotsCars', range=Quantity, label='number of parking lots for cars')
parkingLotsTrucks = op('parkingLotsTrucks', range=Quantity, label='number of parking lots for trucks')
parliament = op('parliament', range=Item, label='parliament')
parliamentaryGroup = op('parliamentaryGroup', range=String, label='parliamentary group')
parliamentType = op('parliamentType', range=String, label='parliament type')
partialFailedLaunches = op('partialFailedLaunches', range=Quantity, label='partial failed launches')
participant = op('participant', range=String, label='participant')
participatingIn = op('participatingIn', range=Item, label='participates/participated in')
particularSign = op('particularSign', range=String, label='particular sign')
partitionCoefficient = op('partitionCoefficient', range=Quantity, label='Partition coefficient')
partner = op('partner', range=Item, label='partner')
party = op('party', range=Item, label='party')
partyNumber = op('partyNumber', range=Quantity, label='party number')
passengersPerDay = op('passengersPerDay', range=Quantity, label='passengers per day')
passengersPerYear = op('passengersPerYear', range=Quantity, label='passengers per year')
passengersUsedSystem = op('passengersUsedSystem', range=String, label='passengers used system')
pastMember = op('pastMember', range=Item, label='past member')
pastor = op('pastor', range=Item, label='pastor')
patron = op('patron', range=Item, label='patron')
patronSaint = op('patronSaint', range=Item, label='patron saint')
pccSecretary = op('pccSecretary', range=String, label='pcc secretary')
pdb = op('pdb', range=String, label='PDB ID')
peabodyAward = op('peabodyAward', range=Item, label='Peabody Award')
penaltiesTeamA = op('penaltiesTeamA', range=String, label='Penalties Team A')
penaltiesTeamB = op('penaltiesTeamB', range=String, label='Penalties Team B')
penaltyScore = op('penaltyScore', range=Quantity, label='penalty score')
pendamicDeaths = op('pendamicDeaths', range=Quantity, label='Deaths')
penisLength = op('penisLength', range=String, label='penis length')
peopleFullyVaccinated = op('peopleFullyVaccinated', range=Item, label='People Fully Vaccinated')
peopleName = op('peopleName', range=Text, label='peopleName')
peopleVaccinated = op('peopleVaccinated', range=Item, label='People Vaccinated')
peopleVaccinatedPerHundred = op('peopleVaccinatedPerHundred', range=Item, label='People Vaccinated Per Hundred')
perCapitaIncome = op('perCapitaIncome', range=Quantity, label='per capita income ($)')
perCapitaIncomeAsOf = op('perCapitaIncomeAsOf', range=Time, label='per capita income as of')
perCapitaIncomeRank = op('perCapitaIncomeRank', range=String, label='per capital income rank')
percentageAlcohol = op('percentageAlcohol', range=Quantity, label='percentage of alcohol')
percentageFat = op('percentageFat', range=Quantity, label='percentage of fat')
percentageLiteracyMen = op('percentageLiteracyMen', range=Quantity, label='percentage of a place\'s male population that is literate, degree of analphabetism')
percentageLiteracyWomen = op('percentageLiteracyWomen', range=Quantity, label='percentage of a place\'s female population that is literate, degree of analphabetism')
percentageLiterate = op('percentageLiterate', range=Quantity, label='percentage of a place\'s population that is literate, degree of analphabetism')
percentageOfAreaWater = op('percentageOfAreaWater', range=Quantity, label='percentage of area water')
performer = op('performer', range=Item, label='performer')
periapsis = op('periapsis', range=Quantity, label='periapsis (μ)')
perifocus = op('perifocus', range=String, label='perifocus')
perimeter = op('perimeter', range=Quantity, label='perimeter (μ)')
perpetrator = op('perpetrator', range=Item, label='perpetrator')
person = op('person', range=Item, label='person')
personFunction = op('personFunction', range=Item, label='person function')
personName = op('personName', range=String, label='personName')
personsFirstDosesCumul = op('personsFirstDosesCumul', range=Quantity, label='PersonsFirstDosesCumul')
personsFullDosesCumul = op('personsFullDosesCumul', range=Quantity, label='PersonsFullDosesCumul')
pfizer = op('pfizer', range=String, label='Pfizer')
pfizerCumul = op('pfizerCumul', range=Quantity, label='PfizerCumulativeDoses')
phonePrefix = op('phonePrefix', range=Quantity, label='phone prefix')
phonePrefixLabel = op('phonePrefixLabel', range=Text, label='phone prefix label of a settlement')
photographer = op('photographer', range=Item, label='photographer')
picturesCommonsCategory = op('picturesCommonsCategory', range=String, label='pictures Commons category')
piercing = op('piercing', range=String, label='piercing')
pisciculturalPopulation = op('pisciculturalPopulation', range=String, label='piscicultural population')
pistonStroke = op('pistonStroke', range=Quantity, label='piston stroke (μ)')
place = op('place', range=Item, label='Relates an entity to the populated place in which it is located.')
placeOfBurial = op('placeOfBurial', range=Item, label='place of burial')
placeOfWorship = op('placeOfWorship', range=Item, label='place of worship')
plant = op('plant', range=Item, label='plant')
playerInTeam = op('playerInTeam', range=Item, label='player in team')
playerStatus = op('playerStatus', range=String, label='player status')
playingTime = op('playingTime', range=Quantity, label='playing time (s)')
plays = op('plays', range=String, label='plays')
pluviometry = op('pluviometry', range=String, label='pluviometry')
podium = op('podium', range=Quantity, label='podium')
podiums = op('podiums', range=Quantity, label='podiums')
pole = op('pole', range=String, label='pole')
poleDriver = op('poleDriver', range=Item, label='pole driver')
poleDriverCountry = op('poleDriverCountry', range=Item, label='pole driver country')
poleDriverTeam = op('poleDriverTeam', range=Item, label='pole driver team')
polePosition = op('polePosition', range=Quantity, label='pole position')
poles = op('poles', range=Quantity, label='poles')
policeName = op('policeName', range=String, label='police name')
polishFilmAward = op('polishFilmAward', range=Item, label='Polish Film Award')
politicalFunction = op('politicalFunction', range=String, label='political function')
politicalLeader = op('politicalLeader', range=Item, label='political leader')
politicalMajority = op('politicalMajority', range=Item, label='political majority')
politicalPartyInLegislature = op('politicalPartyInLegislature', range=Item, label='political party in legislature')
politicalPartyOfLeader = op('politicalPartyOfLeader', range=Item, label='political party of leader')
politicalSeats = op('politicalSeats', range=Quantity, label='political seats')
politician = op('politician', range=Item, label='politician')
popularVote = op('popularVote', range=Quantity, label='Number of votes given to candidate')
population = op('population', range=Item, label='population')
populationAsOf = op('populationAsOf', range=Time, label='population as of')
populationDensity = op('populationDensity', range=Quantity, label='population density (/sqkm)')
populationMetro = op('populationMetro', range=Quantity, label='population metro')
populationMetroDensity = op('populationMetroDensity', range=Quantity, label='population metro density (/sqkm)')
populationPctChildren = op('populationPctChildren', range=Quantity, label='population percentage under 12 years')
populationPctMen = op('populationPctMen', range=Quantity, label='population percentage male')
populationPctWomen = op('populationPctWomen', range=Quantity, label='population percentage female')
populationPlace = op('populationPlace', range=Item, label='population place')
populationQuote = op('populationQuote', range=String, label='population quote')
populationRural = op('populationRural', range=Quantity, label='population rural')
populationRuralDensity = op('populationRuralDensity', range=Quantity, label='population density rural (/sqkm)')
populationTotal = op('populationTotal', range=Quantity, label='population total')
populationTotalRanking = op('populationTotalRanking', range=Quantity, label='total population ranking')
populationUrban = op('populationUrban', range=Quantity, label='population urban')
populationUrbanDensity = op('populationUrbanDensity', range=Quantity, label='population urban density (/sqkm)')
populationYear = op('populationYear', range=String, label='population year')
portfolio = op('portfolio', range=String, label='portfolio')
postalCode = op('postalCode', range=String, label='postal code')
power = op('power', range=String, label='power')
powerOutput = op('powerOutput', range=Quantity, label='power output (W)')
precursor = op('precursor', range=Item, label='precursor')
prefaceBy = op('prefaceBy', range=Item, label='author of preface')
prefect = op('prefect', range=Item, label='prefect')
prefectMandate = op('prefectMandate', range=String, label='mandate of a prefect of a romanian settlement')
prefecture = op('prefecture', range=Item, label='prefecture')
prefix = op('prefix', range=String, label='prefix')
premiereDate = op('premiereDate', range=Time, label='premiere date')
premiereYear = op('premiereYear', range=Time, label='premiere year')
presenter = op('presenter', range=Item, label='presenter')
presentMunicipality = op('presentMunicipality', range=Item, label='present municipality')
presentName = op('presentName', range=String, label='a municipality\'s present name')
president = op('president', range=Item, label='president')
presidentGeneralCouncil = op('presidentGeneralCouncil', range=Item, label='president general council')
presidentGeneralCouncilMandate = op('presidentGeneralCouncilMandate', range=String, label='mandate of the president of the general council')
presidentRegionalCouncil = op('presidentRegionalCouncil', range=Item, label='president regional council')
presidentRegionalCouncilMandate = op('presidentRegionalCouncilMandate', range=String, label='mandate of the president council of the regional council')
previousDemographics = op('previousDemographics', range=Item, label='previous demographics')
previousEditor = op('previousEditor', range=Item, label='previous editor')
previousEntity = op('previousEntity', range=Item, label='previous entity')
previousEvent = op('previousEvent', range=Item, label='previous event')
previousInfrastructure = op('previousInfrastructure', range=Item, label='previous infrastructure')
previousMission = op('previousMission', range=Item, label='previous mission')
previousName = op('previousName', range=String, label='previous name')
previousPopulation = op('previousPopulation', range=Item, label='previous population')
previousPopulationTotal = op('previousPopulationTotal', range=Quantity, label='previous population total')
previousTrackNumber = op('previousTrackNumber', range=Quantity, label='number of the previous track')
previousWork = op('previousWork', range=Item, label='previous work')
previousWorkDate = op('previousWorkDate', range=Item, label='previous work date')
price = op('price', range=Quantity, label='price ($)')
primate = op('primate', range=String, label='Primite')
primeMinister = op('primeMinister', range=Item, label='prime minister')
primogenitor = op('primogenitor', range=Item, label='primogenitor, first forebear')
principal = op('principal', range=Item, label='principal')
principalArea = op('principalArea', range=Item, label='principal area')
principalEngineer = op('principalEngineer', range=Item, label='principal engineer')
probowlPick = op('probowlPick', range=String, label='pro bowl pick')
procedure = op('procedure', range=String, label='procedure')
producedBy = op('producedBy', range=Item, label='produced by')
producer = op('producer', range=Item, label='producer')
production = op('production', range=Quantity, label='production')
productionCompany = op('productionCompany', range=Item, label='production company')
productionEndDate = op('productionEndDate', range=Time, label='production end date')
productionEndYear = op('productionEndYear', range=Time, label='production end year')
productionStartDate = op('productionStartDate', range=Time, label='production start date')
productionStartYear = op('productionStartYear', range=Time, label='production start year')
productionYears = op('productionYears', range=Time, label='production years')
productShape = op('productShape', range=String, label='product shape')
programCost = op('programCost', range=Quantity, label='program cost ($)')
project = op('project', range=Item, label='project')
projectBudgetFunding = op('projectBudgetFunding', range=Quantity, label='project budget funding ($)')
projectBudgetTotal = op('projectBudgetTotal', range=Quantity, label='project budget total ($)')
projectCoordinator = op('projectCoordinator', range=Item, label='project coordinator')
projectEndDate = op('projectEndDate', range=Time, label='project end date')
projectKeyword = op('projectKeyword', range=String, label='project keyword')
projectObjective = op('projectObjective', range=String, label='project objective')
projectParticipant = op('projectParticipant', range=Item, label='project participant')
projectReferenceID = op('projectReferenceID', range=String, label='project reference ID')
projectStartDate = op('projectStartDate', range=Time, label='project start date')
projectType = op('projectType', range=String, label='project type')
prominence = op('prominence', range=Quantity, label='prominence (μ)')
pronunciation = op('pronunciation', range=String, label='pronunciation')
prospectLeague = op('prospectLeague', range=Item, label='prospect league')
prospectTeam = op('prospectTeam', range=Item, label='prospect team')
proTeam = op('proTeam', range=Item, label='pro team')
protectionStatus = op('protectionStatus', range=String, label='monument protection status')
protein = op('protein', range=Quantity, label='protein (g)')
protestantPercentage = op('protestantPercentage', range=String, label='protestant percentage')
provCode = op('provCode', range=String, label='prove code')
province = op('province', range=Item, label='province')
provinceIsoCode = op('provinceIsoCode', range=String, label='iso code of a province')
provinceLink = op('provinceLink', range=Item, label='province link')
provost = op('provost', range=Item, label='provost')
pseudonym = op('pseudonym', range=Text, label='pseudonym')
pubchem = op('pubchem', range=String, label='PubChem')
publication = op('publication', range=String, label='publication')
publicationDate = op('publicationDate', range=Time, label='publication date')
publiclyAccessible = op('publiclyAccessible', range=String, label='publicly accessible')
publisher = op('publisher', range=Item, label='publisher')
purchasingPowerParity = op('purchasingPowerParity', range=String, label='purchasing power parity')
purchasingPowerParityRank = op('purchasingPowerParityRank', range=String, label='purchasing power parity rank')
purchasingPowerParityYear = op('purchasingPowerParityYear', range=String, label='purchasing power parity year')
purpose = op('purpose', range=String, label='purpose')
qatarClassic = op('qatarClassic', range=String, label='qatar classic')
quebecerTitle = op('quebecerTitle', range=String, label='quebecer title')
quotation = op('quotation', range=String, label='quotation')
quote = op('quote', range=String, label='quote')
ra = op('ra', range=String, label='ra')
race = op('race', range=Item, label='race')
raceHorse = op('raceHorse', range=Item, label='race horse')
raceLength = op('raceLength', range=Quantity, label='race length (μ)')
raceResult = op('raceResult', range=Item, label='race result')
races = op('races', range=Quantity, label='races')
raceTrack = op('raceTrack', range=Item, label='race track')
raceWins = op('raceWins', range=Quantity, label='race wins')
racketCatching = op('racketCatching', range=String, label='racket catching')
radio = op('radio', range=Item, label='radio')
radioStation = op('radioStation', range=String, label='radio station')
radius_ly = op('radius_ly', range=Quantity, label='Radius_ly')
railGauge = op('railGauge', range=Quantity, label='rail gauge (μ)')
railwayPlatforms = op('railwayPlatforms', range=String, label='railway platforms')
range = op('range', range=Quantity, label='range')
rank = op('rank', range=String, label='rank')
rankAgreement = op('rankAgreement', range=Quantity, label='rank of an agreement')
rankArea = op('rankArea', range=Quantity, label='rank of an area')
rankInFinalMedalCount = op('rankInFinalMedalCount', range=Quantity, label='rank in final medal count')
ranking = op('ranking', range=Quantity, label='ranking')
rankingsDoubles = op('rankingsDoubles', range=Quantity, label='doubles rankings')
rankingsSingles = op('rankingsSingles', range=Quantity, label='single rankings')
rankingWins = op('rankingWins', range=Quantity, label='ranking wins')
rankPopulation = op('rankPopulation', range=Quantity, label='rank of a population')
rating = op('rating', range=Quantity, label='rating')
ratio = op('ratio', range=String, label='ratio')
rebuildDate = op('rebuildDate', range=Time, label='rebuild date')
rebuildingDate = op('rebuildingDate', range=Time, label='rebuilding date')
rebuildingYear = op('rebuildingYear', range=Time, label='rebuilding year')
recentWinner = op('recentWinner', range=Item, label='recent winner')
recommissioningDate = op('recommissioningDate', range=Time, label='recommissioning date')
recordDate = op('recordDate', range=Time, label='record date')
recordedIn = op('recordedIn', range=Item, label='recorded in')
recordLabel = op('recordLabel', range=Item, label='record label')
recoveryCases = op('recoveryCases', range=Quantity, label='Recovery Cases')
rector = op('rector', range=Item, label='rector')
redline = op('redline', range=Quantity, label='redline (kmh)')
redListIdNL = op('redListIdNL', range=Quantity, label='red list ID NL')
redLongDistancePisteNumber = op('redLongDistancePisteNumber', range=Quantity, label='red long distance piste number')
redSkiPisteNumber = op('redSkiPisteNumber', range=Quantity, label='red ski piste number')
refcul = op('refcul', range=String, label='reference for cultural data')
reference = op('reference', range=String, label='reference')
reffBourgmestre = op('reffBourgmestre', range=Item, label='referent bourgmestre')
refgen = op('refgen', range=String, label='reference for general data')
refgeo = op('refgeo', range=String, label='reference for geographic data')
refpol = op('refpol', range=String, label='reference for politic data')
refseq = op('refseq', range=String, label='RefSeq')
refseqmrna = op('refseqmrna', range=String, label='refseq mRNA')
refseqprotein = op('refseqprotein', range=String, label='refseq protein')
regency = op('regency', range=Item, label='regency')
regentOf = op('regentOf', range=Item, label='regent of')
regime = op('regime', range=String, label='regime')
region = op('region', range=Item, label='region')
regionalCouncil = op('regionalCouncil', range=Item, label='regional council')
regionalLanguage = op('regionalLanguage', range=Item, label='regional language')
regionalPrefecture = op('regionalPrefecture', range=String, label='regional prefecture')
regionLink = op('regionLink', range=String, label='region link')
regionServed = op('regionServed', range=Item, label='region served')
regionType = op('regionType', range=String, label='region type')
registration = op('registration', range=String, label='registration')
registry = op('registry', range=String, label='registry')
registryNumber = op('registryNumber', range=String, label='registry number')
reign = op('reign', range=String, label='reign')
reigningPope = op('reigningPope', range=Item, label='reigning pope')
reignName = op('reignName', range=String, label='reign name')
relatedFunctions = op('relatedFunctions', range=Item, label='related functions')
relatedMeanOfTransportation = op('relatedMeanOfTransportation', range=Item, label='related mean of transportation')
relatedPlaces = op('relatedPlaces', range=Item, label='related places')
relation = op('relation', range=Item, label='relation')
relative = op('relative', range=Item, label='relative')
relativeAtomicMass = op('relativeAtomicMass', range=Quantity, label='atomic weight')
releaseDate = op('releaseDate', range=Time, label='release date')
releaseLocation = op('releaseLocation', range=Item, label='release location')
relics = op('relics', range=String, label='relics')
relief = op('relief', range=String, label='relief')
religiousHead = op('religiousHead', range=Item, label='religious head')
religiousOrder = op('religiousOrder', range=Item, label='religious order')
reopened = op('reopened', range=Time, label='reopened')
reopeningDate = op('reopeningDate', range=Time, label='reopening date')
reopeningYear = op('reopeningYear', range=Time, label='reopening year')
reportingMark = op('reportingMark', range=String, label='reporting mark')
representative = op('representative', range=Quantity, label='number of representatives')
requirement = op('requirement', range=String, label='requirement')
reservations = op('reservations', range=Quantity, label='reservations')
residence = op('residence', range=Item, label='residence')
restaurant = op('restaurant', range=Item, label='hotel')
restingDate = op('restingDate', range=Time, label='resting date')
restingPlace = op('restingPlace', range=Item, label='resting place')
restoreDate = op('restoreDate', range=Time, label='restore date')
restriction = op('restriction', range=String, label='restriction')
result = op('result', range=String, label='result')
retentionTime = op('retentionTime', range=String, label='relation time')
retired = op('retired', range=Time, label='retired')
retiredRocket = op('retiredRocket', range=Item, label='retired rocket')
retirementDate = op('retirementDate', range=Time, label='retirement date')
revenue = op('revenue', range=Quantity, label='revenue ($)')
revenueYear = op('revenueYear', range=Time, label='year of reported revenue')
review = op('review', range=IRI, label='review')
rgbCoordinateBlue = op('rgbCoordinateBlue', range=Quantity, label='bluecoordinate in the RGB space')
rgbCoordinateGreen = op('rgbCoordinateGreen', range=Quantity, label='green coordinate in the RGB space')
rgbCoordinateRed = op('rgbCoordinateRed', range=Quantity, label='red coordinate in the RGB space')
ridId = op('ridId', range=String, label='RID Id')
rightAscension = op('rightAscension', range=Quantity, label='right ascension')
rightChild = op('rightChild', range=Item, label='right child')
rightTributary = op('rightTributary', range=Item, label='right tributary')
rivalSchool = op('rivalSchool', range=Item, label='rival')
river = op('river', range=Item, label='river')
riverBranch = op('riverBranch', range=Item, label='branch')
riverBranchOf = op('riverBranchOf', range=Item, label='branch of')
riverMouth = op('riverMouth', range=Item, label='river mouth')
rkdArtistsId = op('rkdArtistsId', range=String, label='RKDartists id')
road = op('road', range=Item, label='road')
rocket = op('rocket', range=Item, label='rocket')
rocketStages = op('rocketStages', range=Quantity, label='number of rocket stages')
rolandGarrosDouble = op('rolandGarrosDouble', range=String, label='roland garros double')
rolandGarrosMixed = op('rolandGarrosMixed', range=String, label='roland garros mixed')
rolandGarrosSingle = op('rolandGarrosSingle', range=String, label='roland garros single')
role = op('role', range=String, label='role')
roleInEvent = op('roleInEvent', range=Item, label='A Person\'s role in an event')
roofHeight = op('roofHeight', range=Quantity, label='roof height')
rotationPeriod = op('rotationPeriod', range=Quantity, label='rotation period (s)')
route = op('route', range=String, label='route')
routeDirection = op('routeDirection', range=String, label='route direction')
routeEnd = op('routeEnd', range=Item, label='route end')
routeEndDirection = op('routeEndDirection', range=String, label='road end direction')
routeEndLocation = op('routeEndLocation', range=Item, label='route end location')
routeJunction = op('routeJunction', range=Item, label='route junction')
routeNext = op('routeNext', range=Item, label='route next stop')
routeNumber = op('routeNumber', range=String, label='route number')
routePrevious = op('routePrevious', range=Item, label='route previous stop')
routeStart = op('routeStart', range=Item, label='route start')
routeStartDirection = op('routeStartDirection', range=String, label='road start direction')
routeStartLocation = op('routeStartLocation', range=Item, label='route start location')
routeTypeAbbreviation = op('routeTypeAbbreviation', range=String, label='route type abbreviation')
ruling = op('ruling', range=String, label='ruling')
runningMate = op('runningMate', range=Item, label='running mate')
runtime = op('runtime', range=Quantity, label='runtime (s)')
runwayDesignation = op('runwayDesignation', range=String, label='designation of runway')
runwayLength = op('runwayLength', range=Quantity, label='length of runway (μ)')
runwaySurface = op('runwaySurface', range=String, label='surface of runway')
runwayWidth = op('runwayWidth', range=Quantity, label='width of runway (μ)')
ruralMunicipality = op('ruralMunicipality', range=Item, label='rural municipality')
saint = op('saint', range=Item, label='saint')
salary = op('salary', range=Quantity, label='salary ($)')
sales = op('sales', range=Item, label='sales')
sameName = op('sameName', range=Text, label='same name')
satcat = op('satcat', range=String, label='SATCAT')
satellite = op('satellite', range=String, label='satellite')
satellitesDeployed = op('satellitesDeployed', range=Quantity, label='satellites deployed')
scale = op('scale', range=String, label='scale')
scaleFactor = op('scaleFactor', range=Quantity, label='scale factor')
scene = op('scene', range=String, label='scene')
school = op('school', range=Item, label='school')
schoolCode = op('schoolCode', range=String, label='school code')
schoolNumber = op('schoolNumber', range=String, label='school number')
schoolPatron = op('schoolPatron', range=Item, label='school patron')
scientificName = op('scientificName', range=String, label='scientific name')
score = op('score', range=Quantity, label='score')
screenActorsGuildAward = op('screenActorsGuildAward', range=Item, label='Screen Actors Guild Award')
sea = op('sea', range=Item, label='sea')
seasonManager = op('seasonManager', range=String, label='season manager')
seasonNumber = op('seasonNumber', range=Quantity, label='season number')
seatingCapacity = op('seatingCapacity', range=Quantity, label='seating capacity')
seatNumber = op('seatNumber', range=Quantity, label='number of seats in the land parlement')
second = op('second', range=Quantity, label='second')
secondCommander = op('secondCommander', range=Item, label='second commander')
secondDriver = op('secondDriver', range=Item, label='second driver')
secondDriverCountry = op('secondDriverCountry', range=Item, label='second driver country')
secondLeader = op('secondLeader', range=Item, label='secondLeader')
secondPlace = op('secondPlace', range=String, label='second place')
secondPopularVote = op('secondPopularVote', range=Item, label='secondPopularVote')
secondTeam = op('secondTeam', range=Item, label='second team')
secretaryGeneral = op('secretaryGeneral', range=Item, label='secretary')
security = op('security', range=String, label='security')
seiyu = op('seiyu', range=Item, label='seiyu')
selectionPoint = op('selectionPoint', range=Quantity, label='selection point')
selectionYear = op('selectionYear', range=String, label='selection year')
selibrId = op('selibrId', range=String, label='SELIBR Id')
senator = op('senator', range=Item, label='senator')
senior = op('senior', range=String, label='senior')
seniority = op('seniority', range=String, label='seniority')
seniunija = op('seniunija', range=String, label='seniunija')
sentence = op('sentence', range=String, label='sentence')
serviceEndDate = op('serviceEndDate', range=Time, label='service end date')
serviceEndYear = op('serviceEndYear', range=Time, label='service end year')
serviceModule = op('serviceModule', range=String, label='service module')
serviceNumber = op('serviceNumber', range=String, label='service number')
serviceStartDate = op('serviceStartDate', range=Time, label='service start date')
serviceStartYear = op('serviceStartYear', range=Time, label='service start year')
servingSize = op('servingSize', range=Quantity, label='serving size (g)')
servingTemperature = op('servingTemperature', range=String, label='serving temperature')
sessionNumber = op('sessionNumber', range=Quantity, label='session number')
setDesigner = op('setDesigner', range=Item, label='set designer')
settingOfPlay = op('settingOfPlay', range=String, label='setting of play')
settlement = op('settlement', range=Item, label='settlement')
settlementAttached = op('settlementAttached', range=Item, label='settlement attached')
setupTime = op('setupTime', range=Quantity, label='setup time (s)')
severeCases = op('severeCases', range=Quantity, label='Severe Cases')
sex = op('sex', range=String, label='sex')
shape = op('shape', range=Item, label='intercommunality shape')
shareDate = op('shareDate', range=Time, label='share date')
shareOfAudience = op('shareOfAudience', range=Quantity, label='share of audience')
shareSource = op('shareSource', range=String, label='share source')
sharingOutPopulation = op('sharingOutPopulation', range=Quantity, label='sharing out population')
sharingOutPopulationYear = op('sharingOutPopulationYear', range=String, label='sharing out year')
sheading = op('sheading', range=Item, label='sheading')
shipBeam = op('shipBeam', range=Quantity, label='ship beam (μ)')
shipCrew = op('shipCrew', range=Item, label='crew')
shipDisplacement = op('shipDisplacement', range=Quantity, label='displacement (g)')
shipDraft = op('shipDraft', range=Quantity, label='ship draft (μ)')
shipLaunch = op('shipLaunch', range=Time, label='ship launched')
shoeNumber = op('shoeNumber', range=Quantity, label='shoe number')
shoeSize = op('shoeSize', range=String, label='shoe size')
shoot = op('shoot', range=String, label='shoot')
shoots = op('shoots', range=String, label='shoots')
shoreLength = op('shoreLength', range=Quantity, label='shore length (μ)')
shortProgCompetition = op('shortProgCompetition', range=String, label='short prog competition')
shortProgScore = op('shortProgScore', range=String, label='short prog score')
show = op('show', range=Item, label='show')
showJudge = op('showJudge', range=Item, label='showJudge')
shuttle = op('shuttle', range=Item, label='shuttle')
sibling = op('sibling', range=Item, label='sibling')
signature = op('signature', range=String, label='signature')
significantBuilding = op('significantBuilding', range=Item, label='significant building')
signName = op('signName', range=Text, label='sign name of a hungarian settlement')
silverMedalDouble = op('silverMedalDouble', range=String, label='silver medal double')
silverMedalist = op('silverMedalist', range=Item, label='siler medalist')
silverMedalMixed = op('silverMedalMixed', range=String, label='silver medal mixed')
silverMedalSingle = op('silverMedalSingle', range=String, label='silver medal single')
singleList = op('singleList', range=Item, label='list of singles')
singleOf = op('singleOf', range=Item, label='singleOf')
sire = op('sire', range=Item, label='sire')
siren = op('siren', range=Quantity, label='siren number')
sister = op('sister', range=Item, label='sister')
sisterCollege = op('sisterCollege', range=Item, label='sister college')
sisterNewspaper = op('sisterNewspaper', range=Item, label='sister newspaper')
sisterStation = op('sisterStation', range=Item, label='sister station')
sixthFormStudents = op('sixthFormStudents', range=String, label='sixth form students')
size_v = op('size_v', range=Quantity, label='size_v')
sizeBlazon = op('sizeBlazon', range=String, label='size blazon')
sizeLogo = op('sizeLogo', range=Quantity, label='size logo')
sizeMap = op('sizeMap', range=String, label='size map')
sizeThumbnail = op('sizeThumbnail', range=String, label='size thumbnail')
skiLift = op('skiLift', range=Quantity, label='ski lift')
skinColor = op('skinColor', range=String, label='skin color')
skiPisteKilometre = op('skiPisteKilometre', range=Quantity, label='ski piste kilometre (μ)')
skiPisteNumber = op('skiPisteNumber', range=Quantity, label='ski piste number')
skiTow = op('skiTow', range=Quantity, label='ski tow')
slogan = op('slogan', range=Text, label='slogan')
smiles = op('smiles', range=String, label='SMILES')
snowParkNumber = op('snowParkNumber', range=Quantity, label='snow park number')
soccerLeaguePromoted = op('soccerLeaguePromoted', range=Item, label='promoted')
soccerLeagueRelegated = op('soccerLeagueRelegated', range=Item, label='relegated teams')
soccerLeagueSeason = op('soccerLeagueSeason', range=Item, label='season')
soccerLeagueWinner = op('soccerLeagueWinner', range=Item, label='league champion')
soccerTournamentClosingSeason = op('soccerTournamentClosingSeason', range=Item, label='closing season')
soccerTournamentLastChampion = op('soccerTournamentLastChampion', range=Item, label='last champion')
soccerTournamentMostSteady = op('soccerTournamentMostSteady', range=Item, label='most steady')
soccerTournamentMostSuccesfull = op('soccerTournamentMostSuccesfull', range=Item, label='most successfull')
soccerTournamentOpeningSeason = op('soccerTournamentOpeningSeason', range=Item, label='opening season')
soccerTournamentThisSeason = op('soccerTournamentThisSeason', range=Item, label='this season')
soccerTournamentTopScorer = op('soccerTournamentTopScorer', range=Item, label='top scorer')
solicitorGeneral = op('solicitorGeneral', range=Item, label='solicitor general')
solubility = op('solubility', range=Quantity, label='solubility')
solvent = op('solvent', range=Item, label='solvent')
solventWithBadSolubility = op('solventWithBadSolubility', range=Item, label='solvent with bad solubility')
solventWithGoodSolubility = op('solventWithGoodSolubility', range=Item, label='solvent with good solubility')
solventWithMediocreSolubility = op('solventWithMediocreSolubility', range=Item, label='solvent with mediocre solubility')
son = op('son', range=Item, label='son')
soundRecording = op('soundRecording', range=Item, label='sound recording')
sourceConfluenceCountry = op('sourceConfluenceCountry', range=Item, label='source confluence country')
sourceConfluenceElevation = op('sourceConfluenceElevation', range=Quantity, label='source confluence elevation (μ)')
sourceConfluenceMountain = op('sourceConfluenceMountain', range=Item, label='source confluence mountain')
sourceConfluencePlace = op('sourceConfluencePlace', range=Item, label='source confluence place')
sourceConfluenceRegion = op('sourceConfluenceRegion', range=Item, label='source confluence region')
sourceConfluenceState = op('sourceConfluenceState', range=Item, label='source confluence state')
sourceCountry = op('sourceCountry', range=Item, label='source country')
sourceDistrict = op('sourceDistrict', range=Item, label='source district')
sourceElevation = op('sourceElevation', range=Quantity, label='source elevation (μ)')
sourceMountain = op('sourceMountain', range=Item, label='source mountain')
sourceName = op('sourceName', range=Item, label='Source Name')
sourcePlace = op('sourcePlace', range=Item, label='source place')
sourceRegion = op('sourceRegion', range=Item, label='source region')
sourceState = op('sourceState', range=Item, label='source state')
sourceText = op('sourceText', range=Text, label='sourceText')
sourceWebsite = op('sourceWebsite', range=Item, label='Source Website')
southEastPlace = op('southEastPlace', range=Item, label='south-east place')
southPlace = op('southPlace', range=Item, label='south place')
southWestPlace = op('southWestPlace', range=Item, label='south-west place')
sovereignCountry = op('sovereignCountry', range=Item, label='sovereign country')
space = op('space', range=Quantity, label='space')
spacecraft = op('spacecraft', range=Item, label='spacecraft')
spacestation = op('spacestation', range=Item, label='spacestation')
spacewalkBegin = op('spacewalkBegin', range=Time, label='spacewalk begin')
spacewalkEnd = op('spacewalkEnd', range=Time, label='spacewalk end')
speaker = op('speaker', range=Quantity, label='speaker')
specialEffects = op('specialEffects', range=Item, label='special effects')
specialist = op('specialist', range=Item, label='specialist')
speciality = op('speciality', range=String, label='speciality')
specialTrial = op('specialTrial', range=Quantity, label='special trial')
species = op('species', range=Item, label='species')
speedLimit = op('speedLimit', range=Quantity, label='speed limit (kmh)')
spike = op('spike', range=String, label='spike')
splitFromParty = op('splitFromParty', range=Item, label='split from party')
spokenIn = op('spokenIn', range=Item, label='spoken in')
spokesperson = op('spokesperson', range=Item, label='spokesperson')
sport = op('sport', range=Item, label='sport')
sportCountry = op('sportCountry', range=Item, label='sport country')
sportDiscipline = op('sportDiscipline', range=Item, label='sport discipline')
sportsFunction = op('sportsFunction', range=String, label='sports function')
sportSpecialty = op('sportSpecialty', range=Item, label='sport specialty')
spouse = op('spouse', range=Item, label='spouse')
spouseName = op('spouseName', range=String, label='spouse name')
spurOf = op('spurOf', range=Item, label='spur of')
squadNumber = op('squadNumber', range=Quantity, label='squad number')
stadium = op('stadium', range=Item, label='Stadium')
staff = op('staff', range=Quantity, label='staff')
starRating = op('starRating', range=Quantity, label='star rating')
starring = op('starring', range=Item, label='starring')
start = op('start', range=Time, label='start')
startCareer = op('startCareer', range=String, label='start career')
startDate = op('startDate', range=Time, label='start date')
startDateTime = op('startDateTime', range=Time, label='start date and time')
startOccupation = op('startOccupation', range=String, label='start occupation')
startPoint = op('startPoint', range=Item, label='start point')
startWct = op('startWct', range=String, label='start xct')
startWqs = op('startWqs', range=String, label='start wqs')
startYear = op('startYear', range=Time, label='start year')
startYearOfInsertion = op('startYearOfInsertion', range=Time, label='start year of insertion')
startYearOfSales = op('startYearOfSales', range=Time, label='start year of sales')
state = op('state', range=Item, label='state')
stateDelegate = op('stateDelegate', range=Item, label='state delegate')
stateOfOrigin = op('stateOfOrigin', range=Item, label='state of origin')
stateOfOriginPoint = op('stateOfOriginPoint', range=Quantity, label='state of origin point')
stateOfOriginTeam = op('stateOfOriginTeam', range=Item, label='state of origin team')
stateOfOriginYear = op('stateOfOriginYear', range=String, label='state of origin year')
stationEvaDuration = op('stationEvaDuration', range=Quantity, label='station EVA duration (s)')
stationStructure = op('stationStructure', range=String, label='station structure')
stationVisitDuration = op('stationVisitDuration', range=Quantity, label='station visit duration (s)')
statisticValue = op('statisticValue', range=Quantity, label='statistic value')
statisticYear = op('statisticYear', range=Time, label='statistic year')
statName = op('statName', range=String, label='stat name')
status = op('status', range=String, label='status')
statusManager = op('statusManager', range=String, label='status manager')
statusYear = op('statusYear', range=String, label='status year')
statValue = op('statValue', range=Quantity, label='stat value')
stockExchange = op('stockExchange', range=String, label='Registered at Stock Exchange')
storyEditor = op('storyEditor', range=Item, label='story editor')
strength = op('strength', range=String, label='strength')
student = op('student', range=Item, label='student')
stylisticOrigin = op('stylisticOrigin', range=Item, label='stylistic origin')
subdivisionLink = op('subdivisionLink', range=String, label='subdivision link')
subdivisionName = op('subdivisionName', range=Item, label='subdivision name of the island')
subdivisions = op('subdivisions', range=Quantity, label='subdivisions')
subFamily = op('subFamily', range=Item, label='sub-family')
subjectOfPlay = op('subjectOfPlay', range=String, label='subject of play')
subjectTerm = op('subjectTerm', range=String, label='subject term')
sublimationPoint = op('sublimationPoint', range=Quantity, label='sublimation point (K)')
subMunicipalityType = op('subMunicipalityType', range=String, label='type of municipality')
suborbitalFlights = op('suborbitalFlights', range=Quantity, label='suborbital flights')
subprefecture = op('subprefecture', range=Item, label='subprefecture')
subPrefecture = op('subPrefecture', range=String, label='subprefecture')
subregion = op('subregion', range=Item, label='subregion')
subsequentInfrastructure = op('subsequentInfrastructure', range=Item, label='subsequent infrastructure')
subsequentWork = op('subsequentWork', range=Item, label='subsequent work')
subsequentWorkDate = op('subsequentWorkDate', range=Item, label='subsequent work date')
subsidiary = op('subsidiary', range=Item, label='subsidiary')
subsystem = op('subsystem', range=String, label='subsystem')
subsystemLink = op('subsystemLink', range=String, label='subsystem link')
subtitle = op('subtitle', range=String, label='subtitle')
subTribus = op('subTribus', range=Item, label='subtribus')
successfulLaunches = op('successfulLaunches', range=Quantity, label='successful launches')
sudocId = op('sudocId', range=String, label='SUDOC id')
summerAppearances = op('summerAppearances', range=Item, label='summer appearances')
summerTemperature = op('summerTemperature', range=Quantity, label='summer temperature (K)')
superbowlWin = op('superbowlWin', range=String, label='superbowl win')
superFamily = op('superFamily', range=Item, label='super-family')
superintendent = op('superintendent', range=Item, label='superintendent')
superTribus = op('superTribus', range=Item, label='supertribus')
supplementalDraftRound = op('supplementalDraftRound', range=String, label='supplemental draft round')
supplementalDraftYear = op('supplementalDraftYear', range=Time, label='supplemental draft year')
supplies = op('supplies', range=Item, label='supplies')
supply = op('supply', range=Item, label='supply')
suppreddedDate = op('suppreddedDate', range=Time, label='suppredded date')
surfaceArea = op('surfaceArea', range=Quantity, label='surface area (m2)')
surfaceFormOccurrenceOffset = op('surfaceFormOccurrenceOffset', range=String, label='position in which a surface occurs in a text')
surfaceGravity = op('surfaceGravity', range=Quantity, label='surface gravity (g)')
surfaceType = op('surfaceType', range=String, label='type of surface')
suspectedCases = op('suspectedCases', range=Quantity, label='Suspected Cases')
swimmingStyle = op('swimmingStyle', range=String, label='Swimming style')
symbol = op('symbol', range=String, label='Symbol')
synonym = op('synonym', range=String, label='synonym')
systemOfLaw = op('systemOfLaw', range=Item, label='system of law')
systemRequirements = op('systemRequirements', range=String, label='minimum system requirements')
tag = op('tag', range=Time, label='tag')
taoiseach = op('taoiseach', range=Item, label='taoiseach')
targetAirport = op('targetAirport', range=Item, label='target airport')
targetSpaceStation = op('targetSpaceStation', range=Item, label='target space station station')
taste = op('taste', range=String, label='taste or flavour')
tattoo = op('tattoo', range=String, label='tattoo')
taxon = op('taxon', range=Item, label='has taxon')
team = op('team', range=Item, label='team')
teamCoached = op('teamCoached', range=Item, label='team coached')
teamManager = op('teamManager', range=Item, label='team manager')
teamName = op('teamName', range=Text, label='team name')
teamPoint = op('teamPoint', range=Quantity, label='team point')
teamSize = op('teamSize', range=Quantity, label='team size')
teamTitle = op('teamTitle', range=String, label='team title')
technique = op('technique', range=String, label='technique')
televisionSeries = op('televisionSeries', range=Item, label='television series')
temperature = op('temperature', range=Quantity, label='temperature (K)')
templateName = op('templateName', range=String, label='template name')
temple = op('temple', range=String, label='temple')
templeYear = op('templeYear', range=String, label='temple year')
tempPlace = op('tempPlace', range=String, label='Temporary Placement in the Music Charts')
tenant = op('tenant', range=Item, label='tenant')
tennisSurfaceType = op('tennisSurfaceType', range=String, label='type of tennis surface')
termOfOffice = op('termOfOffice', range=String, label='term of office')
termPeriod = op('termPeriod', range=Item, label='term period')
territory = op('territory', range=Item, label='territory')
tessitura = op('tessitura', range=String, label='tessitura')
testaverage = op('testaverage', range=Quantity, label='testaverage')
theology = op('theology', range=String, label='Theology')
third = op('third', range=Quantity, label='third')
thirdCommander = op('thirdCommander', range=Item, label='third commander')
thirdDriver = op('thirdDriver', range=Item, label='third driver')
thirdDriverCountry = op('thirdDriverCountry', range=Item, label='third driver country')
thirdPlace = op('thirdPlace', range=String, label='third place')
thirdTeam = op('thirdTeam', range=Item, label='third team')
throwingSide = op('throwingSide', range=String, label='throwing side')
thumbnail = op('thumbnail', range=Item, label='thumbnail')
thumbnailCaption = op('thumbnailCaption', range=String, label='thumbnail caption')
tie = op('tie', range=Quantity, label='tie')
time = op('time', range=String, label='time')
timeInSpace = op('timeInSpace', range=Quantity, label='total time person has spent in space (s)')
timeshiftChannel = op('timeshiftChannel', range=String, label='timeshift channel')
title = op('title', range=Text, label='title')
titleDate = op('titleDate', range=Time, label='title date')
titleDouble = op('titleDouble', range=String, label='title double')
titleLanguage = op('titleLanguage', range=String, label='title language')
titleSingle = op('titleSingle', range=String, label='title single')
toll = op('toll', range=Quantity, label='toll ($)')
tonyAward = op('tonyAward', range=Item, label='Tony Award')
topFloorHeight = op('topFloorHeight', range=Quantity, label='top floor height')
topic = op('topic', range=String, label='topic')
topLevelDomain = op('topLevelDomain', range=Item, label='country top level (tld)')
topSpeed = op('topSpeed', range=Quantity, label='top speed (kmh)')
torchBearer = op('torchBearer', range=Item, label='torch bearer')
torqueOutput = op('torqueOutput', range=Quantity, label='torque output (Nm)')
totalCargo = op('totalCargo', range=Quantity, label='total cargo (g)')
totalDiscs = op('totalDiscs', range=Quantity, label='total discs')
totalIliCases = op('totalIliCases', range=Quantity, label='Total Pandemic Cases')
totalLaunches = op('totalLaunches', range=Quantity, label='total launches')
totalMass = op('totalMass', range=Quantity, label='total mass (g)')
totalPopulation = op('totalPopulation', range=Quantity, label='total population')
totalTracks = op('totalTracks', range=Quantity, label='total tracks')
totalTravellers = op('totalTravellers', range=Quantity, label='total travellers')
totalVaccinations = op('totalVaccinations', range=Item, label='Total Vaccinations')
totalVaccinationsPerHundred = op('totalVaccinationsPerHundred', range=Item, label='Total Vaccinations Per Hundred')
touristicSite = op('touristicSite', range=Item, label='touristic site')
tournamentOfChampions = op('tournamentOfChampions', range=String, label='tournament of champions')
tournamentRecord = op('tournamentRecord', range=String, label='tournament record')
towerHeight = op('towerHeight', range=Quantity, label='tower height')
trackLength = op('trackLength', range=Quantity, label='track length (μ)')
trackNumber = op('trackNumber', range=Quantity, label='track number')
trackWidth = op('trackWidth', range=Quantity, label='track width (μ)')
tradingName = op('tradingName', range=String, label='trading name')
trainer = op('trainer', range=Item, label='trainer')
trainerClub = op('trainerClub', range=Item, label='trainer club')
trainerYears = op('trainerYears', range=Time, label='trainer years')
training = op('training', range=Item, label='training')
translatedMotto = op('translatedMotto', range=String, label='translated motto')
translator = op('translator', range=Item, label='translator')
transmission = op('transmission', range=String, label='transmission')
tree = op('tree', range=Item, label='tree')
tribus = op('tribus', range=Item, label='tribus')
trustee = op('trustee', range=Item, label='trustee')
tuition = op('tuition', range=Quantity, label='tuition ($)')
tvComId = op('tvComId', range=Quantity, label='tv.com id')
tvShow = op('tvShow', range=Item, label='tvShow')
twinCountry = op('twinCountry', range=Item, label='twin country')
twinTown = op('twinTown', range=Item, label='twin city')
typeCoordinate = op('typeCoordinate', range=String, label='type coordinate')
typeOfGrain = op('typeOfGrain', range=String, label='type of grain (wheat etc.)')
typeOfStorage = op('typeOfStorage', range=String, label='type of storage')
typeOfYeast = op('typeOfYeast', range=String, label='type of yeast')
uciCode = op('uciCode', range=String, label='UCI code')
ulanId = op('ulanId', range=String, label='ULAN id')
umbrellaTitle = op('umbrellaTitle', range=Text, label='umbrella title')
uncle = op('uncle', range=Item, label='uncle')
undraftedYear = op('undraftedYear', range=Time, label='undrafted year')
unesco = op('unesco', range=Item, label='unesco')
unicode = op('unicode', range=String, label='unicode')
uniprot = op('uniprot', range=String, label='UniProt')
unitaryAuthority = op('unitaryAuthority', range=Item, label='unitary authority')
unitCost = op('unitCost', range=Quantity, label='unit cost ($)')
unitedStatesNationalBridgeId = op('unitedStatesNationalBridgeId', range=String, label='United States National Bridge ID')
university = op('university', range=Item, label='university')
unknownOutcomes = op('unknownOutcomes', range=Quantity, label='unknown outcomes')
unloCode = op('unloCode', range=String, label='UN/LOCODE')
unNumber = op('unNumber', range=String, label='UN number')
updated = op('updated', range=Time, label='updated')
upperAge = op('upperAge', range=Quantity, label='upper age')
urbanArea = op('urbanArea', range=String, label='urban area')
usedInWar = op('usedInWar', range=Item, label='used in war')
usingCountry = op('usingCountry', range=Item, label='using country')
usk = op('usk', range=Quantity, label='approved rating of the Entertainment Software Self-Regulation Body in Germany')
usOpenDouble = op('usOpenDouble', range=String, label='us open double')
usOpenMixed = op('usOpenMixed', range=String, label='us open mixed')
usOpenSingle = op('usOpenSingle', range=String, label='us open single')
usSales = op('usSales', range=Quantity, label='US sales')
usurper = op('usurper', range=Item, label='usurper')
utcOffset = op('utcOffset', range=String, label='UTC offset')
v_hb = op('v_hb', range=Quantity, label='V_hb')
vaccination = op('vaccination', range=Item, label='vaccination')
vaccine = op('vaccine', range=String, label='Vaccine')
value = op('value', range=Quantity, label='value')
valvetrain = op('valvetrain', range=String, label='valvetrain')
vaporPressure = op('vaporPressure', range=String, label='vapor pressure (hPa)')
vehicle = op('vehicle', range=Item, label='vehicle')
vehicleCode = op('vehicleCode', range=String, label='vehicle code')
vehiclesInFleet = op('vehiclesInFleet', range=Item, label='vehicle types in fleet')
vehiclesPerDay = op('vehiclesPerDay', range=Quantity, label='vehicles per day')
vein = op('vein', range=Item, label='vein')
veneratedIn = op('veneratedIn', range=Item, label='venerated in')
viafId = op('viafId', range=String, label='VIAF Id')
viceChancellor = op('viceChancellor', range=Item, label='vice chancellor')
viceLeader = op('viceLeader', range=Item, label='vice leader')
viceLeaderParty = op('viceLeaderParty', range=Item, label='vice leader party')
vicePresident = op('vicePresident', range=Item, label='vice president')
vicePrimeMinister = op('vicePrimeMinister', range=Item, label='vice prime minister')
vicePrincipal = op('vicePrincipal', range=Item, label='vice principal')
victims = op('victims', range=String, label='victims (string)')
victory = op('victory', range=Quantity, label='victory')
victoryAsMgr = op('victoryAsMgr', range=Quantity, label='victory as manager')
victoryPercentageAsMgr = op('victoryPercentageAsMgr', range=Quantity, label='victory percentage as manager')
virtualChannel = op('virtualChannel', range=String, label='virtual channel')
visitorsPercentageChange = op('visitorsPercentageChange', range=Quantity, label='visitor percentage change')
visitorsPerDay = op('visitorsPerDay', range=Quantity, label='visitors per day')
visitorsPerYear = op('visitorsPerYear', range=Quantity, label='visitors per year')
visitorStatisticsAsOf = op('visitorStatisticsAsOf', range=Time, label='visitor statistics as of')
visitorsTotal = op('visitorsTotal', range=Quantity, label='visitors total')
voice = op('voice', range=Item, label='voice')
volcanicActivity = op('volcanicActivity', range=String, label='volcanic activity')
volcanicType = op('volcanicType', range=String, label='volcanic type')
volcanoId = op('volcanoId', range=String, label='volcano id')
voltageOfElectrification = op('voltageOfElectrification', range=Quantity, label='voltage of electrification (V)')
volume = op('volume', range=Quantity, label='volume (μ³)')
volumeQuote = op('volumeQuote', range=String, label='volume quote')
volumes = op('volumes', range=Item, label='volumes')
vonKlitzingConstant = op('vonKlitzingConstant', range=Quantity, label='von Klitzing electromagnetic constant (RK)')
votesAgainst = op('votesAgainst', range=Quantity, label='Votes against the resolution')
votesFor = op('votesFor', range=Quantity, label='Number of votes in favour of the resolution')
wagon = op('wagon', range=Item, label='train carriage')
waistSize = op('waistSize', range=Quantity, label='waist size (μ)')
war = op('war', range=String, label='wars')
ward = op('ward', range=String, label='ward of a liechtenstein settlement')
water = op('water', range=String, label='water')
waterArea = op('waterArea', range=Quantity, label='area of water (m2)')
watercourse = op('watercourse', range=String, label='watercourse')
waterPercentage = op('waterPercentage', range=Quantity, label='water percentage of a place')
watershed = op('watershed', range=Quantity, label='watershed (m2)')
wavelength = op('wavelength', range=Quantity, label='wavelength (μ)')
weapon = op('weapon', range=Item, label='weapon')
websiteLabel = op('websiteLabel', range=Text, label='label of a website')
weddingParentsDate = op('weddingParentsDate', range=Time, label='Parents Wedding Date')
weight = op('weight', range=Quantity, label='weight (g)')
westPlace = op('westPlace', range=Item, label='west place')
whaDraft = op('whaDraft', range=String, label='wha draft')
whaDraftTeam = op('whaDraftTeam', range=Item, label='wha draft team')
whaDraftYear = op('whaDraftYear', range=Time, label='wha draft year')
wheelbase = op('wheelbase', range=Quantity, label='wheelbase (μ)')
wholeArea = op('wholeArea', range=Item, label='whole area')
width = op('width', range=Quantity, label='width (μ)')
widthQuote = op('widthQuote', range=String, label='width quote')
wikiPageCharacterSize = op('wikiPageCharacterSize', range=Quantity, label='Character size of wiki page')
wikiPageExtracted = op('wikiPageExtracted', range=Time, label='extraction datetime')
wikiPageID = op('wikiPageID', range=Quantity, label='Wikipage page ID')
wikiPageInDegree = op('wikiPageInDegree', range=Quantity, label='Wiki page in degree')
wikiPageLength = op('wikiPageLength', range=Quantity, label='page length (characters) of wiki page')
wikiPageLengthDelta = op('wikiPageLengthDelta', range=Quantity, label='Delta size of a revision with last one')
wikiPageModified = op('wikiPageModified', range=Time, label='Wikipage modification datetime')
wikiPageOutDegree = op('wikiPageOutDegree', range=Quantity, label='Wiki page out degree')
wikiPageRevisionID = op('wikiPageRevisionID', range=Quantity, label='Wikipage revision ID')
wikiPageUsesTemplate = op('wikiPageUsesTemplate', range=Item, label='wiki page uses template')
wilaya = op('wilaya', range=Item, label='wilaya')
wimbledonDouble = op('wimbledonDouble', range=String, label='wimbledon double')
wimbledonMixed = op('wimbledonMixed', range=String, label='wimbledon mixed')
wimbledonSingle = op('wimbledonSingle', range=String, label='wimbledon single')
wineRegion = op('wineRegion', range=Item, label='wine region')
wineYear = op('wineYear', range=Time, label='wine year')
wingArea = op('wingArea', range=Quantity, label='wing area (m2)')
wingspan = op('wingspan', range=Quantity, label='wingspan (μ)')
wins = op('wins', range=Quantity, label='wins')
winterAppearances = op('winterAppearances', range=Item, label='winter appearances')
winterTemperature = op('winterTemperature', range=Quantity, label='winter temperature (K)')
wordBefore = op('wordBefore', range=String, label='word before the country')
work = op('work', range=String, label='work')
workArea = op('workArea', range=Quantity, label='work area (m2)')
worldChampionTitleYear = op('worldChampionTitleYear', range=String, label='year of world champion title')
worldOpen = op('worldOpen', range=String, label='world open')
worldTeamCup = op('worldTeamCup', range=String, label='world team cup')
worldTournament = op('worldTournament', range=Item, label='world tournament')
worldTournamentBronze = op('worldTournamentBronze', range=Quantity, label='world tournament bronze')
worldTournamentGold = op('worldTournamentGold', range=Quantity, label='world tournament gold')
worldTournamentSilver = op('worldTournamentSilver', range=Quantity, label='world tournament silver')
worstDefeat = op('worstDefeat', range=String, label='worst defeat')
wptFinalTable = op('wptFinalTable', range=Quantity, label='wpt final table')
wptItm = op('wptItm', range=Quantity, label='wpt itm')
wptTitle = op('wptTitle', range=String, label='wpt title')
writer = op('writer', range=Item, label='auteur')
wsopItm = op('wsopItm', range=Quantity, label='wsop itm')
wsopWinYear = op('wsopWinYear', range=Time, label='wsop win year')
wsopWristband = op('wsopWristband', range=Quantity, label='wsop wristband')
year = op('year', range=Time, label='year')
yearElevationIntoNobility = op('yearElevationIntoNobility', range=String, label='year of elevation into the nobility')
yearOfConstruction = op('yearOfConstruction', range=Time, label='year of construction')
yearOfElectrification = op('yearOfElectrification', range=Time, label='year of electrification')
years = op('years', range=Time, label='years')
youthClub = op('youthClub', range=Item, label='youth club')
youthYears = op('youthYears', range=Time, label='youth years')
zdb = op('zdb', range=String, label='zdb')
zipCode = op('zipCode', range=String, label='zip code')
ابی_چرچ_کی_برکت = op('ابی_چرچ_کی_برکت', range=String, label='abbey church blessing')
انتظامی_اجتماعیت = op('انتظامی_اجتماعیت', range=Item, label='administrative collectivity')
انتظامی_درجہ = op('انتظامی_درجہ', range=String, label='administrative status')
انعام = op('انعام', range=Item, label='award')
اے_ایف_آئی_انعام = op('اے_ایف_آئی_انعام', range=Item, label='AFI Award')
جامعہ_کا_ناپ = op('جامعہ_کا_ناپ', range=Quantity, label='campus size (m2)')
جمع_کا_علاقہ = op('جمع_کا_علاقہ', range=Item, label='agglomeration area')
حصول_کی_تاریخ = op('حصول_کی_تاریخ', range=Time, label='date of acquirement')
خلاصہ = op('خلاصہ', range=Text, label='has abstract')
رسائی = op('رسائی', range=String, label='access')
رقبہ = op('رقبہ', range=Quantity, label='area')
رہائی_کی_تاریخ = op('رہائی_کی_تاریخ', range=Time, label='airdate')
طَنابی_گاڑی = op('طَنابی_گاڑی', range=Quantity, label='cable car')
فعال_سال_شروع_سال_Mgr = op('فعال_سال_شروع_سال_Mgr', range=Time, label='active years start year manager')
فعال_سال_کی_آخری_تاریخ_Mgr = op('فعال_سال_کی_آخری_تاریخ_Mgr', range=String, label='active years end date manager')
فعال_سال_کی_شروعات_کی_تاریخ = op('فعال_سال_کی_شروعات_کی_تاریخ', range=Time, label='active years start date')
فعال_کیسز = op('فعال_کیسز', range=Quantity, label='Active Cases')
فنکار = op('فنکار', range=Item, label='artist')
مجموعی_آبادی_کل = op('مجموعی_آبادی_کل', range=Quantity, label='agglomeration population total')
مخفف = op('مخفف', range=String, label='abbreviation')
مصنف = op('مصنف', range=Item, label='writer')
معاملہ = op('معاملہ', range=String, label='affair')
معاملہ = op('معاملہ', range=String, label='case')
پرہیز = op('پرہیز', range=Quantity, label='abstentions')
پیسنے_کے_قابل = op('پیسنے_کے_قابل', range=String, label='able to grind')
کتاب = op('کتاب', range=String, label='book')

__all__ = (
    'abbeychurchBlessing',
    'abbeychurchBlessingCharge',
    'abbreviation',
    'ableToGrind',
    'absoluteMagnitude',
    'abstentions',
    'abstract',
    'academicAdvisor',
    'academyAward',
    'acceleration',
    'access',
    'accessDate',
    'acquirementDate',
    'actingHeadteacher',
    'activeCases',
    'activeYears',
    'activeYearsEndDate',
    'activeYearsEndDateMgr',
    'activeYearsEndYear',
    'activeYearsEndYearMgr',
    'activeYearsStartDate',
    'activeYearsStartDateMgr',
    'activeYearsStartYear',
    'activeYearsStartYearMgr',
    'address',
    'adjacentSettlement',
    'administrativeCenter',
    'administrativeCollectivity',
    'administrativeDistrict',
    'administrativeHeadCity',
    'administrativeStatus',
    'administrator',
    'afdbId',
    'affair',
    'affiliate',
    'affiliation',
    'afiAward',
    'age',
    'agencyStationCode',
    'ageRange',
    'agglomeration',
    'agglomerationArea',
    'agglomerationDemographics',
    'agglomerationPopulation',
    'agglomerationPopulationTotal',
    'agglomerationPopulationYear',
    'aggregation',
    'aircraftAttack',
    'aircraftBomber',
    'aircraftElectronic',
    'aircraftFighter',
    'aircraftHelicopter',
    'aircraftHelicopterAttack',
    'aircraftHelicopterCargo',
    'aircraftHelicopterMultirole',
    'aircraftHelicopterObservation',
    'aircraftHelicopterTransport',
    'aircraftHelicopterUtility',
    'aircraftInterceptor',
    'aircraftPatrol',
    'aircraftRecon',
    'aircraftTrainer',
    'aircraftTransport',
    'aircraftType',
    'aircraftUser',
    'airDate',
    'airportUsing',
    'aitaCode',
    'albedo',
    'album',
    'albumRuntime',
    'alias',
    'allcinemaId',
    'allegiance',
    'almaMater',
    'alongside',
    'alpsGroup',
    'alpsMainPart',
    'alpsMajorSector',
    'alpsSection',
    'alpsSoiusaCode',
    'alpsSubgroup',
    'alpsSubsection',
    'alpsSupergroup',
    'alternativeName',
    'alternativeText',
    'alternativeTitle',
    'altitude',
    'alumni',
    'amateurDefeat',
    'amateurFight',
    'amateurKo',
    'amateurNoContest',
    'amateurTeam',
    'amateurTie',
    'amateurTitle',
    'amateurVictory',
    'amateurYear',
    'americanComedyAward',
    'amgid',
    'amsterdamCode',
    'analogChannel',
    'animal',
    'animator',
    'anniversary',
    'announcedFrom',
    'annualTemperature',
    'anthem',
    'aoCloassification',
    'apcPresident',
    'apoapsis',
    'apofocus',
    'apparentMagnitude',
    'appearance',
    'appearancesInLeague',
    'appearancesInNationalTeam',
    'appointer',
    'apprehended',
    'approvedByLowerParliament',
    'approvedByUpperParliament',
    'approximateCalories',
    'apskritis',
    'architect',
    'architectualBureau',
    'architecturalMovement',
    'area',
    'areaCode',
    'areaDate',
    'areaLand',
    'areaMetro',
    'areaOfCatchment',
    'areaOfCatchmentQuote',
    'areaOfSearch',
    'areaQuote',
    'areaRank',
    'areaRural',
    'areaTotal',
    'areaTotalRanking',
    'areaUrban',
    'areaWater',
    'argueDate',
    'arielAward',
    'arm',
    'army',
    'arrestDate',
    'arrondissement',
    'artery',
    'artificialSnowArea',
    'artist',
    'artistFunction',
    'artisticFunction',
    'artPatron',
    'ascent',
    'asiaChampionship',
    'aSide',
    'assets',
    'assetUnderManagement',
    'associate',
    'associatedAct',
    'associatedBand',
    'associatedMusicalArtist',
    'associatedRocket',
    'associateEditor',
    'associateStar',
    'associationOfLocalGovernment',
    'astrazenca',
    'astrazencaCumul',
    'asWikiText',
    'atcCode',
    'atcPrefix',
    'atcSuffix',
    'athleticsDiscipline',
    'atomicNumber',
    'atPage',
    'atRowNumber',
    'attorneyGeneral',
    'aunt',
    'australiaOpenDouble',
    'australiaOpenMixed',
    'australiaOpenSingle',
    'author',
    'authorityMandate',
    'authorityTitle',
    'automobileModel',
    'automobilePlatform',
    'average',
    'averageAnnualGeneration',
    'averageClassSize',
    'averageDepth',
    'averageDepthQuote',
    'averageSpeed',
    'avgRevSizePerMonth',
    'avgRevSizePerYear',
    'avifaunaPopulation',
    'award',
    'awardName',
    'awayColourHexCode',
    'background',
    'backhand',
    'badGuy',
    'baftaAward',
    'band',
    'bandMember',
    'barangays',
    'barPassRate',
    'basedOn',
    'battery',
    'battingSide',
    'battle',
    'battleHonours',
    'bbr',
    'beatifiedBy',
    'beatifiedDate',
    'beatifiedPlace',
    'bedCount',
    'believers',
    'beltwayCity',
    'bestFinish',
    'bestLap',
    'bestRankDouble',
    'bestRankSingle',
    'bestWsopRank',
    'bestYearWsop',
    'bgafdId',
    'bibsysId',
    'bicycleInformation',
    'biggestCity',
    'bigPoolRecord',
    'billed',
    'bioavailability',
    'bioclimate',
    'bird',
    'birthDate',
    'birthName',
    'birthPlace',
    'birthYear',
    'blackLongDistancePisteNumber',
    'blackSkiPisteNumber',
    'blazon',
    'blazonCaption',
    'blazonLink',
    'blazonRatio',
    'block',
    'bloodGroup',
    'blueLongDistancePisteNumber',
    'blueSkiPisteNumber',
    'bnfId',
    'bodyDiscovered',
    'boilingPoint',
    'book',
    'booster',
    'border',
    'borough',
    'bourgmestre',
    'bowlingSide',
    'bowlRecord',
    'boxerStyle',
    'bpnId',
    'brainInfoNumber',
    'brainInfoType',
    'branchFrom',
    'branchTo',
    'brand',
    'breeder',
    'bridgeCarries',
    'brinCode',
    'britishComedyAwards',
    'britishOpen',
    'broadcastArea',
    'broadcastNetwork',
    'broadcastRepeater',
    'broadcastStationClass',
    'broadcastTranslator',
    'bronzeMedalDouble',
    'bronzeMedalist',
    'bronzeMedalMixed',
    'bronzeMedalSingle',
    'brother',
    'bSide',
    'budget',
    'budgetYear',
    'building',
    'buildingEndDate',
    'buildingEndYear',
    'buildingStartDate',
    'buildingStartYear',
    'bustSize',
    'bustWaistHipSize',
    'cableCar',
    'callSign',
    'callsignMeaning',
    'campusSize',
    'campusType',
    'canBaggageChecked',
    'cannonNumber',
    'canonizedBy',
    'canonizedDate',
    'canonizedPlace',
    'canton',
    'capacity',
    'capacityFactor',
    'capital',
    'capitalCoordinates',
    'capitalCountry',
    'capitalDistrict',
    'capitalElevation',
    'capitalMountain',
    'capitalPlace',
    'capitalRegion',
    'captureDate',
    'carbohydrate',
    'carcinogen',
    'careerPoints',
    'careerPrizeMoney',
    'careerStation',
    'cargoFuel',
    'cargoGas',
    'cargoWater',
    'carNumber',
    'case',
    'casNumber',
    'casSupplemental',
    'casualties',
    'catch',
    'caterer',
    'catholicPercentage',
    'causalties',
    'causeOfDeath',
    'ccaState',
    'ceeb',
    'ceiling',
    'cemetery',
    'censusYear',
    'center',
    'centuryBreaks',
    'ceo',
    'ceremonialCounty',
    'certification',
    'certificationDate',
    'cesarAward',
    'chain',
    'chairman',
    'chairmanTitle',
    'chairperson',
    'champion',
    'championInDouble',
    'championInDoubleFemale',
    'championInDoubleMale',
    'championInMixedDouble',
    'championInSingle',
    'championInSingleFemale',
    'championInSingleMale',
    'championships',
    'chancellor',
    'channel',
    'chaplain',
    'characterInPlay',
    'chEBI',
    'chef',
    'chEMBL',
    'chemicalFormula',
    'chemSpiderId',
    'chief',
    'chiefEditor',
    'chiefPlace',
    'child',
    'childOrganisation',
    'choreographer',
    'chorusCharacterInPlay',
    'christeningDate',
    'chromosome',
    'cinematography',
    'circle',
    'circuitLength',
    'circuitName',
    'circulation',
    'circumcised',
    'cites',
    'city',
    'cityLink',
    'cityRank',
    'citySince',
    'cityType',
    'classes',
    'classification',
    'climbUpNumber',
    'closed',
    'closeTo',
    'closingDate',
    'closingFilm',
    'closingYear',
    'clothingSize',
    'clothSize',
    'club',
    'clubsRecordGoalscorer',
    'cmpEvaDuration',
    'cmykCoordinateBlack',
    'cmykCoordinateCyanic',
    'cmykCoordinateMagenta',
    'cmykCoordinateYellow',
    'co2Emission',
    'coach',
    'coachClub',
    'coachedTeam',
    'coachingRecord',
    'coachSeason',
    'coalition',
    'coastLength',
    'coastLine',
    'code',
    'codeBook',
    'codeDistrict',
    'codeIndex',
    'codeListOfHonour',
    'codeMemorial',
    'codeMunicipalMonument',
    'coden',
    'codeNationalMonument',
    'codeProvincialMonument',
    'codeSettlement',
    'codeStockExchange',
    'coemperor',
    'coExecutiveProducer',
    'collaboration',
    'colleague',
    'collection',
    'college',
    'collegeHof',
    'colonialName',
    'colorChart',
    'colour',
    'colourHexCode',
    'colourName',
    'combatant',
    'comic',
    'comitat',
    'command',
    'commandant',
    'commander',
    'commandModule',
    'commandStructure',
    'comment',
    'commissioner',
    'commissionerDate',
    'commissioningDate',
    'committee',
    'commonName',
    'commune',
    'communityIsoCode',
    'company',
    'comparable',
    'competition',
    'competitionTitle',
    'compiler',
    'completionDate',
    'complexity',
    'complications',
    'component',
    'composer',
    'compressionRatio',
    'configuration',
    'confirmedCases',
    'conflict',
    'consecration',
    'conservationStatus',
    'conservationStatusSystem',
    'constituencyDistrict',
    'contest',
    'continent',
    'continentalTournament',
    'continentalTournamentBronze',
    'continentalTournamentGold',
    'continentalTournamentSilver',
    'continentRank',
    'contractAward',
    'contractor',
    'convictionDate',
    'copilote',
    'coProducer',
    'coronationDate',
    'cosparId',
    'cost',
    'costumeDesigner',
    'council',
    'councilArea',
    'country',
    'countryCode',
    'countryOrigin',
    'countryRank',
    'countryWithFirstAstronaut',
    'countryWithFirstSatellite',
    'countryWithFirstSatelliteLaunched',
    'countryWithFirstSpaceflight',
    'county',
    'course',
    'courseArea',
    'cousurper',
    'coverArtist',
    'created',
    'creationChristianBishop',
    'creationYear',
    'creativeDirector',
    'creator',
    'creatorOfDish',
    'credit',
    'crew',
    'crewMember',
    'crews',
    'crewSize',
    'criminalCharge',
    'criteria',
    'crosses',
    'crownDependency',
    'cuisine',
    'cultivatedVariety',
    'curator',
    'currency',
    'currencyCode',
    'currentCity',
    'currentLeague',
    'currentlyUsedFor',
    'currentMember',
    'currentPartner',
    'currentRank',
    'currentRecord',
    'currentStatus',
    'currentTeam',
    'currentTeamManager',
    'currentTeamMember',
    'currentWorldChampion',
    'custodian',
    'cylinderBore',
    'cylinderCount',
    'dailyVaccinationsPerMillion',
    'dailyVaccinationsRaw',
    'daira',
    'dam',
    'damage',
    'damsire',
    'danseCompetition',
    'danseScore',
    'date',
    'dateAct',
    'dateAgreement',
    'dateBudget',
    'dateClosed',
    'dateCompleted',
    'dateConstruction',
    'dateExtended',
    'dateLastUpdated',
    'dateOfAbandonment',
    'dateOfBurial',
    'dateUnveiled',
    'dateUse',
    'daughter',
    'day',
    'dbnlCodeDutch',
    'dcc',
    'deadInFightDate',
    'deadInFightPlace',
    'dean',
    'deanery',
    'deathAge',
    'deathDate',
    'deathPlace',
    'deaths',
    'deathYear',
    'debut',
    'debutTeam',
    'debutWork',
    'dec',
    'decay',
    'decideDate',
    'declination',
    'decommissioningDate',
    'deFactoLanguage',
    'defeat',
    'defeatAsMgr',
    'definition',
    'defunct',
    'delegateMayor',
    'delegation',
    'deliveryDate',
    'deme',
    'demographics',
    'demographicsAsOf',
    'demolitionDate',
    'demolitionYear',
    'demonym',
    'density',
    'department',
    'departmentCode',
    'departmentPosition',
    'depictionDescription',
    'depth',
    'depthQuote',
    'depths',
    'deputy',
    'derivative',
    'derivedWord',
    'description',
    'designCompany',
    'designer',
    'destination',
    'destructionDate',
    'detectionMethod',
    'detractor',
    'developer',
    'diameter',
    'digitalChannel',
    'digitalSubChannel',
    'diocese',
    'diploma',
    'director',
    'disappearanceDate',
    'disbanded',
    'discharge',
    'dischargeAverage',
    'disciple',
    'discontinued',
    'discovered',
    'discoverer',
    'discovery',
    'disease',
    'diseasesDb',
    'diseasesDB',
    'displacement',
    'dissolutionDate',
    'dissolutionYear',
    'dissolved',
    'dist_ly',
    'dist_pc',
    'distance',
    'distanceLaps',
    'distanceToBelfast',
    'distanceToCapital',
    'distanceToCardiff',
    'distanceToCharingCross',
    'distanceToDouglas',
    'distanceToDublin',
    'distanceToEdinburgh',
    'distanceToLondon',
    'distanceToNearestCity',
    'distanceTraveled',
    'distributingCompany',
    'distributingLabel',
    'distributor',
    'district',
    'dockedTime',
    'doctoralAdvisor',
    'doctoralStudent',
    'documentDesignation',
    'documentNumber',
    'dorlandsId',
    'dorlandsPrefix',
    'dorlandsSuffix',
    'dose',
    'dosesFirst',
    'dosesSecond',
    'draft',
    'draftLeague',
    'draftPick',
    'draftPosition',
    'draftRound',
    'draftTeam',
    'draftYear',
    'drainsFrom',
    'drainsTo',
    'drama',
    'dressCode',
    'drug',
    'drugbank',
    'dryCargo',
    'dubber',
    'duration',
    'dutchArtworkCode',
    'dutchCOROPCode',
    'dutchMIPCode',
    'dutchNAIdentifier',
    'dutchPPNCode',
    'dutchRKDCode',
    'dutchWinkelID',
    'eastPlace',
    'ecNumber',
    'editing',
    'editor',
    'editorTitle',
    'educationPlace',
    'effectiveRadiatedPower',
    'egafdId',
    'einecsNumber',
    'ekatteCode',
    'electionDate',
    'electionDateLeader',
    'electionMajority',
    'elementAbove',
    'elementBlock',
    'elementGroup',
    'elementPeriod',
    'elevation',
    'elevationQuote',
    'elevatorCount',
    'elo',
    'eloRecord',
    'emblem',
    'eMedicineSubject',
    'eMedicineTopic',
    'emmyAward',
    'employer',
    'employersCelebration',
    'end',
    'endangeredSince',
    'endCareer',
    'endDate',
    'endDateTime',
    'endingTheme',
    'endOccupation',
    'endowment',
    'endPoint',
    'endYear',
    'endYearOfInsertion',
    'endYearOfSales',
    'enemy',
    'engine',
    'engineer',
    'enginePower',
    'ensembl',
    'enshrinedDeity',
    'entourage',
    'entrezgene',
    'episode',
    'episodeNumber',
    'epoch',
    'eptFinalTable',
    'eptItm',
    'eptTitle',
    'equity',
    'eruption',
    'eruptionYear',
    'escalafon',
    'escapeVelocity',
    'espnId',
    'established',
    'establishment',
    'eTeatrId',
    'ethnicGroup',
    'ethnicGroupsInYear',
    'ethnicity',
    'eurobabeIndexId',
    'europeanChampionship',
    'europeanUnionEntranceDate',
    'event',
    'eventDate',
    'eventDescription',
    'executiveHeadteacher',
    'executiveProducer',
    'exhibition',
    'expedition',
    'externalOrnament',
    'extinctionDate',
    'extinctionYear',
    'eyeColor',
    'eyeColour',
    'eyes',
    'faaLocationIdentifier',
    'facilityId',
    'facultySize',
    'failedLaunches',
    'family',
    'familyMember',
    'fansgroup',
    'fareZone',
    'fastestDriver',
    'fastestDriverCountry',
    'fastestDriverTeam',
    'fastestLap',
    'fat',
    'fatalityRate',
    'fate',
    'father',
    'fauna',
    'fc',
    'fcRuns',
    'fdaUniiCode',
    'feastDay',
    'feat',
    'feature',
    'features',
    'featuring',
    'fedCup',
    'federalState',
    'federation',
    'fees',
    'fibahof',
    'fight',
    'fighter',
    'fileExtension',
    'filename',
    'fileSize',
    'fileURL',
    'fillingStation',
    'film',
    'filmAudioType',
    'filmColourType',
    'filmFareAward',
    'filmNumber',
    'filmPolskiId',
    'filmRuntime',
    'filmVersion',
    'finalFlight',
    'finalLost',
    'finalLostDouble',
    'finalLostSingle',
    'finalLostTeam',
    'finalPublicationDate',
    'finalPublicationYear',
    'fipsCode',
    'firstAirDate',
    'firstAppearance',
    'firstAscent',
    'firstAscentPerson',
    'firstAscentYear',
    'firstBroadcast',
    'firstDriver',
    'firstDriverCountry',
    'firstDriverTeam',
    'firstFlight',
    'firstFlightEndDate',
    'firstFlightStartDate',
    'firstGame',
    'firstLaunch',
    'firstLaunchDate',
    'firstLaunchRocket',
    'firstLeader',
    'firstMention',
    'firstOlympicEvent',
    'firstOwner',
    'firstPlace',
    'firstPopularVote',
    'firstProMatch',
    'firstPublicationDate',
    'firstPublicationYear',
    'firstPublisher',
    'firstRace',
    'firstWin',
    'firstWinner',
    'flag',
    'flagBearer',
    'flagBorder',
    'flagCaption',
    'flagLink',
    'flagSize',
    'flashPoint',
    'floodingDate',
    'floorArea',
    'floorCount',
    'flora',
    'flower',
    'flyingHours',
    'foalDate',
    'followingEvent',
    'foot',
    'footedness',
    'forces',
    'formationDate',
    'formationYear',
    'formerBandMember',
    'formerBroadcastNetwork',
    'formerCallsign',
    'formerChannel',
    'formerChoreographer',
    'formerCoach',
    'formerHighschool',
    'formerName',
    'formerPartner',
    'formerTeam',
    'formula',
    'fossil',
    'foundation',
    'foundationPlace',
    'foundedBy',
    'founder',
    'foundingDate',
    'foundingYear',
    'fourthCommander',
    'frazioni',
    'free',
    'freeDanseScore',
    'freeFlightTime',
    'freeLabel',
    'freeProgCompetition',
    'freeProgScore',
    'freeScoreCompetition',
    'frequency',
    'frequencyOfPublication',
    'frequentlyUpdated',
    'friend',
    'frontierLength',
    'frozen',
    'fuelCapacity',
    'fuelConsumption',
    'fuelTypeName',
    'fullCompetition',
    'fullScore',
    'functionEndDate',
    'functionEndYear',
    'functionStartDate',
    'functionStartYear',
    'fundedBy',
    'galicianSpeakersDate',
    'galicianSpeakersPercentage',
    'galleryItem',
    'gameArtist',
    'gameModus',
    'games',
    'garrison',
    'gasChambers',
    'gaudiAward',
    'gdpPerCapita',
    'geminiAward',
    'geneLocation',
    'geneLocationEnd',
    'geneLocationStart',
    'generalCouncil',
    'generalManager',
    'generationUnits',
    'geneReviewsId',
    'geneReviewsName',
    'genomeDB',
    'genre',
    'geolocDepartment',
    'geolocDual',
    'geologicPeriod',
    'geology',
    'giniCoefficient',
    'giniCoefficientAsOf',
    'giniCoefficientRanking',
    'glycemicIndex',
    'gnisCode',
    'gnl',
    'goalsInLeague',
    'goalsInNationalTeam',
    'goldenCalfAward',
    'goldenGlobeAward',
    'goldenRaspberryAward',
    'goldMedalDouble',
    'goldMedalist',
    'goldMedalMixed',
    'goldMedalSingle',
    'governingBody',
    'governmentCountry',
    'governmentElevation',
    'governmentMountain',
    'governmentPlace',
    'governmentRegion',
    'governmentType',
    'governor',
    'governorate',
    'governorGeneral',
    'goyaAward',
    'gradName',
    'gradNum',
    'grammyAward',
    'grandsire',
    'grave',
    'grayPage',
    'graySubject',
    'greekName',
    'greenLongDistancePisteNumber',
    'greenSkiPisteNumber',
    'gridReference',
    'grindingCapability',
    'gross',
    'grossDomesticProduct',
    'grossDomesticProductAsOf',
    'grossDomesticProductNominalPerCapita',
    'grossDomesticProductPerPeople',
    'grossDomesticProductPurchasingPowerParityPerCapita',
    'grossDomesticProductRank',
    'ground',
    'groundsForLiquidation',
    'groupCommemorated',
    'growingGrape',
    'guest',
    'gun',
    'hairColor',
    'hairColour',
    'hairs',
    'hallOfFame',
    'handisport',
    'hasAbsorbedMunicipality',
    'hasAnnotation',
    'hasInsidePlace',
    'hasJunctionWith',
    'hasKMLData',
    'hasNaturalBust',
    'hasOutsidePlace',
    'head',
    'headChef',
    'headLabel',
    'headOfFamily',
    'headquarter',
    'headteacher',
    'height',
    'heightAboveAverageTerrain',
    'heightAgainst',
    'heightAttack',
    'heir',
    'heisman',
    'hgncid',
    'highest',
    'highestAltitude',
    'highestBreak',
    'highestBuildingInYear',
    'highestMountain',
    'highestPlace',
    'highestPoint',
    'highestPointIsland',
    'highestRank',
    'highestRegion',
    'highestState',
    'highschool',
    'hipSize',
    'historicalMap',
    'historicalName',
    'historicalRegion',
    'hof',
    'homage',
    'homeArena',
    'homeColourHexCode',
    'homeport',
    'homeStadium',
    'hometown',
    'hopmanCup',
    'horseRidingDiscipline',
    'house',
    'hraState',
    'hsvCoordinateHue',
    'hsvCoordinateSaturation',
    'hsvCoordinateValue',
    'hubAirport',
    'humanDevelopmentIndex',
    'humanDevelopmentIndexAsOf',
    'humanDevelopmentIndexRank',
    'hybrid',
    'iafdId',
    'iataAirlineCode',
    'iataLocationIdentifier',
    'ibdbId',
    'icaoAirlineCode',
    'icaoLocationIdentifier',
    'icd1',
    'icd10',
    'icd9',
    'icdo',
    'iconographicAttributes',
    'id',
    'idAllocine',
    'identificationSymbol',
    'ideology',
    'idNumber',
    'iftaAward',
    'iihfHof',
    'illiteracy',
    'illustrator',
    'imageSize',
    'imdbId',
    'impactFactor',
    'impactFactorAsOf',
    'importantStation',
    'imposedDanseCompetition',
    'imposedDanseScore',
    'inCemetery',
    'inchi',
    'inclination',
    'income',
    'incumbent',
    'individualisedGnd',
    'individualisedPnd',
    'infantMortality',
    'inflow',
    'information',
    'informationName',
    'ingredientName',
    'initiallyUsedFor',
    'inn',
    'innervates',
    'inscription',
    'inseeCode',
    'installedCapacity',
    'institution',
    'instrument',
    'intercommunality',
    'interest',
    'internationally',
    'internationalPhonePrefix',
    'internationalPhonePrefixLabel',
    'introduced',
    'introductionDate',
    'iobdbId',
    'isbn',
    'isCityState',
    'isHandicappedAccessible',
    'isil',
    'island',
    'isMinorRevision',
    'isniId',
    'iso31661Code',
    'iso6391Code',
    'iso6392Code',
    'iso6393Code',
    'isoCode',
    'isoCodeRegion',
    'isPartOfAnatomicalStructure',
    'isPartOfMilitaryConflict',
    'isPartOfName',
    'isPartOfWineRegion',
    'isPeerReviewed',
    'isRouteStop',
    'issDockings',
    'issn',
    'ist',
    'istat',
    'italicTitle',
    'ithfDate',
    'iucnCategory',
    'iupacName',
    'jockey',
    'jointCommunity',
    'jstor',
    'judge',
    'juniorTeam',
    'juniorYearsEndYear',
    'juniorYearsStartYear',
    'jureLanguage',
    'jutsu',
    'kegg',
    'keyPerson',
    'khlDraft',
    'khlDraftTeam',
    'khlDraftYear',
    'killedBy',
    'kindOfCoordinate',
    'kindOfCriminal',
    'kindOfCriminalAction',
    'kindOfRock',
    'kinOfLanguage',
    'ko',
    'lahHof',
    'lake',
    'land',
    'landArea',
    'landeshauptmann',
    'landingDate',
    'landingSite',
    'landingVehicle',
    'landPercentage',
    'landRegistryCode',
    'landskap',
    'landtag',
    'landtagMandate',
    'language',
    'languageCode',
    'languageRegulator',
    'largestCity',
    'largestMetro',
    'largestSettlement',
    'largestWin',
    'lastAirDate',
    'lastElectionDate',
    'lastFamilyMember',
    'lastFlight',
    'lastFlightEndDate',
    'lastFlightStartDate',
    'lastLaunch',
    'lastLaunchDate',
    'lastLaunchRocket',
    'lastPosition',
    'lastProMatch',
    'lastPublicationDate',
    'lastRace',
    'lastSeason',
    'lastWin',
    'laterality',
    'latestElection',
    'latestPreviewDate',
    'latestPreviewVersion',
    'latestReleaseDate',
    'latestReleaseVersion',
    'latinName',
    'launch',
    'launchDate',
    'launches',
    'launchPad',
    'launchSite',
    'laurenceOlivierAward',
    'lawCountry',
    'layingDown',
    'lcc',
    'lccn',
    'lccnId',
    'lchfDraft',
    'lchfDraftTeam',
    'lchfDraftYear',
    'leader',
    'leaderFunction',
    'leaderName',
    'leadership',
    'leaderTitle',
    'leadTeam',
    'leadYear',
    'league',
    'leagueManager',
    'leftChild',
    'leftTributary',
    'legalArrondissement',
    'legalArticle',
    'legislativePeriodName',
    'legislature',
    'length',
    'lengthQuote',
    'lengthReference',
    'lethalOnChickens',
    'lethalOnMice',
    'lethalOnRabbits',
    'lethalOnRats',
    'liberationDate',
    'libretto',
    'licenceLetter',
    'licenceNumber',
    'licenceNumberLabel',
    'licensee',
    'lieutenancy',
    'lieutenancyArea',
    'lieutenant',
    'lifeExpectancy',
    'limit',
    'lineLength',
    'linkedSpace',
    'linkedTo',
    'littlePoolRecord',
    'livingPlace',
    'loadLimit',
    'locality',
    'localization',
    'localizationThumbnailCaption',
    'localPhonePrefix',
    'locatedInArea',
    'location',
    'locationCity',
    'locationCountry',
    'locationIdentifier',
    'locationName',
    'locomotive',
    'locusSupplementaryData',
    'logo',
    'longDistancePisteKilometre',
    'longDistancePisteNumber',
    'longName',
    'longtype',
    'lowerAge',
    'lowerEarthOrbitPayload',
    'lowest',
    'lowestAltitude',
    'lowestMountain',
    'lowestPlace',
    'lowestPoint',
    'lowestRegion',
    'lowestState',
    'lunarEvaTime',
    'lunarLandingSite',
    'lunarModule',
    'lunarOrbitTime',
    'lunarRover',
    'lunarSampleMass',
    'lunarSurfaceTime',
    'lymph',
    'lyrics',
    'magazine',
    'maidenFlight',
    'maidenFlightRocket',
    'maidenVoyage',
    'mainArtist',
    'mainBuilding',
    'mainCharacter',
    'mainFamilyBranch',
    'mainIsland',
    'mainIslands',
    'mainspan',
    'majorIsland',
    'majorityFloorLeader',
    'majorityLeader',
    'makeupArtist',
    'managementCountry',
    'managementElevation',
    'managementMountain',
    'managementPlace',
    'managementRegion',
    'manager',
    'managerClub',
    'managerTitle',
    'managerYears',
    'managerYearsEndYear',
    'managerYearsStartYear',
    'managingEditor',
    'mandate',
    'manufactory',
    'manufacturer',
    'mapCaption',
    'mapDescription',
    'march',
    'marketCapitalisation',
    'mascot',
    'mass',
    'massif',
    'matchPoint',
    'max',
    'maxAbsoluteMagnitude',
    'maxApparentMagnitude',
    'maximumArea',
    'maximumAreaQuote',
    'maximumBoatBeam',
    'maximumBoatLength',
    'maximumDepth',
    'maximumDepthQuote',
    'maximumDischarge',
    'maximumElevation',
    'maximumInclination',
    'maximumTemperature',
    'maxTime',
    'mayor',
    'mayorArticle',
    'mayorCouncillor',
    'mayorFunction',
    'mayorMandate',
    'mayorTitle',
    'mbaId',
    'meaning',
    'meanRadius',
    'meanTemperature',
    'measurements',
    'medalist',
    'mediaItem',
    'medicalSpecialty',
    'medlinePlus',
    'meetingBuilding',
    'meetingCity',
    'meetingRoad',
    'meltingPoint',
    'member',
    'memberOfParliament',
    'membership',
    'membershipAsOf',
    'mentor',
    'mergedSettlement',
    'mergedWith',
    'mergerDate',
    'meshId',
    'meshName',
    'meshNumber',
    'messierName',
    'metropolitanBorough',
    'mgiid',
    'militaryBranch',
    'militaryCommand',
    'militaryFunction',
    'militaryGovernment',
    'militaryService',
    'militaryUnit',
    'militaryUnitSize',
    'millsCodeBE',
    'millsCodeDutch',
    'millsCodeNL',
    'millsCodeNLVerdwenen',
    'millsCodeNLWindmotoren',
    'millSpan',
    'min',
    'minimumArea',
    'minimumAreaQuote',
    'minimumDischarge',
    'minimumElevation',
    'minimumInclination',
    'minimumTemperature',
    'minister',
    'minority',
    'minorityFloorLeader',
    'minorityLeader',
    'minTime',
    'mirDockings',
    'mission',
    'missionDuration',
    'missions',
    'model',
    'modelEndDate',
    'modelEndYear',
    'modelLineVehicle',
    'modelStartDate',
    'modelStartYear',
    'moderna',
    'modernaCumul',
    'molarMass',
    'molecularWeight',
    'monarch',
    'month',
    'mood',
    'mostDownPoint',
    'mostSuccessfulPlayer',
    'mother',
    'motive',
    'motto',
    'mount',
    'mountainRange',
    'mouthCountry',
    'mouthDistrict',
    'mouthElevation',
    'mouthMountain',
    'mouthPlace',
    'mouthRegion',
    'mouthState',
    'movie',
    'mukhtar',
    'municipality',
    'municipalityAbsorbedBy',
    'municipalityCode',
    'municipalityRenamedTo',
    'municipalityType',
    'museum',
    'musicalArtist',
    'musicalBand',
    'musicalKey',
    'musicBand',
    'musicBrainzArtistId',
    'musicBy',
    'musicComposer',
    'musicFormat',
    'musicFusionGenre',
    'musicians',
    'musicSubgenre',
    'muteCharacterInPlay',
    'mvp',
    'naacpImageAward',
    'name',
    'nameAsOf',
    'nameDay',
    'namedByLanguage',
    'nameInCantoneseChinese',
    'nameInHangulKorean',
    'nameInHanjaKorean',
    'nameInJapanese',
    'nameInMindongyuChinese',
    'nameInMinnanyuChinese',
    'nameInPinyinChinese',
    'nameInSimplifiedChinese',
    'nameInTraditionalChinese',
    'nameInWadeGilesChinese',
    'names',
    'narrator',
    'nation',
    'nationalChampionship',
    'nationalFilmAward',
    'nationality',
    'nationalRanking',
    'nationalTeam',
    'nationalTeamMatchPoint',
    'nationalTeamYear',
    'nationalTopographicSystemMapNumber',
    'nationalTournament',
    'nationalTournamentBronze',
    'nationalTournamentGold',
    'nationalTournamentSilver',
    'nationalYears',
    'nbRevPerMonth',
    'nbRevPerYear',
    'nbUniqueContrib',
    'ncaaSeason',
    'ncaaTeam',
    'ncbhof',
    'nciId',
    'ndlId',
    'nearestCity',
    'neighboringMunicipality',
    'neighbourConstellations',
    'neighbourhood',
    'neighbourRegion',
    'nerve',
    'netIncome',
    'network',
    'networth',
    'newspaper',
    'nextEntity',
    'nextEvent',
    'nextMission',
    'nextTrackNumber',
    'nflCode',
    'nflSeason',
    'nflTeam',
    'ngcName',
    'nisCode',
    'nlaId',
    'nndbId',
    'nobelLaureates',
    'noContest',
    'nominee',
    'nonProfessionalCareer',
    'nord',
    'northEastPlace',
    'northPlace',
    'northWestPlace',
    'notableCommander',
    'notableFeatures',
    'notableStudent',
    'notableWork',
    'note',
    'noteOnPlaceOfBurial',
    'noteOnRestingPlace',
    'notes',
    'notifyDate',
    'notSolubleIn',
    'novel',
    'nrhpReferenceNumber',
    'nssdcId',
    'number',
    'numberBuilt',
    'numberOfAcademicStaff',
    'numberOfAlbums',
    'numberOfArrondissement',
    'numberOfBombs',
    'numberOfBronzeMedalsWon',
    'numberOfCanton',
    'numberOfCantons',
    'numberOfCapitalDeputies',
    'numberOfCity',
    'numberOfClasses',
    'numberOfClassesWithResource',
    'numberOfClubs',
    'numberOfCollectionItems',
    'numberOfCompetitors',
    'numberOfCounties',
    'numberOfCountries',
    'numberOfCrew',
    'numberOfDeaths',
    'numberOfDependency',
    'numberOfDisambiguates',
    'numberOfDistrict',
    'numberOfDistricts',
    'numberOfDoctoralStudents',
    'numberOfDoors',
    'numberOfEmployees',
    'numberOfEntrances',
    'numberOfEpisodes',
    'numberOfEtoilesMichelin',
    'numberOfFederalDeputies',
    'numberOfFilms',
    'numberOfGoals',
    'numberOfGoldMedalsWon',
    'numberOfGraduateStudents',
    'numberOfGraves',
    'numberOfHoles',
    'numberOfHouses',
    'numberOfIndegree',
    'numberOfIntercommunality',
    'numberOfIsland',
    'numberOfIslands',
    'numberOfLanes',
    'numberOfLaps',
    'numberOfLaunches',
    'numberOfLawyers',
    'numberOfLifts',
    'numberOfLines',
    'numberOfLiveAlbums',
    'numberOfLocations',
    'numberOfMatches',
    'numberOfMembers',
    'numberOfMembersAsOf',
    'numberOfMinistries',
    'numberOfMunicipalities',
    'numberOfMusicalArtistEntities',
    'numberOfMusicalArtistInstrument',
    'numberOfMusicalArtistStyle',
    'numberOfNeighbourhood',
    'numberOfNewlyIntroducedSports',
    'numberOfOffices',
    'numberOfOfficials',
    'numberOfOrbits',
    'numberOfOutdegree',
    'numberOfPads',
    'numberOfPages',
    'numberOfParkingSpaces',
    'numberOfParticipatingAthletes',
    'numberOfParticipatingFemaleAthletes',
    'numberOfParticipatingMaleAthletes',
    'numberOfParticipatingNations',
    'numberOfPassengers',
    'numberOfPeopleAttending',
    'numberOfPeopleLicensed',
    'numberOfPersonBornInPlace',
    'numberOfPersonEntities',
    'numberOfPersonFromUniversity',
    'numberOfPersonInOccupation',
    'numberOfPiersInWater',
    'numberOfPixels',
    'numberOfPlatformLevels',
    'numberOfPlayers',
    'numberOfPostgraduateStudents',
    'numberOfPredicates',
    'numberOfProfessionals',
    'numberOfProperties',
    'numberOfPropertiesUsed',
    'numberOfReactors',
    'numberOfRedirectedResource',
    'numberOfResource',
    'numberOfResourceOfClass',
    'numberOfResourceOfType',
    'numberOfResourceWithType',
    'numberOfRestaurants',
    'numberOfRockets',
    'numberOfRooms',
    'numberOfRun',
    'numberOfSeasons',
    'numberOfSeats',
    'numberOfSeatsInParliament',
    'numberOfSettlement',
    'numberOfSettlementsInCountry',
    'numberOfSilverMedalsWon',
    'numberOfSoccerPlayerInCountryRepre',
    'numberOfSoccerPlayersBornInPlace',
    'numberOfSoccerPlayersInTeam',
    'numberOfSpans',
    'numberOfSpeakers',
    'numberOfSports',
    'numberOfSportsEvents',
    'numberOfStaff',
    'numberOfStars',
    'numberOfStateDeputies',
    'numberOfStations',
    'numberOfStores',
    'numberOfStudents',
    'numberOfStudioAlbums',
    'numberOfSuites',
    'numberOfTeams',
    'numberOfTracks',
    'numberOfTrails',
    'numberOfTriples',
    'numberOfTurns',
    'numberOfUndergraduateStudents',
    'numberOfUniqeResources',
    'numberOfUseOfProperty',
    'numberOfVehicles',
    'numberOfVillages',
    'numberOfVineyards',
    'numberOfVisitors',
    'numberOfVisitorsAsOf',
    'numberOfVolumes',
    'numberOfVolunteers',
    'numberOfWineries',
    'numberSold',
    'nutsCode',
    'observatory',
    'occupation',
    'oclc',
    'odor',
    'offeredClasses',
    'office',
    'officerInCharge',
    'officialLanguage',
    'officialName',
    'officialOpenedBy',
    'officialSchoolColour',
    'ofsCode',
    'okatoCode',
    'oldcode',
    'oldDistrict',
    'oldName',
    'oldProvince',
    'oldTeamCoached',
    'olivierAward',
    'olympicGames',
    'olympicGamesBronze',
    'olympicGamesGold',
    'olympicGamesSilver',
    'olympicGamesWins',
    'olympicOathSwornBy',
    'olympicOathSwornByAthlete',
    'olympicOathSwornByJudge',
    'omim',
    'onChromosome',
    'ons',
    'openAccessContent',
    'openingDate',
    'openingFilm',
    'openingTheme',
    'openingYear',
    'operatingIncome',
    'opponent',
    'orbitalEccentricity',
    'orbitalFlights',
    'orbitalInclination',
    'orbitalPeriod',
    'orbits',
    'orcidId',
    'orderDate',
    'orderInOffice',
    'ordination',
    'organ',
    'organisation',
    'organisationMember',
    'organSystem',
    'orientation',
    'origin',
    'originalDanseCompetition',
    'originalDanseScore',
    'originalEndPoint',
    'originalLanguage',
    'originallyUsedFor',
    'originalMaximumBoatBeam',
    'originalMaximumBoatLength',
    'originalName',
    'originalNotLatinTitle',
    'originalStartPoint',
    'originalTitle',
    'origo',
    'orpha',
    'orthologousGene',
    'other',
    'otherActivity',
    'otherAppearances',
    'otherChannel',
    'otherFamilyBranch',
    'otherInformation',
    'otherLanguage',
    'otherMedia',
    'otherName',
    'otherOccupation',
    'otherParty',
    'otherServingLines',
    'otherSportsExperience',
    'otherWins',
    'otherWorks',
    'outflow',
    'output',
    'outputHistory',
    'outskirts',
    'overallRecord',
    'oversight',
    'owner',
    'owningCompany',
    'owningOrganisation',
    'owns',
    'painter',
    'pandemic',
    'pandemicDeaths',
    'parent',
    'parentCompany',
    'parentMountainPeak',
    'parentOrganisation',
    'parish',
    'parkingInformation',
    'parkingLotsCars',
    'parkingLotsTrucks',
    'parliament',
    'parliamentaryGroup',
    'parliamentType',
    'partialFailedLaunches',
    'participant',
    'participatingIn',
    'particularSign',
    'partitionCoefficient',
    'partner',
    'party',
    'partyNumber',
    'passengersPerDay',
    'passengersPerYear',
    'passengersUsedSystem',
    'pastMember',
    'pastor',
    'patron',
    'patronSaint',
    'pccSecretary',
    'pdb',
    'peabodyAward',
    'penaltiesTeamA',
    'penaltiesTeamB',
    'penaltyScore',
    'pendamicDeaths',
    'penisLength',
    'peopleFullyVaccinated',
    'peopleName',
    'peopleVaccinated',
    'peopleVaccinatedPerHundred',
    'perCapitaIncome',
    'perCapitaIncomeAsOf',
    'perCapitaIncomeRank',
    'percentageAlcohol',
    'percentageFat',
    'percentageLiteracyMen',
    'percentageLiteracyWomen',
    'percentageLiterate',
    'percentageOfAreaWater',
    'performer',
    'periapsis',
    'perifocus',
    'perimeter',
    'perpetrator',
    'person',
    'personFunction',
    'personName',
    'personsFirstDosesCumul',
    'personsFullDosesCumul',
    'pfizer',
    'pfizerCumul',
    'phonePrefix',
    'phonePrefixLabel',
    'photographer',
    'picturesCommonsCategory',
    'piercing',
    'pisciculturalPopulation',
    'pistonStroke',
    'place',
    'placeOfBurial',
    'placeOfWorship',
    'plant',
    'playerInTeam',
    'playerStatus',
    'playingTime',
    'plays',
    'pluviometry',
    'podium',
    'podiums',
    'pole',
    'poleDriver',
    'poleDriverCountry',
    'poleDriverTeam',
    'polePosition',
    'poles',
    'policeName',
    'polishFilmAward',
    'politicalFunction',
    'politicalLeader',
    'politicalMajority',
    'politicalPartyInLegislature',
    'politicalPartyOfLeader',
    'politicalSeats',
    'politician',
    'popularVote',
    'population',
    'populationAsOf',
    'populationDensity',
    'populationMetro',
    'populationMetroDensity',
    'populationPctChildren',
    'populationPctMen',
    'populationPctWomen',
    'populationPlace',
    'populationQuote',
    'populationRural',
    'populationRuralDensity',
    'populationTotal',
    'populationTotalRanking',
    'populationUrban',
    'populationUrbanDensity',
    'populationYear',
    'portfolio',
    'postalCode',
    'power',
    'powerOutput',
    'precursor',
    'prefaceBy',
    'prefect',
    'prefectMandate',
    'prefecture',
    'prefix',
    'premiereDate',
    'premiereYear',
    'presenter',
    'presentMunicipality',
    'presentName',
    'president',
    'presidentGeneralCouncil',
    'presidentGeneralCouncilMandate',
    'presidentRegionalCouncil',
    'presidentRegionalCouncilMandate',
    'previousDemographics',
    'previousEditor',
    'previousEntity',
    'previousEvent',
    'previousInfrastructure',
    'previousMission',
    'previousName',
    'previousPopulation',
    'previousPopulationTotal',
    'previousTrackNumber',
    'previousWork',
    'previousWorkDate',
    'price',
    'primate',
    'primeMinister',
    'primogenitor',
    'principal',
    'principalArea',
    'principalEngineer',
    'probowlPick',
    'procedure',
    'producedBy',
    'producer',
    'production',
    'productionCompany',
    'productionEndDate',
    'productionEndYear',
    'productionStartDate',
    'productionStartYear',
    'productionYears',
    'productShape',
    'programCost',
    'project',
    'projectBudgetFunding',
    'projectBudgetTotal',
    'projectCoordinator',
    'projectEndDate',
    'projectKeyword',
    'projectObjective',
    'projectParticipant',
    'projectReferenceID',
    'projectStartDate',
    'projectType',
    'prominence',
    'pronunciation',
    'prospectLeague',
    'prospectTeam',
    'proTeam',
    'protectionStatus',
    'protein',
    'protestantPercentage',
    'provCode',
    'province',
    'provinceIsoCode',
    'provinceLink',
    'provost',
    'pseudonym',
    'pubchem',
    'publication',
    'publicationDate',
    'publiclyAccessible',
    'publisher',
    'purchasingPowerParity',
    'purchasingPowerParityRank',
    'purchasingPowerParityYear',
    'purpose',
    'qatarClassic',
    'quebecerTitle',
    'quotation',
    'quote',
    'ra',
    'race',
    'raceHorse',
    'raceLength',
    'raceResult',
    'races',
    'raceTrack',
    'raceWins',
    'racketCatching',
    'radio',
    'radioStation',
    'radius_ly',
    'railGauge',
    'railwayPlatforms',
    'range',
    'rank',
    'rankAgreement',
    'rankArea',
    'rankInFinalMedalCount',
    'ranking',
    'rankingsDoubles',
    'rankingsSingles',
    'rankingWins',
    'rankPopulation',
    'rating',
    'ratio',
    'rebuildDate',
    'rebuildingDate',
    'rebuildingYear',
    'recentWinner',
    'recommissioningDate',
    'recordDate',
    'recordedIn',
    'recordLabel',
    'recoveryCases',
    'rector',
    'redline',
    'redListIdNL',
    'redLongDistancePisteNumber',
    'redSkiPisteNumber',
    'refcul',
    'reference',
    'reffBourgmestre',
    'refgen',
    'refgeo',
    'refpol',
    'refseq',
    'refseqmrna',
    'refseqprotein',
    'regency',
    'regentOf',
    'regime',
    'region',
    'regionalCouncil',
    'regionalLanguage',
    'regionalPrefecture',
    'regionLink',
    'regionServed',
    'regionType',
    'registration',
    'registry',
    'registryNumber',
    'reign',
    'reigningPope',
    'reignName',
    'relatedFunctions',
    'relatedMeanOfTransportation',
    'relatedPlaces',
    'relation',
    'relative',
    'relativeAtomicMass',
    'releaseDate',
    'releaseLocation',
    'relics',
    'relief',
    'religiousHead',
    'religiousOrder',
    'reopened',
    'reopeningDate',
    'reopeningYear',
    'reportingMark',
    'representative',
    'requirement',
    'reservations',
    'residence',
    'restaurant',
    'restingDate',
    'restingPlace',
    'restoreDate',
    'restriction',
    'result',
    'retentionTime',
    'retired',
    'retiredRocket',
    'retirementDate',
    'revenue',
    'revenueYear',
    'review',
    'rgbCoordinateBlue',
    'rgbCoordinateGreen',
    'rgbCoordinateRed',
    'ridId',
    'rightAscension',
    'rightChild',
    'rightTributary',
    'rivalSchool',
    'river',
    'riverBranch',
    'riverBranchOf',
    'riverMouth',
    'rkdArtistsId',
    'road',
    'rocket',
    'rocketStages',
    'rolandGarrosDouble',
    'rolandGarrosMixed',
    'rolandGarrosSingle',
    'role',
    'roleInEvent',
    'roofHeight',
    'rotationPeriod',
    'route',
    'routeDirection',
    'routeEnd',
    'routeEndDirection',
    'routeEndLocation',
    'routeJunction',
    'routeNext',
    'routeNumber',
    'routePrevious',
    'routeStart',
    'routeStartDirection',
    'routeStartLocation',
    'routeTypeAbbreviation',
    'ruling',
    'runningMate',
    'runtime',
    'runwayDesignation',
    'runwayLength',
    'runwaySurface',
    'runwayWidth',
    'ruralMunicipality',
    'saint',
    'salary',
    'sales',
    'sameName',
    'satcat',
    'satellite',
    'satellitesDeployed',
    'scale',
    'scaleFactor',
    'scene',
    'school',
    'schoolCode',
    'schoolNumber',
    'schoolPatron',
    'scientificName',
    'score',
    'screenActorsGuildAward',
    'sea',
    'seasonManager',
    'seasonNumber',
    'seatingCapacity',
    'seatNumber',
    'second',
    'secondCommander',
    'secondDriver',
    'secondDriverCountry',
    'secondLeader',
    'secondPlace',
    'secondPopularVote',
    'secondTeam',
    'secretaryGeneral',
    'security',
    'seiyu',
    'selectionPoint',
    'selectionYear',
    'selibrId',
    'senator',
    'senior',
    'seniority',
    'seniunija',
    'sentence',
    'serviceEndDate',
    'serviceEndYear',
    'serviceModule',
    'serviceNumber',
    'serviceStartDate',
    'serviceStartYear',
    'servingSize',
    'servingTemperature',
    'sessionNumber',
    'setDesigner',
    'settingOfPlay',
    'settlement',
    'settlementAttached',
    'setupTime',
    'severeCases',
    'sex',
    'shape',
    'shareDate',
    'shareOfAudience',
    'shareSource',
    'sharingOutPopulation',
    'sharingOutPopulationYear',
    'sheading',
    'shipBeam',
    'shipCrew',
    'shipDisplacement',
    'shipDraft',
    'shipLaunch',
    'shoeNumber',
    'shoeSize',
    'shoot',
    'shoots',
    'shoreLength',
    'shortProgCompetition',
    'shortProgScore',
    'show',
    'showJudge',
    'shuttle',
    'sibling',
    'signature',
    'significantBuilding',
    'signName',
    'silverMedalDouble',
    'silverMedalist',
    'silverMedalMixed',
    'silverMedalSingle',
    'singleList',
    'singleOf',
    'sire',
    'siren',
    'sister',
    'sisterCollege',
    'sisterNewspaper',
    'sisterStation',
    'sixthFormStudents',
    'size_v',
    'sizeBlazon',
    'sizeLogo',
    'sizeMap',
    'sizeThumbnail',
    'skiLift',
    'skinColor',
    'skiPisteKilometre',
    'skiPisteNumber',
    'skiTow',
    'slogan',
    'smiles',
    'snowParkNumber',
    'soccerLeaguePromoted',
    'soccerLeagueRelegated',
    'soccerLeagueSeason',
    'soccerLeagueWinner',
    'soccerTournamentClosingSeason',
    'soccerTournamentLastChampion',
    'soccerTournamentMostSteady',
    'soccerTournamentMostSuccesfull',
    'soccerTournamentOpeningSeason',
    'soccerTournamentThisSeason',
    'soccerTournamentTopScorer',
    'solicitorGeneral',
    'solubility',
    'solvent',
    'solventWithBadSolubility',
    'solventWithGoodSolubility',
    'solventWithMediocreSolubility',
    'son',
    'soundRecording',
    'sourceConfluenceCountry',
    'sourceConfluenceElevation',
    'sourceConfluenceMountain',
    'sourceConfluencePlace',
    'sourceConfluenceRegion',
    'sourceConfluenceState',
    'sourceCountry',
    'sourceDistrict',
    'sourceElevation',
    'sourceMountain',
    'sourceName',
    'sourcePlace',
    'sourceRegion',
    'sourceState',
    'sourceText',
    'sourceWebsite',
    'southEastPlace',
    'southPlace',
    'southWestPlace',
    'sovereignCountry',
    'space',
    'spacecraft',
    'spacestation',
    'spacewalkBegin',
    'spacewalkEnd',
    'speaker',
    'specialEffects',
    'specialist',
    'speciality',
    'specialTrial',
    'species',
    'speedLimit',
    'spike',
    'splitFromParty',
    'spokenIn',
    'spokesperson',
    'sport',
    'sportCountry',
    'sportDiscipline',
    'sportsFunction',
    'sportSpecialty',
    'spouse',
    'spouseName',
    'spurOf',
    'squadNumber',
    'stadium',
    'staff',
    'starRating',
    'starring',
    'start',
    'startCareer',
    'startDate',
    'startDateTime',
    'startOccupation',
    'startPoint',
    'startWct',
    'startWqs',
    'startYear',
    'startYearOfInsertion',
    'startYearOfSales',
    'state',
    'stateDelegate',
    'stateOfOrigin',
    'stateOfOriginPoint',
    'stateOfOriginTeam',
    'stateOfOriginYear',
    'stationEvaDuration',
    'stationStructure',
    'stationVisitDuration',
    'statisticValue',
    'statisticYear',
    'statName',
    'status',
    'statusManager',
    'statusYear',
    'statValue',
    'stockExchange',
    'storyEditor',
    'strength',
    'student',
    'stylisticOrigin',
    'subdivisionLink',
    'subdivisionName',
    'subdivisions',
    'subFamily',
    'subjectOfPlay',
    'subjectTerm',
    'sublimationPoint',
    'subMunicipalityType',
    'suborbitalFlights',
    'subprefecture',
    'subPrefecture',
    'subregion',
    'subsequentInfrastructure',
    'subsequentWork',
    'subsequentWorkDate',
    'subsidiary',
    'subsystem',
    'subsystemLink',
    'subtitle',
    'subTribus',
    'successfulLaunches',
    'sudocId',
    'summerAppearances',
    'summerTemperature',
    'superbowlWin',
    'superFamily',
    'superintendent',
    'superTribus',
    'supplementalDraftRound',
    'supplementalDraftYear',
    'supplies',
    'supply',
    'suppreddedDate',
    'surfaceArea',
    'surfaceFormOccurrenceOffset',
    'surfaceGravity',
    'surfaceType',
    'suspectedCases',
    'swimmingStyle',
    'symbol',
    'synonym',
    'systemOfLaw',
    'systemRequirements',
    'tag',
    'taoiseach',
    'targetAirport',
    'targetSpaceStation',
    'taste',
    'tattoo',
    'taxon',
    'team',
    'teamCoached',
    'teamManager',
    'teamName',
    'teamPoint',
    'teamSize',
    'teamTitle',
    'technique',
    'televisionSeries',
    'temperature',
    'templateName',
    'temple',
    'templeYear',
    'tempPlace',
    'tenant',
    'tennisSurfaceType',
    'termOfOffice',
    'termPeriod',
    'territory',
    'tessitura',
    'testaverage',
    'theology',
    'third',
    'thirdCommander',
    'thirdDriver',
    'thirdDriverCountry',
    'thirdPlace',
    'thirdTeam',
    'throwingSide',
    'thumbnail',
    'thumbnailCaption',
    'tie',
    'time',
    'timeInSpace',
    'timeshiftChannel',
    'title',
    'titleDate',
    'titleDouble',
    'titleLanguage',
    'titleSingle',
    'toll',
    'tonyAward',
    'topFloorHeight',
    'topic',
    'topLevelDomain',
    'topSpeed',
    'torchBearer',
    'torqueOutput',
    'totalCargo',
    'totalDiscs',
    'totalIliCases',
    'totalLaunches',
    'totalMass',
    'totalPopulation',
    'totalTracks',
    'totalTravellers',
    'totalVaccinations',
    'totalVaccinationsPerHundred',
    'touristicSite',
    'tournamentOfChampions',
    'tournamentRecord',
    'towerHeight',
    'trackLength',
    'trackNumber',
    'trackWidth',
    'tradingName',
    'trainer',
    'trainerClub',
    'trainerYears',
    'training',
    'translatedMotto',
    'translator',
    'transmission',
    'tree',
    'tribus',
    'trustee',
    'tuition',
    'tvComId',
    'tvShow',
    'twinCountry',
    'twinTown',
    'typeCoordinate',
    'typeOfGrain',
    'typeOfStorage',
    'typeOfYeast',
    'uciCode',
    'ulanId',
    'umbrellaTitle',
    'uncle',
    'undraftedYear',
    'unesco',
    'unicode',
    'uniprot',
    'unitaryAuthority',
    'unitCost',
    'unitedStatesNationalBridgeId',
    'university',
    'unknownOutcomes',
    'unloCode',
    'unNumber',
    'updated',
    'upperAge',
    'urbanArea',
    'usedInWar',
    'usingCountry',
    'usk',
    'usOpenDouble',
    'usOpenMixed',
    'usOpenSingle',
    'usSales',
    'usurper',
    'utcOffset',
    'v_hb',
    'vaccination',
    'vaccine',
    'value',
    'valvetrain',
    'vaporPressure',
    'vehicle',
    'vehicleCode',
    'vehiclesInFleet',
    'vehiclesPerDay',
    'vein',
    'veneratedIn',
    'viafId',
    'viceChancellor',
    'viceLeader',
    'viceLeaderParty',
    'vicePresident',
    'vicePrimeMinister',
    'vicePrincipal',
    'victims',
    'victory',
    'victoryAsMgr',
    'victoryPercentageAsMgr',
    'virtualChannel',
    'visitorsPercentageChange',
    'visitorsPerDay',
    'visitorsPerYear',
    'visitorStatisticsAsOf',
    'visitorsTotal',
    'voice',
    'volcanicActivity',
    'volcanicType',
    'volcanoId',
    'voltageOfElectrification',
    'volume',
    'volumeQuote',
    'volumes',
    'vonKlitzingConstant',
    'votesAgainst',
    'votesFor',
    'wagon',
    'waistSize',
    'war',
    'ward',
    'water',
    'waterArea',
    'watercourse',
    'waterPercentage',
    'watershed',
    'wavelength',
    'weapon',
    'websiteLabel',
    'weddingParentsDate',
    'weight',
    'westPlace',
    'whaDraft',
    'whaDraftTeam',
    'whaDraftYear',
    'wheelbase',
    'wholeArea',
    'width',
    'widthQuote',
    'wikiPageCharacterSize',
    'wikiPageExtracted',
    'wikiPageID',
    'wikiPageInDegree',
    'wikiPageLength',
    'wikiPageLengthDelta',
    'wikiPageModified',
    'wikiPageOutDegree',
    'wikiPageRevisionID',
    'wikiPageUsesTemplate',
    'wilaya',
    'wimbledonDouble',
    'wimbledonMixed',
    'wimbledonSingle',
    'wineRegion',
    'wineYear',
    'wingArea',
    'wingspan',
    'wins',
    'winterAppearances',
    'winterTemperature',
    'wordBefore',
    'work',
    'workArea',
    'worldChampionTitleYear',
    'worldOpen',
    'worldTeamCup',
    'worldTournament',
    'worldTournamentBronze',
    'worldTournamentGold',
    'worldTournamentSilver',
    'worstDefeat',
    'wptFinalTable',
    'wptItm',
    'wptTitle',
    'writer',
    'wsopItm',
    'wsopWinYear',
    'wsopWristband',
    'year',
    'yearElevationIntoNobility',
    'yearOfConstruction',
    'yearOfElectrification',
    'years',
    'youthClub',
    'youthYears',
    'zdb',
    'zipCode',
    'ابی_چرچ_کی_برکت',
    'انتظامی_اجتماعیت',
    'انتظامی_درجہ',
    'انعام',
    'اے_ایف_آئی_انعام',
    'جامعہ_کا_ناپ',
    'جمع_کا_علاقہ',
    'حصول_کی_تاریخ',
    'خلاصہ',
    'رسائی',
    'رقبہ',
    'رہائی_کی_تاریخ',
    'طَنابی_گاڑی',
    'فعال_سال_شروع_سال_Mgr',
    'فعال_سال_کی_آخری_تاریخ_Mgr',
    'فعال_سال_کی_شروعات_کی_تاریخ',
    'فعال_کیسز',
    'فنکار',
    'مجموعی_آبادی_کل',
    'مخفف',
    'مصنف',
    'معاملہ',
    'معاملہ',
    'پرہیز',
    'پیسنے_کے_قابل',
    'کتاب',
)

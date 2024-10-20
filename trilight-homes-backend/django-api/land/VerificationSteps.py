# verification_decision_tree.py

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class VerificationStep(MPTTModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

class MPTTMeta:
    order_insertion_by = ['order']

    def __str__(self):
        return self.name

def create_verification_tree(): # Root
    root = VerificationStep.objects.create(name="Land Verification", description="Complete land verification process")

    # Level 1: Main Categories
    ownership = VerificationStep.objects.create(name="1. Ownership Verification", description="Verify the true ownership of the land", parent=root)
    legal_status = VerificationStep.objects.create(name="2. Legal Status Check", description="Check the legal status and documentation of the land", parent=root)
    physical_inspection = VerificationStep.objects.create(name="3. Physical Inspection", description="Conduct a physical inspection of the land", parent=root)
    community_validation = VerificationStep.objects.create(name="4. Community Validation", description="Validate the land ownership with the local community", parent=root)
    dispute_check = VerificationStep.objects.create(name="5. Dispute Check", description="Check for any existing or potential disputes", parent=root)
    environmental_assessment = VerificationStep.objects.create(name="6. Environmental Assessment", description="Assess environmental factors and risks", parent=root)
    financial_verification = VerificationStep.objects.create(name="7. Financial Verification", description="Verify financial aspects of the land transaction", parent=root)
    infrastructure_assessment = VerificationStep.objects.create(name="8. Infrastructure Assessment", description="Assess the quality and availability of infrastructure", parent=root)
    market_analysis = VerificationStep.objects.create(name="9. Market Analysis", description="Analyze market conditions and risks", parent=root)
    cultural_social_assessment = VerificationStep.objects.create(name="10. Cultural and Social Assessment", description="Assess cultural and social factors", parent=root)

    # Level 2-3: Detailed Steps

    # 1. Ownership Verification
    seller_verification = VerificationStep.objects.create(name="1.1 Seller Identity Verification", description="Verify the identity of the seller", parent=ownership)
    VerificationStep.objects.create(name="1.1.1 Government ID Check", description="Verify seller's government-issued ID", parent=seller_verification)
    VerificationStep.objects.create(name="1.1.2 Address Verification", description="Confirm seller's current address", parent=seller_verification)
    VerificationStep.objects.create(name="1.1.3 Biometric Verification", description="Conduct biometric verification if available", parent=seller_verification)

    title_review = VerificationStep.objects.create(name="1.2 Title Document Review", description="Review and verify all title documents", parent=ownership)
    VerificationStep.objects.create(name="1.2.1 Certificate of Occupancy Check", description="Verify the Certificate of Occupancy (C of O)", parent=title_review)
    VerificationStep.objects.create(name="1.2.2 Deed of Assignment Verification", description="Check the Deed of Assignment if applicable", parent=title_review)
    VerificationStep.objects.create(name="1.2.3 Governor's Consent Verification", description="Verify Governor's Consent on the title", parent=title_review)
    VerificationStep.objects.create(name="1.2.4 Digital Land Registry Check", description="Verify title in digital land registry if available", parent=title_review)

    ownership_history = VerificationStep.objects.create(name="1.3 Ownership History", description="Investigate the history of land ownership", parent=ownership)
    VerificationStep.objects.create(name="1.3.1 Previous Owners Check", description="Identify and verify previous land owners", parent=ownership_history)
    VerificationStep.objects.create(name="1.3.2 Duration of Ownership", description="Confirm the duration of current ownership", parent=ownership_history)
    VerificationStep.objects.create(name="1.3.3 Chain of Title Analysis", description="Analyze the complete chain of title", parent=ownership_history)

    # 2. Legal Status Check
    land_use = VerificationStep.objects.create(name="2.1 Land Use and Zoning", description="Check the approved land use and zoning regulations", parent=legal_status)
    VerificationStep.objects.create(name="2.1.1 Zoning Regulations Check", description="Verify compliance with local zoning laws", parent=land_use)
    VerificationStep.objects.create(name="2.1.2 Land Use Approval", description="Confirm approved land use matches intended use", parent=land_use)
    VerificationStep.objects.create(name="2.1.3 Future Zoning Plans", description="Check for any planned changes in zoning", parent=land_use)

    govt_charges = VerificationStep.objects.create(name="2.2 Government Charges", description="Verify if there are any outstanding government charges", parent=legal_status)
    VerificationStep.objects.create(name="2.2.1 Property Tax Check", description="Verify payment of all property taxes", parent=govt_charges)
    VerificationStep.objects.create(name="2.2.2 Land Use Charge", description="Check for any outstanding land use charges", parent=govt_charges)
    VerificationStep.objects.create(name="2.2.3 Utility Bill Verification", description="Verify payment of utility bills if applicable", parent=govt_charges)

    encumbrances = VerificationStep.objects.create(name="2.3 Encumbrances Check", description="Check for any encumbrances on the land", parent=legal_status)
    VerificationStep.objects.create(name="2.3.1 Mortgage Check", description="Verify if the land is under any mortgage", parent=encumbrances)
    VerificationStep.objects.create(name="2.3.2 Lien Search", description="Search for any liens on the property", parent=encumbrances)
    VerificationStep.objects.create(name="2.3.3 Easement Verification", description="Check for any easements on the property", parent=encumbrances)

    # 3. Physical Inspection
    boundary = VerificationStep.objects.create(name="3.1 Boundary Verification", description="Verify the land boundaries", parent=physical_inspection)
    VerificationStep.objects.create(name="3.1.1 Survey Plan Check", description="Review and verify the survey plan", parent=boundary)
    VerificationStep.objects.create(name="3.1.2 Physical Boundary Inspection", description="Physically inspect and confirm boundaries", parent=boundary)
    VerificationStep.objects.create(name="3.1.3 GPS Coordinate Verification", description="Verify GPS coordinates of the land", parent=boundary)

    topography = VerificationStep.objects.create(name="3.2 Topography Assessment", description="Assess the topography of the land", parent=physical_inspection)
    VerificationStep.objects.create(name="3.2.1 Soil Quality Check", description="Assess soil quality and composition", parent=topography)
    VerificationStep.objects.create(name="3.2.2 Flood Risk Assessment", description="Evaluate potential flood risks", parent=topography)
    VerificationStep.objects.create(name="3.2.3 Erosion Risk Evaluation", description="Assess the risk of soil erosion", parent=topography)

    accessibility = VerificationStep.objects.create(name="3.3 Accessibility Check", description="Check the accessibility of the land", parent=physical_inspection)
    VerificationStep.objects.create(name="3.3.1 Road Access Verification", description="Confirm road access to the property", parent=accessibility)
    VerificationStep.objects.create(name="3.3.2 Public Transportation Proximity", description="Check proximity to public transportation", parent=accessibility)
    VerificationStep.objects.create(name="3.3.3 Seasonal Access Evaluation", description="Evaluate accessibility during different seasons", parent=accessibility)

    # 4. Community Validation
    local_authority = VerificationStep.objects.create(name="4.1 Local Authority Consultation", description="Consult with local authorities", parent=community_validation)
    VerificationStep.objects.create(name="4.1.1 Local Chief Consultation", description="Meet with the local chief or traditional ruler", parent=local_authority)
    VerificationStep.objects.create(name="4.1.2 Community Leaders Interview", description="Interview other community leaders", parent=local_authority)
    VerificationStep.objects.create(name="4.1.3 Local Government Verification", description="Verify land status with local government officials", parent=local_authority)

    neighbor_check = VerificationStep.objects.create(name="4.2 Neighbor Verification", description="Verify with neighboring property owners", parent=community_validation)
    VerificationStep.objects.create(name="4.2.1 Adjoining Neighbors Interview", description="Interview immediately adjoining neighbors", parent=neighbor_check)
    VerificationStep.objects.create(name="4.2.2 General Neighborhood Inquiry", description="Make general inquiries in the neighborhood", parent=neighbor_check)
    VerificationStep.objects.create(name="4.2.3 Community Land Use Confirmation", description="Confirm community's understanding of land use", parent=neighbor_check)

    community_plans = VerificationStep.objects.create(name="4.3 Community Development Checks", description="Check for any community development plans affecting the land", parent=community_validation)
    VerificationStep.objects.create(name="4.3.1 Future Development Plans", description="Inquire about any planned community developments", parent=community_plans)
    VerificationStep.objects.create(name="4.3.2 Community Restrictions", description="Check for any community-imposed restrictions", parent=community_plans)
    VerificationStep.objects.create(name="4.3.3 Cultural Site Verification", description="Verify if the land includes any cultural or historical sites", parent=community_plans)

    # 5. Dispute Check
    legal_disputes = VerificationStep.objects.create(name="5.1 Legal Dispute Check", description="Check for any legal disputes involving the land", parent=dispute_check)
    VerificationStep.objects.create(name="5.1.1 Court Records Search", description="Search court records for any litigation involving the land", parent=legal_disputes)
    VerificationStep.objects.create(name="5.1.2 Lawyer Consultation", description="Consult with a local real estate lawyer", parent=legal_disputes)
    VerificationStep.objects.create(name="5.1.3 Land Registry Dispute Check", description="Check land registry for registered disputes", parent=legal_disputes)

    family_disputes = VerificationStep.objects.create(name="5.2 Family Dispute Investigation", description="Investigate any potential family disputes over the land", parent=dispute_check)
    VerificationStep.objects.create(name="5.2.1 Inheritance Dispute Check", description="Check for any inheritance-related disputes", parent=family_disputes)
    VerificationStep.objects.create(name="5.2.2 Family Member Interviews", description="Interview relevant family members if applicable", parent=family_disputes)
    VerificationStep.objects.create(name="5.2.3 Family Land History", description="Investigate the history of the land within the family", parent=family_disputes)

    boundary_disputes = VerificationStep.objects.create(name="5.3 Boundary Dispute Check", description="Check for any boundary disputes with neighboring lands", parent=dispute_check)
    VerificationStep.objects.create(name="5.3.1 Historical Dispute Search", description="Research any historical boundary disputes", parent=boundary_disputes)
    VerificationStep.objects.create(name="5.3.2 Local Land Registry Check", description="Check local land registry for boundary issue reports", parent=boundary_disputes)
    VerificationStep.objects.create(name="5.3.3 Surveyor Consultation", description="Consult with a licensed surveyor about potential boundary issues", parent=boundary_disputes)

    # 6. Environmental Assessment
    environmental_risks = VerificationStep.objects.create(name="6.1 Environmental Risk Assessment", description="Assess potential environmental risks", parent=environmental_assessment)
    VerificationStep.objects.create(name="6.1.1 Flood Zone Check", description="Determine if the land is in a flood-prone area", parent=environmental_risks)
    VerificationStep.objects.create(name="6.1.2 Erosion Risk Evaluation", description="Evaluate the risk of soil erosion", parent=environmental_risks)
    VerificationStep.objects.create(name="6.1.3 Natural Disaster Risk Assessment", description="Assess risks from earthquakes, landslides, etc.", parent=environmental_risks)

    pollution_check = VerificationStep.objects.create(name="6.2 Pollution Check", description="Check for any pollution issues", parent=environmental_assessment)
    VerificationStep.objects.create(name="6.2.1 Soil Contamination Test", description="Test for soil contamination", parent=pollution_check)
    VerificationStep.objects.create(name="6.2.2 Water Quality Assessment", description="Assess the quality of available water sources", parent=pollution_check)
    VerificationStep.objects.create(name="6.2.3 Air Quality Evaluation", description="Evaluate local air quality", parent=pollution_check)

    wildlife_assessment = VerificationStep.objects.create(name="6.3 Wildlife and Vegetation Assessment", description="Assess local wildlife and vegetation", parent=environmental_assessment)
    VerificationStep.objects.create(name="6.3.1 Protected Species Check", description="Check for any protected species on the land", parent=wildlife_assessment)
    VerificationStep.objects.create(name="6.3.2 Vegetation Removal Regulations", description="Verify regulations on vegetation removal", parent=wildlife_assessment)
    VerificationStep.objects.create(name="6.3.3 Ecosystem Impact Evaluation", description="Evaluate potential impact on local ecosystem", parent=wildlife_assessment)

    climate_impact = VerificationStep.objects.create(name="6.4 Climate Change Impact", description="Assess potential impacts of climate change", parent=environmental_assessment)
    VerificationStep.objects.create(name="6.4.1 Sea Level Rise Risk", description="Evaluate risk from potential sea level rise", parent=climate_impact)
    VerificationStep.objects.create(name="6.4.2 Temperature Change Projections", description="Consider local temperature change projections", parent=climate_impact)
    VerificationStep.objects.create(name="6.4.3 Extreme Weather Frequency", description="Assess potential increase in extreme weather events", parent=climate_impact)

    # 7. Financial Verification
    value_assessment = VerificationStep.objects.create(name="7.1 Land Value Assessment", description="Assess the true value of the land", parent=financial_verification)
    VerificationStep.objects.create(name="7.1.1 Professional Valuation", description="Obtain a professional land valuation", parent=value_assessment)
    VerificationStep.objects.create(name="7.1.2 Comparative Market Analysis", description="Perform a comparative market analysis", parent=value_assessment)
    VerificationStep.objects.create(name="7.1.3 Future Value Projection", description="Project potential future value of the land", parent=value_assessment)

    transaction_costs = VerificationStep.objects.create(name="7.2 Transaction Cost Verification", description="Verify all costs associated with the transaction", parent=financial_verification)
    VerificationStep.objects.create(name="7.2.1 Legal Fee Estimation", description="Estimate all legal fees involved", parent=transaction_costs)
    VerificationStep.objects.create(name="7.2.2 Tax Obligation Check", description="Verify all tax obligations for the transaction", parent=transaction_costs)
    VerificationStep.objects.create(name="7.2.3 Hidden Cost Investigation", description="Investigate potential hidden costs", parent=transaction_costs)

    payment_verification = VerificationStep.objects.create(name="7.3 Payment Method Verification", description="Verify the proposed payment method", parent=financial_verification)
    VerificationStep.objects.create(name="7.3.1 Bank Transfer Verification", description="Verify bank details for transfer if applicable", parent=payment_verification)
    VerificationStep.objects.create(name="7.3.2 Escrow Service Check", description="Check availability of escrow services", parent=payment_verification)
    VerificationStep.objects.create(name="7.3.3 Anti-Money Laundering Check", description="Perform necessary anti-money laundering checks", parent=payment_verification)

    financing_options = VerificationStep.objects.create(name="7.4 Financing Options Assessment", description="Assess available financing options", parent=financial_verification)
    VerificationStep.objects.create(name="7.4.1 Mortgage Availability Check", description="Check availability of mortgages for the property", parent=financing_options)
    VerificationStep.objects.create(name="7.4.2 Interest Rate Comparison", description="Compare interest rates from different lenders", parent=financing_options)
    VerificationStep.objects.create(name="7.4.3 Government Subsidy Eligibility", description="Check eligibility for any government subsidies or programs", parent=financing_options)

    maintenance_cost = VerificationStep.objects.create(name="7.5 Maintenance Cost Estimation", description="Estimate future maintenance costs", parent=financial_verification)
    VerificationStep.objects.create(name="7.5.1 Property Upkeep Projection", description="Project costs for regular property upkeep", parent=maintenance_cost)
    VerificationStep.objects.create(name="7.5.2 Infrastructure Maintenance Estimation", description="Estimate costs for maintaining local infrastructure", parent=maintenance_cost)
    VerificationStep.objects.create(name="7.5.3 Long-term Repair Forecast", description="Forecast potential long-term repair costs", parent=maintenance_cost)

    # 8. Infrastructure Assessment
    road_assessment = VerificationStep.objects.create(name="8.1 Road Infrastructure Assessment", description="Assess the quality and accessibility of road infrastructure", parent=infrastructure_assessment)
    VerificationStep.objects.create(name="8.1.1 Road Quality Evaluation", description="Evaluate the quality of access roads", parent=road_assessment)
    VerificationStep.objects.create(name="8.1.2 Traffic Congestion Analysis", description="Analyze potential traffic congestion issues", parent=road_assessment)
    VerificationStep.objects.create(name="8.1.3 Future Road Development Plans", description="Check for any planned road developments", parent=road_assessment)

    utility_services = VerificationStep.objects.create(name="8.2 Utility Services Verification", description="Verify the availability and quality of utility services", parent=infrastructure_assessment)
    VerificationStep.objects.create(name="8.2.1 Electricity Supply Check", description="Verify reliability of electricity supply", parent=utility_services)
    VerificationStep.objects.create(name="8.2.2 Water Supply Assessment", description="Assess the quality and reliability of water supply", parent=utility_services)
    VerificationStep.objects.create(name="8.2.3 Telecommunications Infrastructure", description="Check availability of internet and mobile networks", parent=utility_services)

    public_services = VerificationStep.objects.create(name="8.3 Public Services Assessment", description="Assess the availability of essential public services", parent=infrastructure_assessment)
    VerificationStep.objects.create(name="8.3.1 Healthcare Facilities Proximity", description="Check proximity to healthcare facilities", parent=public_services)
    VerificationStep.objects.create(name="8.3.2 Educational Institutions Check", description="Verify availability of schools and educational institutions", parent=public_services)
    VerificationStep.objects.create(name="8.3.3 Emergency Services Evaluation", description="Evaluate access to police, fire, and emergency services", parent=public_services)

    # 9. Market Analysis
    market_trends = VerificationStep.objects.create(name="9.1 Real Estate Market Trends", description="Analyze current and projected real estate market trends", parent=market_analysis)
    VerificationStep.objects.create(name="9.1.1 Price Trend Analysis", description="Analyze historical and projected price trends", parent=market_trends)
    VerificationStep.objects.create(name="9.1.2 Supply-Demand Assessment", description="Assess the balance of supply and demand in the local market", parent=market_trends)
    VerificationStep.objects.create(name="9.1.3 Market Cycle Evaluation", description="Evaluate the current phase of the real estate market cycle", parent=market_trends)

    economic_factors = VerificationStep.objects.create(name="9.2 Economic Factor Analysis", description="Analyze relevant economic factors affecting the property market", parent=market_analysis)
    VerificationStep.objects.create(name="9.2.1 Local Economic Growth Assessment", description="Assess local economic growth prospects", parent=economic_factors)
    VerificationStep.objects.create(name="9.2.2 Employment Rate Analysis", description="Analyze local employment rates and trends", parent=economic_factors)
    VerificationStep.objects.create(name="9.2.3 Interest Rate Projections", description="Consider projections for interest rates", parent=economic_factors)

    market_risks = VerificationStep.objects.create(name="9.3 Market Risk Assessment", description="Assess potential market risks", parent=market_analysis)
    VerificationStep.objects.create(name="9.3.1 Market Volatility Evaluation", description="Evaluate the volatility of the local real estate market", parent=market_risks)
    VerificationStep.objects.create(name="9.3.2 Oversupply Risk Assessment", description="Assess the risk of market oversupply", parent=market_risks)
    VerificationStep.objects.create(name="9.3.3 Regulatory Risk Analysis", description="Analyze potential impacts of changing regulations", parent=market_risks)

    # 10. Cultural and Social Assessment
    language_assessment = VerificationStep.objects.create(name="10.1 Language and Communication Assessment", description="Assess potential language barriers and communication challenges", parent=cultural_social_assessment)
    VerificationStep.objects.create(name="10.1.1 Local Language Identification", description="Identify predominant local languages", parent=language_assessment)
    VerificationStep.objects.create(name="10.1.2 Interpreter Requirement Evaluation", description="Evaluate need for interpreters in transactions", parent=language_assessment)
    VerificationStep.objects.create(name="10.1.3 Documentation Language Check", description="Verify languages used in official documentation", parent=language_assessment)

    cultural_norms = VerificationStep.objects.create(name="10.2 Cultural Norms and Practices Assessment", description="Assess relevant cultural norms and practices", parent=cultural_social_assessment)
    VerificationStep.objects.create(name="10.2.1 Land Ownership Customs", description="Investigate local customs regarding land ownership", parent=cultural_norms)
    VerificationStep.objects.create(name="10.2.2 Business Etiquette Evaluation", description="Evaluate local business etiquette and practices", parent=cultural_norms)
    VerificationStep.objects.create(name="10.2.3 Religious Considerations", description="Consider any relevant religious factors", parent=cultural_norms)

    social_impact = VerificationStep.objects.create(name="10.3 Social Impact Assessment", description="Assess the social impact of the land transaction", parent=cultural_social_assessment)
    VerificationStep.objects.create(name="10.3.1 Displacement Risk Evaluation", description="Evaluate risk of displacing local communities", parent=social_impact)
    VerificationStep.objects.create(name="10.3.2 Community Benefit Analysis", description="Analyze potential benefits to the local community", parent=social_impact)
    VerificationStep.objects.create(name="10.3.3 Social Tension Risk Assessment", description="Assess risk of creating social tensions", parent=social_impact)

# Uncomment the following line to create the verification tree
create_verification_tree()

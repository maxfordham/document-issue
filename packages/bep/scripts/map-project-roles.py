from enum import Enum



# old
class RoleEnum(Enum):
    director = "Director in Charge"
    lead_crm = "Client Relationship Management (CRM) Lead"
    lead_management = "Management Lead"
    lead_commercial = "Commercial Lead"
    lead_design = "Design Strategy Lead"
    lead_mechanical = "Lead Mechanical Engineer"
    lead_electrical = "Lead Electrical Engineer"
    lead_h_and_s = "Health and Safety Lead"
    lead_sustainability = "Lead Sustainability Consultant"
    lead_bpm = "Lead Building Performance Modeller"
    lead_acoustics = "Lead Acoustician"
    lead_passivhaus = "Lead Passivhaus"
    project_engineer = "Project Engineer"
    proj_coordinator = "Project Coordinator"
    proj_admin = "Project Administrator"
    rev_strategy = "Strategy Reviewer"
    rev_technical = "Technical Reviewer"
    eng_bpm = "Building Performance Modeller"
    eng_systems = "Systems Engineer"
    eng_site = "Site Engineer"
    eng_digital = "Digital Design Engineer"
    eng_acoustics = "Acoustician"
    eng_passivhaus = "Passivhaus Engineer"
    con_sustainability = "Sustainability Consultant"
    con_bim = "BIM Strategy Advisor"





# new
li_roles = """role_name,role_title
project_administrator,Project Administrator
project_engineer,Project Engineer
project_coordinator,Project Coordinator
project_leader,Project Leader
acoustician,Acoustician
client_relationship_leader,Client Relationship Leader
commercial_leader,Commercial Leader
health_and_safety_lead,Health and Safety Lead
site_engineer,Site Engineer
building_performance_modeller,Building Performance Modeller
bim_strategy_advisor,BIM Strategy Advisor
engineer,Engineer
digital_design_engineer,Digital Design Engineer
project_passivhaus_designer,Project Passivhaus Designer
passivhaus_designer,Passivhaus Designer
director_in_charge,Director in Charge
final_acoustics_reviewer,Final Acoustics Reviewer
acoustic_sponsor,Acoustic Sponsor
project_acoustician,Project Acoustician
final_model_reviewer,Final Model Reviewer
building_performance_modeller_sponsor,Building Performance Modeller Sponsor
project_building_performance_modeller,Project Building Performance Modeller
final_light_and_air_reviewer,Final Light and Air Reviewer
light_and_air_sponsor,Light and Air Sponsor
project_light_and_air_specialist,Project Light and Air Specialist
light_and_air_specialist,Light and Air Specialist
final_mechanical_reviewer,Final Mechanical Reviewer
final_electrical_reviewer,Final Electrical Reviewer
mechanical_sponsor,Mechanical Sponsor
electrical_sponsor,Electrical Sponsor
sector_strategy_reviewer,Sector Strategy Reviewer
project_mechanical_engineer,Project Mechanical Engineer
project_electrical_engineer,Project Electrical Engineer
final_passivhaus_reviewer,Final Passivhaus Reviewer
passivhaus_sponsor,Passivhaus Sponsor
final_sustainability_reviewer,Final Sustainability Reviewer
sustainability_sponsor,Sustainability Sponsor
project_sustainability_consultant,Project Sustainability Consultant
sustainability_consultant,Sustainability Consultant
mep_stragegy_leader,MEP Stragegy Leader
sustainability_strategy_leader,Sustainability Strategy Leader""".split("\n")
map_new_name_title = {x.split(",")[0]: x.split(",")[1] for x in li_roles[1:]}


# map
map_project_roles= {
    RoleEnum.director_in_charge: "director_in_charge",
    RoleEnum.lead_crm: "client_relationship_leader",
    RoleEnum.lead_management: "project_leader",
    RoleEnum.lead_commercial: "commercial_leader",
    RoleEnum.lead_design: "mep_stragegy_leader",
    RoleEnum.lead_mechanical: "project_mechanical_engineer",
    RoleEnum.lead_electrical: "project_electrical_engineer",
    RoleEnum.lead_h_and_s: "health_and_safety_lead",
    RoleEnum.lead_sustainability: "sustainability_strategy_leader",
    RoleEnum.lead_bpm: "project_building_performance_modeller",
    RoleEnum.lead_acoustics: "project_acoustician",
    RoleEnum.lead_passivhaus: "project_passivhaus_designer",
    RoleEnum.project_engineer: "project_engineer",
    RoleEnum.proj_coordinator: "project_coordinator",
    RoleEnum.proj_admin: "project_coordinator",
    RoleEnum.rev_strategy: "sector_strategy_reviewer",
    RoleEnum.rev_technical: "sector_strategy_reviewer",
    RoleEnum.eng_bpm: "building_performance_modeller",
    RoleEnum.eng_systems: "engineer",
    RoleEnum.eng_site: "site_engineer",
    RoleEnum.eng_digital: "digital_design_engineer",
    RoleEnum.eng_acoustics: "acoustician",
    RoleEnum.eng_passivhaus: "passivhaus_designer",
    RoleEnum.con_sustainability: "sustainability_consultant",
    RoleEnum.con_bim: "bim_strategy_advisor",
}

map_titles = {k.value: map_new_name_title[v] for k, v in map_project_roles.items()}
import pathlib
import json
(pathlib.Path(__file__).parent / "map-project-roles.json").write_text(json.dumps(map_titles, indent=4))
